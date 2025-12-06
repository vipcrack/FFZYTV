#!/usr/bin/env python3
# generate_ffzytv_project.py (SAFE FINAL VERSION)
# 只生成源码和配置，不碰 Gradle Wrapper！

import os
from pathlib import Path

PROJECT_NAME = "FFZYTV"
PACKAGE_NAME = "com.ffzy.tv"
APP_DIR = Path(PROJECT_NAME)
SRC_DIR = APP_DIR / "app" / "src" / "main"
JAVA_SRC = SRC_DIR / "java" / "com" / "ffzy" / "tv"

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✅ {path}")

def create_project_structure():
    folders = [
        SRC_DIR / "res" / "layout",
        SRC_DIR / "res" / "values",
        SRC_DIR / "res" / "mipmap-mdpi",
        JAVA_SRC,
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

# --- 以下函数保持不变（略去重复代码，仅保留关键部分）---
def generate_project_build_gradle():
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
    write_file(APP_DIR / "build.gradle", content)

def generate_settings_gradle():
    content = '''pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = 'FFZYTV'
include ':app'
'''
    write_file(APP_DIR / "settings.gradle", content)

def generate_gradle_properties():
    content = '''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true
kotlin.code.style=official
'''
    write_file(APP_DIR / "gradle.properties", content)

def generate_app_build_gradle():
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
    write_file(APP_DIR / "app" / "build.gradle", content)

def generate_manifest():
    content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-feature
        android:name="android.software.leanback"
        android:required="true" />
    <uses-feature
        android:name="android.hardware.touchscreen"
        android:required="false" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.Leanback"
        tools:targetApi="34">
        
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LEANBACK_LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
'''
    write_file(SRC_DIR / "AndroidManifest.xml", content)

def generate_main_activity():
    content = '''package com.ffzy.tv

import android.os.Bundle
import androidx.fragment.app.FragmentActivity

class MainActivity : FragmentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}
'''
    write_file(JAVA_SRC / "MainActivity.kt", content)

def generate_layout():
    content = '''<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@android:color/black">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="center"
        android:text="FFZYTV"
        android:textColor="@android:color/white"
        android:textSize="32sp" />

</FrameLayout>
'''
    write_file(SRC_DIR / "res" / "layout" / "activity_main.xml", content)

def generate_strings():
    content = '''<resources>
    <string name="app_name">FFZYTV</string>
</resources>
'''
    write_file(SRC_DIR / "res" / "values" / "strings.xml", content)

def generate_dummy_icon():
    icon = '''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="48dp"
    android:height="48dp"
    android:viewportWidth="48"
    android:viewportHeight="48">
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M12,36 L36,36 L36,12 L12,12 Z" />
</vector>
'''
    write_file(SRC_DIR / "res" / "mipmap-mdpi" / "ic_launcher.xml", icon)

def main():
    print(f"🚀 正在生成 FFZYTV Android TV 项目...\n")
    
    create_project_structure()
    generate_project_build_gradle()
    generate_settings_gradle()
    generate_gradle_properties()
    generate_app_build_gradle()
    generate_manifest()
    generate_main_activity()
    generate_layout()
    generate_strings()
    generate_dummy_icon()

    print("\n🎉 项目源码生成完成！")
    print(f"\n📁 项目路径: ./{PROJECT_NAME}")
    print("\n🔧 下一步：使用系统 Gradle 生成 Wrapper（确保已安装 Gradle）")
    print(f"  cd {PROJECT_NAME}")
    print("  gradle wrapper --gradle-version 8.7")
    print("\n📦 然后构建：")
    print("  ./gradlew assembleDebug --no-daemon --stacktrace")

if __name__ == "__main__":
    main()
