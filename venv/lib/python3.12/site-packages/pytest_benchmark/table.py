"""
..
  PYTEST_DONT_REWRITE
"""

import operator
import sys
from math import isinf

from .utils import report_online_progress
from .utils import report_progress

NUMBER_FMT = '{0:,.4f}' if sys.version_info[:2] > (2, 6) else '{0:.4f}'
ALIGNED_NUMBER_FMT = '{0:>{1},.4f}{2:<{3}}' if sys.version_info[:2] > (2, 6) else '{0:>{1}.4f}{2:<{3}}'


class TableResults:
    def __init__(self, columns, sort, histogram, name_format, logger, scale_unit):
        self.columns = columns
        self.sort = sort
        self.histogram = histogram
        self.name_format = name_format
        self.logger = logger
        self.scale_unit = scale_unit

    def display(self, tr, groups, progress_reporter=report_progress):
        tr.write_line('')
        report_online_progress(progress_reporter, tr, 'Computing stats ...')
        for line, (group, benchmarks) in progress_reporter(groups, tr, 'Computing stats ... group {pos}/{total}'):
            benchmarks = sorted(benchmarks, key=operator.itemgetter(self.sort))
            for bench in benchmarks:
                bench['name'] = self.name_format(bench)

            worst = {}
            best = {}
            solo = len(benchmarks) == 1
            for line1, prop in progress_reporter(
                ('min', 'max', 'mean', 'median', 'iqr', 'stddev', 'ops'), tr, '{line}: {value}', line=line
            ):
                if prop == 'ops':
                    worst[prop] = min(bench[prop] for _, bench in progress_reporter(benchmarks, tr, '{line} ({pos}/{total})', line=line1))
                    best[prop] = max(bench[prop] for _, bench in progress_reporter(benchmarks, tr, '{line} ({pos}/{total})', line=line1))
                else:
                    worst[prop] = max(bench[prop] for _, bench in progress_reporter(benchmarks, tr, '{line} ({pos}/{total})', line=line1))
                    best[prop] = min(bench[prop] for _, bench in progress_reporter(benchmarks, tr, '{line} ({pos}/{total})', line=line1))
            for line1, prop in progress_reporter(('outliers', 'rounds', 'iterations'), tr, '{line}: {value}', line=line):
                worst[prop] = max(
                    benchmark[prop] for _, benchmark in progress_reporter(benchmarks, tr, '{line} ({pos}/{total})', line=line1)
                )

            unit, adjustment = self.scale_unit(unit='seconds', benchmarks=benchmarks, best=best, worst=worst, sort=self.sort)
            ops_unit, ops_adjustment = self.scale_unit(unit='operations', benchmarks=benchmarks, best=best, worst=worst, sort=self.sort)
            labels = {
                'name': f'Name (time in {unit}s)',
                'min': 'Min',
                'max': 'Max',
                'mean': 'Mean',
                'stddev': 'StdDev',
                'rounds': 'Rounds',
                'iterations': 'Iterations',
                'iqr': 'IQR',
                'median': 'Median',
                'outliers': 'Outliers',
                'ops': f'OPS ({ops_unit}ops/s)' if ops_unit else 'OPS',
            }
            widths = {
                'name': 3 + max(len(labels['name']), max(len(benchmark['name']) for benchmark in benchmarks)),
                'rounds': 2 + max(len(labels['rounds']), len(str(worst['rounds']))),
                'iterations': 2 + max(len(labels['iterations']), len(str(worst['iterations']))),
                'outliers': 2 + max(len(labels['outliers']), len(str(worst['outliers']))),
                'ops': 2 + max(len(labels['ops']), len(NUMBER_FMT.format(best['ops'] * ops_adjustment))),
            }
            for prop in 'min', 'max', 'mean', 'stddev', 'median', 'iqr':
                widths[prop] = 2 + max(len(labels[prop]), max(len(NUMBER_FMT.format(bench[prop] * adjustment)) for bench in benchmarks))

            rpadding = 0 if solo else 10
            labels_line = labels['name'].ljust(widths['name']) + ''.join(
                labels[prop].rjust(widths[prop]) + (' ' * rpadding if prop not in ['outliers', 'rounds', 'iterations'] else '')
                for prop in self.columns
            )
            report_online_progress(progress_reporter, tr, '')
            tr.write_line(
                ' benchmark{name}: {count} tests '.format(
                    count=len(benchmarks),
                    name='' if group is None else f' {group!r}',
                ).center(len(labels_line), '-'),
                yellow=True,
            )
            tr.write_line(labels_line)
            tr.write_line('-' * len(labels_line), yellow=True)

            for bench in benchmarks:
                has_error = bench.get('has_error')
                tr.write(bench['name'].ljust(widths['name']), red=has_error, invert=has_error)
                for prop in self.columns:
                    if prop in ('min', 'max', 'mean', 'stddev', 'median', 'iqr'):
                        tr.write(
                            ALIGNED_NUMBER_FMT.format(
                                bench[prop] * adjustment, widths[prop], compute_baseline_scale(best[prop], bench[prop], rpadding), rpadding
                            ),
                            green=not solo and bench[prop] == best.get(prop),
                            red=not solo and bench[prop] == worst.get(prop),
                            bold=True,
                        )
                    elif prop == 'ops':
                        tr.write(
                            ALIGNED_NUMBER_FMT.format(
                                bench[prop] * ops_adjustment,
                                widths[prop],
                                compute_baseline_scale(best[prop], bench[prop], rpadding),
                                rpadding,
                            ),
                            green=not solo and bench[prop] == best.get(prop),
                            red=not solo and bench[prop] == worst.get(prop),
                            bold=True,
                        )
                    else:
                        tr.write('{0:>{1}}'.format(bench[prop], widths[prop]))
                tr.write('\n')
            tr.write_line('-' * len(labels_line), yellow=True)
            tr.write_line('')
            if self.histogram:
                from .histogram import make_histogram  # noqa: PLC0415

                if len(benchmarks) > 75:
                    self.logger.warning(f'Group {group!r} has too many benchmarks. Only plotting 50 benchmarks.')
                    benchmarks = benchmarks[:75]

                output_file = make_histogram(self.histogram, group, benchmarks, unit, adjustment)

                self.logger.info(f'Generated histogram: {output_file}', bold=True)

        tr.write_line('Legend:')
        tr.write_line('  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.')
        tr.write_line('  OPS: Operations Per Second, computed as 1 / Mean')


def compute_baseline_scale(baseline, value, width):
    if not width:
        return ''
    if value == baseline:
        return ' (1.0)'.ljust(width)

    scale = abs(value / baseline) if baseline else float('inf')
    if scale > 1000:
        if isinf(scale):
            return ' (inf)'.ljust(width)
        else:
            return ' (>1000.0)'.ljust(width)
    else:
        return f' ({scale:.2f})'.ljust(width)
