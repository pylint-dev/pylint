Add 2 new command line options: use-local-configs and use-parent-configs.

use-local-configs enables searching for local pylint configurations in the same directory where linted file is located.
For example:
if there exists package/pylintrc, then
pylint --use-local-configs=y package/file.py
will use package/pylintrc instead of default config from $PWD.

use-parent-configs enables searching for local pylint configurations upwards from the directory where linted file is located.
For example:
if there exists package/pylintrc, and doesn't exist package/subpackage/pylintrc, then
pylint --use-local-configs=y --use-parent-configs=y package/subpackage/file.py
will use package/pylintrc instead of default config from $PWD.

Closes #618
