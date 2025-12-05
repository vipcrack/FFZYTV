#!/usr/bin/env python3
"""
一键生成 FFZY TV Android 应用（需提前存在 gradle wrapper）
"""

import os
from base64 import b64decode

# === 配置区 ===
PACKAGE_NAME = "com.ffzy.tv"
APP_LABEL = "非凡影视"
LAUNCH_URL = "http://cj.ffzyapi.com/"

# 极简透明 PNG（1x1 像素）
TRANSPARENT_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAsgByZ0dVjYAAAAASUVORK5CYII="

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def write_binary_file(path: str, data: bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

def main():
    # === 1. 项目根目录 build.gradle ===
    write_file("build.gradle", """
// Top-level build file
buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.5.0'
    }
}
""")

    # === 2. settings.gradle ===
    write_file("settings.gradle", """
pluginManagement {
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
rootProject.name = "FFZYTV"
include ':app'
""")

    # === 3. app/build.gradle ===
    write_file("app/build.gradle", f"""
plugins {{
    id 'com.android.application'
}}

android {{
    namespace '{PACKAGE_NAME}'
    compileSdk 34

    defaultConfig {{
        applicationId "{PACKAGE_NAME}"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }}

    buildTypes {{
        release {{
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }}
    }}

    compileOptions {{
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }}
}}

dependencies {{
    implementation 'androidx.appcompat:appcompat:1.7.0'
    implementation 'androidx.webkit:webkit:1.12.0'
}}
""")

    # === 4. AndroidManifest.xml ===
    write_file("app/src/main/AndroidManifest.xml", f"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET"/>
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="landscape">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
                <category android:name="android.intent.category.LEANBACK_LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

    # === 5. strings.xml ===
    write_file("app/src/main/res/values/strings.xml", f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{APP_LABEL}</string>
</resources>
""")

    # === 6. styles.xml ===
    write_file("app/src/main/res/values/styles.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.NoActionBar">
        <item name="android:windowFullscreen">true</item>
        <item name="android:windowContentOverlay">@null</item>
    </style>
</resources>
""")

    # === 7. MainActivity.java ===
    java_dir = f"app/src/main/java/{PACKAGE_NAME.replace('.', '/')}"
    write_file(f"{java_dir}/MainActivity.java", f"""package {PACKAGE_NAME};

import android.os.Bundle;
import android.webkit.WebView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        WebView webView = new WebView(this);
        setContentView(webView);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setUseWideViewPort(true);
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.loadUrl("{LAUNCH_URL}");
    }}
}}
""")

    # === 8. 透明图标（所有密度）===
    for density in ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]:
        icon_path = f"app/src/main/res/mipmap-{density}/ic_launcher.png"
        write_binary_file(icon_path, b64decode(TRANSPARENT_PNG_B64))

    print("✅ FFZY TV 项目已生成！")
    print("📁 项目结构已就绪，可直接运行 ./gradlew assembleDebug")

if __name__ == "__main__":
    main()