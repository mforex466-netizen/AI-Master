[app]
title = AI MASTER
package.name = aimaster
package.domain = uz.sergeli
source.dir = .
source.include_exts = py,json,kv,png,jpg,atlas,md
version = 1.1.0
requirements = python3==3.11.5,hostpython3==3.11.5,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.permissions = INTERNET
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
