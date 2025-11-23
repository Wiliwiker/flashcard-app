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
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf

# (list) Source files to exclude (let empty to not exclude anything)
# source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude)
# source.exclude_dirs = tests, bin, venv

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (str) Presplash image to use at startup
#presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/assets/icon.png

# (list) List of application requirements
# Comma separated e.g. requirements = sqlite3,kivy
requirements = python3, kivy==2.3.0

# (str) Supported orientation (landscape, portrait, or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
# Updated to a more modern API level for better compatibility [citation:1].
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Path to the Android NDK, uncomment and set if needed
# android.ndk_path = /path/to/ndk

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (list) The Android archs to build for
# In a real-world scenario, you would likely add arm64-v8a
android.archs = armeabi-v7a

# (bool) Enable Android auto backup feature (Android API >=23)
android.allow_backup = True

# (bool) If True, then skip trying to update the Android SDK
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

#
# Buildozer configuration
#

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage and the default build command
# buildozer will create a 'bin' directory here to store the generated packages.
# build_dir = /path/to/build/folder

# (str) Path to build output (i.e. .apk, .aab files) storage
# bin_dir = /path/to/bin/folder
