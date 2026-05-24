[app]

# Название приложения
title = Lite Server

# Пакетное имя
package.name = liteserver

# Домен (обратный)
package.domain = org.liteserver

# Исходный код
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json

# Версия
version = 1.0.0

# Требования
requirements = kivy

# Android permissions
android.permissions = INTERNET,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# API level
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# Архитектура (только arm64 для стабильной сборки)
android.archs = arm64-v8a

# Принять лицензии SDK автоматически
android.accept_sdk_license = True

# AndroidX поддержка
android.enable_androidx = True

# Иконка
icon.filename = %(source.dir)s/icon.png

# Ориентация
orientation = portrait

# Полноэкранный режим
fullscreen = 0

# Android entry point
android.allow_backup = True

# Wake lock (не засыпать при работе сервера)
android.wakelock = True

# Тема Android
android.theme = @android:style/Theme.DeviceDefault.Light.NoActionBar

# Logcat
android.logcat_filters = *:S python:D

# Класс приложения
android.entrypoint = org.kivy.android.PythonActivity

# Gradle зависимости
android.gradle_dependencies = 

# Intent filters
android.manifest.intent_filters = 

# Meta data
android.meta_data = 

[buildozer]

# Лог
log_level = 2

# Директория сборки
build_dir = ./.buildozer
bin_dir = ./bin
