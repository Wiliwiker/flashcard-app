[app]

# (str) Title of your application
title = Flashcard App

# (str) Package name
package.name = flashcardapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,ttf


source.include_patterns = icon.png, adaptive_icon_fg.png, adaptive_icon_bg.png


# (str) Application versioning (method 1)
version = 0.1

# (list) List of application requirements
requirements = python3,
    kivy,
    https://github.com/kivymd/KivyMD/archive/master.zip,
    materialyoucolor,
    materialshapes,
    pillow,
    exceptiongroup,
    asyncgui,
    asynckivy,
    android

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (list) List of Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# For CI builds, stick to one architecture to save time and memory
android.arch = arm64-v8a

# (bool) Enable Android X (Android Jetpack) support
android.enable_androidx = True

# (bool) If True, then skip trying to update the Android SDK
# This can help with CI stability
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1





# (str) Icon of the application
icon.filename = 'icon.png'

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
icon.adaptive_foreground.filename = 'adaptive_icon_fg.png'
icon.adaptive_background.filename = 'adaptive_icon_bg.png'


# (str) Presplash
presplash.filename = 'icon.png'