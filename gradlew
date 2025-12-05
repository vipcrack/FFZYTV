# 创建 gradle/wrapper 目录
mkdir -p gradle/wrapper

# 下载官方 gradle-wrapper.jar（Gradle 8.7）
curl -sL https://services.gradle.org/distributions/gradle-8.7-bin.zip -o /tmp/gradle.zip
unzip -q -o /tmp/gradle.zip 'gradle-8.7/lib/gradle-wrapper-8.7.jar' -d /tmp/
mv /tmp/gradle-8.7/lib/gradle-wrapper-8.7.jar gradle/wrapper/gradle-wrapper.jar

# 创建 gradlew
cat > gradlew << 'EOF'
#!/bin/sh
scriptDir="$(cd "$(dirname "$0")" && pwd)"
exec java -classpath "$scriptDir/gradle/wrapper/gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain "$@"
EOF
chmod +x gradlew

# 创建 gradlew.bat（Windows 兼容）
cat > gradlew.bat << 'EOF'
@echo off
set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_HOME=%DIRNAME%
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi
set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar
java "-Dorg.gradle.appname=%APP_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
EOF

# 创建 properties
cat > gradle/wrapper/gradle-wrapper.properties << EOF
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.7-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
EOF