#!/bin/bash
set -e

echo "=== 1. Checking Java ==="
java -version
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
echo "JAVA_HOME=$JAVA_HOME"

echo "=== 2. Setting up Android SDK directories ==="
export ANDROID_HOME=/opt/android-sdk
export ANDROID_SDK_ROOT=/opt/android-sdk
mkdir -p /opt/android-sdk/cmdline-tools

if [ ! -f /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager ]; then
    echo "Downloading Android Commandline Tools..."
    cd /tmp
    curl -sS -o cmdline-tools.zip https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
    unzip -q cmdline-tools.zip
    mkdir -p /opt/android-sdk/cmdline-tools/latest
    cp -r cmdline-tools/* /opt/android-sdk/cmdline-tools/latest/
    rm -rf cmdline-tools cmdline-tools.zip
    cd /app/applet
fi

export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

echo "=== 3. Accepting licenses & installing SDK components ==="
mkdir -p /opt/android-sdk/licenses
echo -e "24333f8a63b6825ea9c5514f83c2829b004d1fee\nd56f5187479451eabf01fb78af6dfcb131a6481e\n84831b9409646a2a3e0f983282492b49d5f23b82" > /opt/android-sdk/licenses/android-sdk-license
echo -e "84831b9409646a2a3e0f983282492b49d5f23b82" > /opt/android-sdk/licenses/android-sdk-preview-license
yes | /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=/opt/android-sdk --licenses || true

echo "Installing platforms;android-35 and build-tools;35.0.0..."
/opt/android-sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=/opt/android-sdk "platforms;android-35" "build-tools;35.0.0" "platform-tools"

echo "Android SDK setup complete!"
