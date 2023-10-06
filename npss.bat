@echo off
@SET _calldir=%CD%
@SET EMI_TOP="C:\NPSS\NPSS.EMI.14.0.1_LE"
@SET EMI_TOP=%EMI_TOP:"=%
@Set NPSS_VERSION_STRING=NPSS_3.2_nt_Release_VC14_64
@CALL "C:\NPSS\NPSS.nt.ver32_VC14_64_LE\scripts\npssenv.bat"
@SET PATH=%EMI_TOP%\scripts\nt;%EMI_TOP%\scripts\AutoDoc;%PATH%

REM Include the current directory paths that are relavant
@SET NPSS_PATH=%CD%\utils;%CD%\Models;%CD%\maps

@cd %_calldir%
@SET _calldir=
@REM echo %NPSS_PATH%

REM SHORTCUTS ADDED BY PRASH... DEC 2020
doskey pwd=echo %cd%
doskey npss=runnpss $* 
doskey killnpss=taskkill /f /fi "imagename eq npssle.nt.exe"
doskey listnpss=tasklist /fi "imagename eq npssle.nt.exe"

doskey ls=dir 