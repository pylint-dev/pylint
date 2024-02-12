Add new command line option: use-local-configs.

use-local-configs enables searching for local pylint configurations in the same directory where linted file is located and upwards until $PWD or root.
For example:
if there exists package/pylintrc, then
pylint --use-local-configs=y package/file.py
will use package/pylintrc instead of default config from $PWD.

if there exists package/pylintrc, and doesn't exist package/subpackage/pylintrc, then
pylint --use-local-configs=y package/subpackage/file.py
will use package/pylintrc instead of default config from $PWD.

Closes #618
