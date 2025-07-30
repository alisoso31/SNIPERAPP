[app]
title = SniperApp
package.name = sniperapp
package.domain = org.example
source.dir = .
version = 0.1
requirements = python3,kivy==2.2.1,kivymd,requests,cryptography,pandas,numpy,websocket-client,certifi,charset-normalizer,urllib3,solana,bip_utils,pyjnius
orientation = landscape

[android]
p4a.bootstrap = sdl2
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a
android.copy_libs = 1
android.enable_androidx = True
android.permissions = INTERNET
android.apptheme = @android:style/Theme.NoTitleBar
android.entrypoint = org.kivy.android.PythonActivity

[buildozer]
log_level = 2
