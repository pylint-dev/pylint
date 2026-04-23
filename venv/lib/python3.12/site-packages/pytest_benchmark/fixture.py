"""
..
  PYTEST_DONT_REWRITE
"""

import cProfile
import gc
import pstats
import sys
import time
import traceback
import typing
from math import ceil
from pathlib import Path

from .timers import compute_timer_precision
from .utils import NameWrapper
from .utils import format_time
from .utils import slugify

statistics: typing.Any
statistics_error: typing.Optional[str] = None
try:
    import statistics
except (ImportError, SyntaxError):
    statistics_error = traceback.format_exc()
    statistics = None
else:
    statistics_error = None
    from .stats import Metadata


class FixtureAlreadyUsed(Exception):
    pass


class PauseInstrumentation:
    def __init__(self, tracer=True, profiler=True):
        self.disable_profiler = profiler
        self.disable_tracer = tracer
        self.prev_tracer = None
        self.prev_profiler = None

    def __enter__(self):
        if self.disable_tracer:
            self.prev_tracer = sys.gettrace()
            if self.prev_tracer:
                sys.settrace(None)
        if self.disable_profiler:
            self.prev_profiler = sys.getprofile()
            if self.prev_profiler:
                sys.setprofile(None)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.prev_tracer:
            sys.settrace(self.prev_tracer)
        if self.prev_profiler:
            sys.setprofile(self.prev_profiler)


class BenchmarkFixture:
    _precisions: typing.ClassVar[dict[str, float]] = {}

    def __init__(
        self,
        node,
        disable_gc,
        timer,
        min_rounds,
        min_time,
        max_time,
        warmup,
        warmup_iterations,
        calibration_precision,
        add_stats,
        logger,
        warner,
        disabled,
        cprofile,
        cprofile_loops,
        cprofile_dump,
        group=None,
    ):
        self.name = node.name
        self.fullname = node._nodeid
        self.disabled = disabled
        if hasattr(node, 'callspec'):
            self.param = node.callspec.id
            self.params = node.callspec.params
        else:
            self.param = None
            self.params = None
        self.group = group
        self.has_error = False
        self.extra_info = {}
        self.skipped = False

        self._disable_gc = disable_gc
        self._timer = timer.target
        self._min_rounds = min_rounds
        self._max_time = float(max_time)
        self._min_time = float(min_time)
        self._add_stats = add_stats
        self._calibration_precision = calibration_precision
        self._warmup = warmup and warmup_iterations
        self._logger = logger
        self._warner = warner
        self._cleanup_callbacks = []
        self._mode = None
        self.cprofile = cprofile
        self.cprofile_loops = cprofile_loops
        self.cprofile_dump = cprofile_dump
        self.cprofile_stats = None
        self.stats = None

    @property
    def enabled(self):
        return not self.disabled

    def _get_precision(self, timer):
        if timer in self._precisions:
            timer_precision = self._precisions[timer]
        else:
            timer_precision = self._precisions[timer] = compute_timer_precision(timer)
            self._logger.debug('')
            self._logger.debug(f'Computing precision for {NameWrapper(timer)} ... {format_time(timer_precision)}s.', blue=True, bold=True)
        return timer_precision

    def _make_runner(self, function_to_benchmark, args, kwargs):
        def runner(loops_range, timer=self._timer):
            gc_enabled = gc.isenabled()
            if self._disable_gc:
                gc.disable()
            try:
                if loops_range:
                    start = timer()
                    for _ in loops_range:
                        function_to_benchmark(*args, **kwargs)
                    end = timer()
                    return end - start
                else:
                    start = timer()
                    result = function_to_benchmark(*args, **kwargs)
                    end = timer()
                    return end - start, result
            finally:
                if gc_enabled:
                    gc.enable()

        return runner

    def _make_stats(self, iterations):
        bench_stats = Metadata(
            self,
            iterations=iterations,
            options={
                'disable_gc': self._disable_gc,
                'timer': self._timer,
                'min_rounds': self._min_rounds,
                'max_time': self._max_time,
                'min_time': self._min_time,
                'warmup': self._warmup,
            },
        )
        self._add_stats(bench_stats)
        self.stats = bench_stats
        return bench_stats

    def _save_cprofile(self, profile: cProfile.Profile):
        stats = pstats.Stats(profile)
        self.stats.cprofile_stats = stats
        if self.cprofile_dump:
            output_file = Path(f'{self.cprofile_dump}-{slugify(self.name)}.prof')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            stats.dump_stats(output_file)
            self._logger.info(f'Saved profile: {output_file}', bold=True)

    def __call__(self, function_to_benchmark, *args, **kwargs):
        if self._mode:
            self.has_error = True
            raise FixtureAlreadyUsed(f'Fixture can only be used once. Previously it was used in {self._mode} mode.')
        try:
            self._mode = 'benchmark(...)'
            return self._raw(function_to_benchmark, *args, **kwargs)
        except Exception:
            self.has_error = True
            raise

    def pedantic(self, target, args=(), kwargs=None, setup=None, teardown=None, rounds=1, warmup_rounds=0, iterations=1):
        if self._mode:
            self.has_error = True
            raise FixtureAlreadyUsed(f'Fixture can only be used once. Previously it was used in {self._mode} mode.')
        try:
            self._mode = 'benchmark.pedantic(...)'
            return self._raw_pedantic(
                target,
                args=args,
                kwargs=kwargs,
                setup=setup,
                teardown=teardown,
                rounds=rounds,
                warmup_rounds=warmup_rounds,
                iterations=iterations,
            )
        except Exception:
            self.has_error = True
            raise

    def _raw(self, function_to_benchmark, *args, **kwargs):
        loops_range = None

        if self.enabled:
            runner = self._make_runner(function_to_benchmark, args, kwargs)

            with PauseInstrumentation():
                duration, iterations, loops_range = self._calibrate_timer(runner)

            # Choose how many times we must repeat the test
            rounds = ceil(self._max_time / duration)
            rounds = max(rounds, self._min_rounds)
            rounds = min(rounds, sys.maxsize)

            stats = self._make_stats(iterations)

            self._logger.debug(f'  Running {rounds} rounds x {iterations} iterations ...', yellow=True, bold=True)
            run_start = time.time()
            if self._warmup:
                warmup_rounds = min(rounds, max(1, int(self._warmup / iterations)))
                self._logger.debug(f'  Warmup {warmup_rounds} rounds x {iterations} iterations ...')
                with PauseInstrumentation():
                    for _ in range(warmup_rounds):
                        runner(loops_range)
            with PauseInstrumentation():
                for _ in range(rounds):
                    stats.update(runner(loops_range))
            self._logger.debug(f'  Ran for {format_time(time.time() - run_start)}s.', yellow=True, bold=True)
        if self.cprofile_loops is None:
            cprofile_loops = loops_range or range(1)
        else:
            cprofile_loops = range(self.cprofile_loops)
        if self.enabled and self.cprofile:
            with PauseInstrumentation():
                profile = cProfile.Profile()
                for _ in cprofile_loops:
                    function_result = profile.runcall(function_to_benchmark, *args, **kwargs)
                self._save_cprofile(profile)
        else:
            function_result = function_to_benchmark(*args, **kwargs)
        return function_result

    def _raw_pedantic(self, target, args=(), kwargs=None, setup=None, teardown=None, rounds=1, warmup_rounds=0, iterations=1):
        if kwargs is None:
            kwargs = {}

        has_args = bool(args or kwargs)

        if not isinstance(iterations, int) or iterations < 1:
            raise ValueError('Must have positive int for `iterations`.')

        if not isinstance(rounds, int) or rounds < 1:
            raise ValueError('Must have positive int for `rounds`.')

        if not isinstance(warmup_rounds, int) or warmup_rounds < 0:
            raise ValueError('Must have positive int for `warmup_rounds`.')

        if iterations > 1 and setup:
            raise ValueError("Can't use more than 1 `iterations` with a `setup` function.")

        def make_arguments(args=args, kwargs=kwargs):
            if setup:
                maybe_args = setup()
                if maybe_args:
                    if has_args:
                        raise TypeError("Can't use `args` or `kwargs` if `setup` returns the arguments.")
                    args, kwargs = maybe_args
            return args, kwargs

        if self.disabled:
            args, kwargs = make_arguments()
            return target(*args, **kwargs)

        stats = self._make_stats(iterations)
        loops_range = range(iterations) if iterations > 1 else None
        for _ in range(warmup_rounds):
            args, kwargs = make_arguments()

            runner = self._make_runner(target, args, kwargs)
            with PauseInstrumentation():
                runner(loops_range)

            if teardown is not None:
                teardown(*args, **kwargs)

        for _ in range(rounds):
            args, kwargs = make_arguments()

            runner = self._make_runner(target, args, kwargs)
            with PauseInstrumentation():
                if loops_range:
                    duration = runner(loops_range)
                else:
                    duration, result = runner(loops_range)
            stats.update(duration)

            if teardown is not None:
                teardown(*args, **kwargs)

        if loops_range:
            # if it has been looped then we don't have the result, we need to do 1 extra run for it
            args, kwargs = make_arguments()
            result = target(*args, **kwargs)
            if teardown is not None:
                teardown(*args, **kwargs)

        if self.cprofile:
            if self.cprofile_loops is None:
                cprofile_loops = loops_range or range(1)
            else:
                cprofile_loops = range(self.cprofile_loops)

            profile = cProfile.Profile()
            args, kwargs = make_arguments()
            for _ in cprofile_loops:
                with PauseInstrumentation():
                    profile.runcall(target, *args, **kwargs)
                if teardown is not None:
                    teardown(*args, **kwargs)
            self._save_cprofile(profile)

        return result

    def weave(self, target, **kwargs):
        try:
            import aspectlib  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(exc.args, 'Please install aspectlib or pytest-benchmark[aspect]') from exc

        def aspect(function):
            def wrapper(*args, **kwargs):
                return self(function, *args, **kwargs)

            return wrapper

        self._cleanup_callbacks.append(aspectlib.weave(target, aspect, **kwargs).rollback)

    patch = weave

    def _cleanup(self):
        while self._cleanup_callbacks:
            callback = self._cleanup_callbacks.pop()
            callback()
        if not self._mode and not self.skipped:
            self._logger.warning('Benchmark fixture was not used at all in this test!', warner=self._warner, suspend=True)

    def _calibrate_timer(self, runner):
        timer_precision = self._get_precision(self._timer)
        min_time = max(self._min_time, timer_precision * self._calibration_precision)
        min_time_estimate = min_time * 5 / self._calibration_precision
        self._logger.debug('')
        self._logger.debug(
            f'  Calibrating to target round {format_time(min_time)}s; will estimate when reaching {format_time(min_time_estimate)}s '
            f'(using: {NameWrapper(self._timer)}, precision: {format_time(timer_precision)}s).',
            yellow=True,
            bold=True,
        )

        loops = 1
        while True:
            loops_range = range(loops)
            duration = runner(loops_range)
            if self._warmup:
                warmup_start = time.time()
                warmup_iterations = 0
                warmup_rounds = 0
                while time.time() - warmup_start < self._max_time and warmup_iterations < self._warmup:
                    duration = min(duration, runner(loops_range))
                    warmup_rounds += 1
                    warmup_iterations += loops
                self._logger.debug(f'    Warmup: {format_time(time.time() - warmup_start)}s ({warmup_rounds} x {loops} iterations).')

            self._logger.debug(f'    Measured {loops} iterations: {format_time(duration)}s.', yellow=True)
            if duration >= min_time:
                break

            if duration >= min_time_estimate:
                # coarse estimation of the number of loops
                loops = ceil(min_time * loops / duration)
                self._logger.debug(f'    Estimating {loops} iterations.', green=True)
                if loops == 1:
                    # If we got a single loop then bail early - nothing to calibrate if the the
                    # test function is 100 times slower than the timer resolution.
                    loops_range = range(loops)
                    break
            else:
                loops *= 10
        return duration, loops, loops_range
