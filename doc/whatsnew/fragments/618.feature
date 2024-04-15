Add new command line option: use-local-configs.

use-local-configs enables loading of local pylint configurations in addition to the base pylint config from $PWD. Local configurations are searched in the same directories where linted files are located and upwards until $PWD or root.
For example:
if there exists package/pylintrc, then
pylint --use-local-configs=y package/file.py
will use package/pylintrc instead of default config from $PWD.

if there exists package/pylintrc, and doesn't exist package/subpackage/pylintrc, then
pylint --use-local-configs=y package/subpackage/file.py
will use package/pylintrc instead of default config from $PWD.

Closes #618
