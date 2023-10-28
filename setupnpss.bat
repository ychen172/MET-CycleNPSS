echo Setting up NPSS
call C:\NPSS\NPSS.EMI.14.0.1_LE\scripts\nt\emi_NPSS_3.2.nt.Release.VC14.64.bat
SET NPSS_PATH=%CD%\ExampleRuns;%CD%\maps;%CD%\Models;%CD%\output;%CD%\utils;%CD%\temp

if not exist output (
    mkdir Output
)

if not exist temp (
    mkdir temp
)