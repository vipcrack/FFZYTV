#!/usr/bin/env python3
import os
from base64 import b64decode

PACKAGE = "com.ffzy.tv"
APP_NAME = "非凡影视"
LAUNCH_URL = "http://cj.ffzyapi.com/"
TRANSPARENT_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAsgByZ0dVjYAAAAASUVORK5CYII="

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def write_binary_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

# Root build.gradle
write_file("build.gradle", """
buildscript {
    repositories { google(); mavenCentral(); }
    dependencies { classpath 'com.android.tools.build:gradle:8.5.0'; }
}
""")

# settings.gradle
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

# gradle-wrapper.properties (with Tencent mirror)
write_file("gradle/wrapper/gradle-wrapper.properties", """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://mirrors.cloud.tencent.com/gradle/gradle-8.7-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")

# app/build.gradle
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

# AndroidManifest.xml
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

# strings.xml
write_file("app/src/main/res/values/strings.xml", f"""<?xml version="1.0" encoding="utf-8"?>
<resources><string name="app_name">{APP_NAME}</string></resources>""")

# styles.xml
write_file("app/src/main/res/values/styles.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources><style name="AppTheme" parent="Theme.AppCompat.NoActionBar">
    <item name="android:windowFullscreen">true</item>
</style></resources>""")

# MainActivity.java
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

# ic_launcher.png (transparent 1x1)
for d in ["mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]:
    write_binary_file(f"app/src/main/res/mipmap-{d}/ic_launcher.png", b64decode(TRANSPARENT_PNG_B64))

# gradlew
if os.name == "nt":
    write_file("gradlew.bat", "@echo off\njava -classpath gradle/wrapper/gradle-wrapper.jar org.gradle.wrapper.GradleWrapperMain %*\n")
else:
    write_file("gradlew", "#!/bin/sh\nexec \"$(dirname \"$0\")/gradle/wrapper/gradle-wrapper.jar\" \"$@\"\n")
    os.chmod("gradlew", 0o755)

print("✅ Project generated successfully!")