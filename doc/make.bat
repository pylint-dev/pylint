@ECHO OFF

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set BUILDDIR=_build
set ALLSPHINXOPTS=-d %BUILDDIR%/doctrees -T -E -W --keep-going -n .
if NOT "%PAPER%" == "" (
	set ALLSPHINXOPTS=-D latex_paper_size=%PAPER% %ALLSPHINXOPTS%
)

REM Check if no argument is provided, or if "help" is requested
if "%1" == "" goto help
if "%1" == "help" goto help

REM Command options
if "%1" == "install-dependencies" (
    echo Installing dependencies...
    cd .. && pip install -r doc/requirements.txt
    goto end
)

if "%1" == "clean" (
	echo Cleaning build directory...
	for /d %%i in (%BUILDDIR%\*) do rmdir /q /s %%i
	del /q /s %BUILDDIR%\*
	goto end
)

if "%1" == "html" (
	echo Building HTML...
	%SPHINXBUILD% -b html %ALLSPHINXOPTS% %BUILDDIR%/html
	if errorlevel 1 exit /b 1
	%SPHINXBUILD% -b linkcheck -q %ALLSPHINXOPTS% %BUILDDIR%/linkcheck
	if errorlevel 1 exit /b 1
	echo.
	echo Link check complete; look for any errors in the above output or in %BUILDDIR%/linkcheck/output.txt.
	goto end
)

if "%1" == "dirhtml" (
	echo Building directory-based HTML...
	%SPHINXBUILD% -b dirhtml %ALLSPHINXOPTS% %BUILDDIR%/dirhtml
	if errorlevel 1 exit /b 1
	echo.
	echo Build finished. The HTML pages are in %BUILDDIR%/dirhtml.
	goto end
)


REM Help section
:help
echo. Please use `make ^<target^>` where ^<target^> is one of:
echo.
echo.  install-dependencies   to install required documentation dependencies
echo.  html                   to make standalone HTML files
echo.  dirhtml                to make HTML files with index.html in directories
echo.  singlehtml             to make a single large HTML file
echo.  pickle                 to make pickle files
echo.  json                   to make JSON files
echo.  htmlhelp               to make HTML files and a HTML help project
echo.  qthelp                 to make HTML files and a Qt help project
echo.  devhelp                to make HTML files and a Devhelp project
echo.  epub                   to make an EPUB file
echo.  latex                  to make LaTeX files (set PAPER=a4 or PAPER=letter)
echo.  text                   to make plain text files
echo.  man                    to make manual pages
echo.  texinfo                to make Texinfo files
echo.  gettext                to make PO message catalogs
echo.  changes                to generate an overview of changed/added/deprecated items
echo.  linkcheck              to check all external links for integrity
echo.  clean                  to remove all generated files
echo.
goto end

:end
echo Script completed.
