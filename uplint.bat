goto code
use this script the reinstall currently installed pylint package.
Example on PyCharm:
1. Open terminal with interpreter where pylint is installed
2. Run: `uplint`

:code
echo y|pip uninstall pylint
SET working_dir=%cd%
cd %working_dir%
python setup.py install
cd %working_dir%
