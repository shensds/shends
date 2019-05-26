@echo off
cd /d %~dp0
set CI_ROOT=%CD%
set ANT_HOME=%CI_ROOT%/tools/ant
set JAVA_HOME=%CI_ROOT%/tools/jre_win
set PATH=%PATH%;%ANT_HOME%/bin;%JAVA_HOME%/bin;
IF NOT DEFINED PYTHONHOME set PYTHONHOME=%CI_ROOT%

pushd .
cd watcher
tasklist | findstr uciwatcher.exe > nul
if errorlevel 1 (
    echo start agent watcher...
    start /b uciwatcher.exe
) else (
    echo detect agent watcher has been started.
)
popd

title umptg
cd bin
uciagent.exe %*
