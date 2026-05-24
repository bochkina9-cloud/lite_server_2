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
requirements = python3,kivy,pyjnius

# Android permissions
android.permissions = INTERNET,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# API level
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# Архитектура
android.archs = arm64-v8a, armeabi-v7a

# Иконка
icon.filename = %(source.dir)s/icon.png

# Presplash (экран загрузки)
presplash.filename = %(source.dir)s/presplash.png
presplash.landscape = True

# Ориентация
orientation = portrait

# Полноэкранный режим
fullscreen = 0

# Android entry point
android.allow_backup = True

# Services (HTTP сервер работает в фоне)
services = HTTPServer:service.py:foreground

# Wake lock (не засыпать при работе сервера)
android.wakelock = True

# Тема Android
android.theme = @android:style/Theme.DeviceDefault.Light.NoActionBar

# Logcat
android.logcat_filters = *:S python:D

# Класс приложения (для доступа к файлам Android 11+)
android.entrypoint = org.kivy.android.PythonActivity

# Gradle зависимости
android.gradle_dependencies = 

# Intent filters (для открытия файлов)
android.manifest.intent_filters = 

# Meta data
android.meta_data = 

[buildozer]

# Лог
log_level = 2

# Директория сборки
build_dir = ./.buildozer
bin_dir = ./bin

# Android
android.logcat_filters = *:S python:D
