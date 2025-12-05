#!/usr/bin/env python3
"""
一键生成 Android 项目所需的完整 Gradle Wrapper（含 gradle-wrapper.jar）
支持离线/无 Gradle 环境使用
"""

import os
import urllib.request
import zipfile
import tempfile
import shutil

# 配置
GRADLE_VERSION = "8.7"
WRAPPER_DIR = "gradle/wrapper"
MIRROR_URL = f"https://mirrors.cloud.tencent.com/gradle/gradle-{GRADLE_VERSION}-bin.zip"

def write_file(path, content, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, encoding="utf-8" if "b" not in mode else None) as f:
        f.write(content)

def download_and_extract_jar():
    print(f"📥 正在从腾讯镜像下载 Gradle {GRADLE_VERSION}...")
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "gradle.zip")
        extract_dir = os.path.join(tmpdir, "extracted")

        # 下载 ZIP
        urllib.request.urlretrieve(MIRROR_URL, zip_path)

        # 解压
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # 找到 gradle-wrapper.jar
        gradle_root = os.path.join(extract_dir, f"gradle-{GRADLE_VERSION}")
        jar_src = os.path.join(gradle_root, "lib", f"gradle-wrapper-{GRADLE_VERSION}.jar")
        jar_dst = os.path.join(WRAPPER_DIR, "gradle-wrapper.jar")

        if not os.path.exists(jar_src):
            raise FileNotFoundError(f"未找到 JAR 文件: {jar_src}")

        os.makedirs(WRAPPER_DIR, exist_ok=True)
        shutil.copy2(jar_src, jar_dst)
        print(f"✅ 已保存 gradle-wrapper.jar 到 {jar_dst}")

def main():
    # 1. gradlew (Linux/macOS)
    write_file("gradlew", """#!/bin/sh
scriptDir="$(cd "$(dirname "$0")" && pwd)"
exec java -classpath "$scriptDir/gradle/wrapper/gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain "$@"
""")
    os.chmod("gradlew", 0o755)  # 可执行

    # 2. gradlew.bat (Windows)
    write_file("gradlew.bat", r"""@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem  Gradle startup script for Windows
@rem ##########################################################################

if "%OS%"=="Windows_NT" setlocal
set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_HOME=%DIRNAME%
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi
set DEFAULT_JVM_OPTS="-Xmx64m" "-Xms64m"
if defined JAVA_HOME goto findJavaFromJavaHome
set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto execute
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
goto fail
:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe
if exist "%JAVA_EXE%" goto execute
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
goto fail
:execute
set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% "-Dorg.gradle.appname=%APP_NAME%" -classpath "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
:end
if "%ERRORLEVEL%"=="0" goto mainEnd
:fail
exit /b 1
:mainEnd
if "%OS%"=="Windows_NT" endlocal
:omega
""")

    # 3. gradle-wrapper.properties
    write_file(f"{WRAPPER_DIR}/gradle-wrapper.properties", f"""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://mirrors.cloud.tencent.com/gradle/gradle-{GRADLE_VERSION}-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")

    # 4. Download gradle-wrapper.jar
    download_and_extract_jar()

    print("\n🎉 完整 Gradle Wrapper 已生成！")
    print("✅ 文件列表:")
    print("   - gradlew")
    print("   - gradlew.bat")
    print("   - gradle/wrapper/gradle-wrapper.jar")
    print("   - gradle/wrapper/gradle-wrapper.properties")
    print("\n📌 下一步：提交这些文件到 Git 仓库！")

if __name__ == "__main__":
    main()