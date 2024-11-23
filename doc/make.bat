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


REM Help section
:help
echo. Please use `make ^<target^>` where ^<target^> is one of:
echo.
echo.  install-dependencies   to install required documentation dependencies
echo.  html                   to make standalone HTML files
echo.
goto end

:end
echo Script completed.
