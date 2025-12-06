#!/usr/bin/env python3
# fix_tv_project.py
# 用途：自动修复 Android TV 项目构建问题（Kotlin 冲突 + Theme.Leanback 缺失）

import os
import shutil
import re
from pathlib import Path

PROJECT_ROOT = Path(".").resolve()
APP_DIR = PROJECT_ROOT / "app"

def write_file(path: Path, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✅ 已写入: {path}")

def backup_file(path: Path):
    if path.exists():
        backup = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, backup)
        print(f"📦 已备份: {backup}")

def fix_project_build_gradle():
    """修复项目级 build.gradle：仅使用 plugins 块，移除 buildscript"""
    content = '''plugins {
    id 'com.android.application' version '8.5.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.20' apply false
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
'''
    backup_file(PROJECT_ROOT / "build.gradle")
    write_file(PROJECT_ROOT / "build.gradle", content)

def fix_app_build_gradle():
    """修复 app 模块 build.gradle"""
    content = '''plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.ffzy.tv'
    compileSdk 34

    defaultConfig {
        applicationId "com.ffzy.tv"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        debug {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = '17'
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.13.1'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.2.0'
    implementation 'androidx.leanback:leanback:1.1.0'

    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
'''
    backup_file(APP_DIR / "build.gradle")
    write_file(APP_DIR / "build.gradle", content)

def fix_gradle_wrapper():
    """确保使用 Gradle 8.7"""
    wrapper_props = PROJECT_ROOT / "gradle" / "wrapper" / "gradle-wrapper.properties"
    if not wrapper_props.exists():
        print("⚠️ gradle-wrapper.properties 不存在，跳过")
        return

    with open(wrapper_props, "r", encoding="utf-8") as f:
        content = f.read()

    new_url = "https\\://services.gradle.org/distributions/gradle-8.7-bin.zip"
    content = re.sub(
        r"distributionUrl\s*=\s*.*",
        f"distributionUrl={new_url}",
        content
    )

    with open(wrapper_props, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ 已设置 Gradle 8.7")

def add_gradle_properties():
    """添加或更新 gradle.properties"""
    props_file = PROJECT_ROOT / "gradle.properties"
    recommended = [
        "org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8",
        "android.useAndroidX=true",
        "android.enableJetifier=true",
        "# Fixed by fix_tv_project.py"
    ]
    content = "\n".join(recommended) + "\n"
    if props_file.exists():
        backup_file(props_file)
    write_file(props_file, content)

def clean_gradle_cache():
    """提示用户清理缓存（不自动删除全局缓存）"""
    print("\n🧹 建议手动清理缓存以确保干净构建：")
    print("   ./gradlew clean")
    print("   ./gradlew --stop")
    print("   rm -rf .gradle/")
    print("\n💡 然后运行：./gradlew assembleDebug --stacktrace\n")

def main():
    print("🔧 正在修复 Android TV 项目 (com.ffzy.tv)...\n")

    if not (PROJECT_ROOT / "build.gradle").exists():
        print("❌ 错误：请在 Android 项目根目录运行此脚本！")
        return

    if not APP_DIR.exists():
        print("❌ 错误：未找到 app/ 目录！")
        return

    fix_project_build_gradle()
    fix_app_build_gradle()
    fix_gradle_wrapper()
    add_gradle_properties()
    clean_gradle_cache()

    print("🎉 修复完成！请按上述提示清理缓存并重新构建。")

if __name__ == "__main__":
    main()