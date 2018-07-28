import glob
import os

import restructuredtext_lint

os.chdir('..')
issues = []

print('==Linting reStructuredText files with rst-lint==')

for file in glob.iglob('**/*.rst', recursive=True):
    issues.extend(restructuredtext_lint.lint_file(filepath=file))


if issues:
    for issue in issues:
        print('{type}:{filename}:{line} {message}'.format(
            type=issue.type,
            filename=issue.source,
            line=issue.line,
            message=issue.message.replace('\n', ' ')))
    print('reStructuredText linter found {} issues in rst files!'.format(
        len(issues)))
    exit(1)
