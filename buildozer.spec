[app]

# App name (shown on device)
title = Flashcard App

# Package name (unique identifier)
package.name = flashcardapp
package.domain = com.yourname

# Source code (your main Python file)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# App version
version = 0.1

# Requirements - Kivy dependencies
requirements = python3,kivy

# Android API settings
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False

# App orientation
orientation = portrait

# Full screen mode
fullscreen = 0

# Icons and splash (add these files to your project)
#icon.filename = %(source.dir)s/icon.png
#presplash.filename = %(source.dir)s/presplash.png

# Android architecture
android.archs = arm64-v8a, armeabi-v7a

# App metadata
android.meta_data = com.samsung.android.sdk.multiwindow.enable=true

[buildozer]

# Build directory
build_dir = ./.buildozer

# Binary directory  
bin_dir = ./bin

# Log level
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1