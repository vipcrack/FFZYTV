#!/usr/bin/env python3
import os
from base64 import b64decode

PACKAGE = "com.ffzy.tv"
APP_NAME = "非凡影视"
LAUNCH_URL = "http://cj.ffzyapi.com/"
TRANSPARENT_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAsgByZ0dVjYAAAAASUVORK5CYII="

def write_file(path, content):
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def write_binary_file(path, data):
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

# Root files
write_file("build.gradle", """
buildscript {
    repositories { google(); mavenCentral(); }
    dependencies { classpath 'com.android.tools.build:gradle:8.5.0'; }
}
""")

write_file("settings.gradle", """
pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal(); }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral(); }
}
rootProject.name = "FFZYTV"
include ':app'
""")

# App module
write_file("app/build.gradle", f"""
plugins {{ id 'com.android.application' }}
android {{
    namespace '{PACKAGE}'
    compileSdk 34
    defaultConfig {{
        applicationId "{PACKAGE}"
        minSdk 21
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }}
    buildTypes {{ release {{ minifyEnabled false }} }}
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

# Manifest & resources
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

write_file("app/src/main/res/values/strings.xml", f"<resources><string name=\"app_name\">{APP_NAME}</string></resources>")
write_file("app/src/main/res/values/styles.xml", """<resources><style name="AppTheme" parent="Theme.AppCompat.NoActionBar">
    <item name="android:windowFullscreen">true</item>
</style></resources>""")

java_path = f"app/src/main/java/{PACKAGE.replace('.', '/')}/MainActivity.java"
write_file(java_path, f"""package {PACKAGE};
import android.os.Bundle;
import android.webkit.WebView;
import androidx.appcompat.app.AppCompatActivity;
public class MainActivity extends AppCompatActivity {{
    @Override protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        WebView wv = new WebView(this);
        setContentView(wv);
        wv.getSettings().setJavaScriptEnabled(true);
        wv.getSettings().setDomStorageEnabled(true);
        wv.getSettings().setUseWideViewPort(true);
        wv.getSettings().setLoadWithOverviewMode(true);
        wv.loadUrl("{LAUNCH_URL}");
    }}
}}""")

for d in ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]:
    write_binary_file(f"app/src/main/res/mipmap-{d}/ic_launcher.png", b64decode(TRANSPARENT_PNG_B64))

print("✅ FFZY TV 项目已生成！")