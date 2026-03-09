"""
..
  PYTEST_DONT_REWRITE
"""

import csv
import operator
from pathlib import Path


class CSVResults:
    def __init__(self, columns, sort, logger):
        self.columns = columns
        self.sort = sort
        self.logger = logger

    def render(self, output_file, groups):
        output_file = Path(output_file)
        output_file.parent.mkdir(exist_ok=True, parents=True)

        if not output_file.suffix:
            output_file = output_file.with_suffix('.csv')
        with output_file.open('w') as stream:
            writer = csv.writer(stream)
            params = sorted(
                {param for group, benchmarks in groups for benchmark in benchmarks for param in benchmark.get('params', {}) or ()}
            )
            writer.writerow(
                [
                    'name',
                ]
                + [f'param:{p}' for p in params]
                + self.columns
            )

            for _, benchmarks in groups:
                benchmarks = sorted(benchmarks, key=operator.itemgetter(self.sort))

                for bench in benchmarks:
                    row = [bench.get('fullfunc', bench['fullname'])]
                    bench_params = bench.get('params', {})
                    bench_params = bench_params if bench_params is not None else {}
                    row.extend(bench_params.get(param, '') for param in params)
                    row.extend(bench[prop] for prop in self.columns)
                    writer.writerow(row)
        self.logger.info(f'Generated csv: {output_file}', bold=True)
