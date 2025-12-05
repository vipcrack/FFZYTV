@echo off
set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_HOME=%DIRNAME%

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar

@java.exe -Dorg.gradle.daemon=false -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
