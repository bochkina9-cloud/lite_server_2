# 📡 Lite Server

Мини HTTP-сервер для Android — аналог Simple HTTP Server.

## ✨ Функционал
- 📂 Выбор папки для раздачи файлов
- ▶️ Кнопка Старт/Стоп сервера
- 🌐 Показ IP-адреса + порт
- 📱 Встроенный WebView для просмотра сайтов
- 🔗 Кнопка "Открыть в браузере"
- 🔔 Уведомление в статус-баре

## 📱 Сборка APK через GitHub Actions

### Шаг 1: Создай репозиторий на GitHub
```bash
cd lite_server
git init
git add .
git commit -m "feat: initial Lite Server app"
git remote add origin https://github.com/ТВОЙ_ЛОГИН/lite_server.git
git push -u origin master
```

### Шаг 2: Включи GitHub Actions
1. Открой репозиторий → вкладка **Actions**
2. Нажми **"I understand my workflows, go ahead and enable them"**
3. Нажми **"Run workflow"** → **"Build APK"**

### Шаг 3: Скачай APK
1. После завершения сборки (~15-20 минут)
2. Открой **Actions** → последний запуск → **Artifacts**
3. Скачай `lite-server-apk`

## 🛠 Локальная сборка (Linux/WSL)
```bash
pip install buildozer
buildozer android debug
```

## 📋 Использование
1. Установи APK на Android
2. Нажми "Выбрать папку" → укажи папку с файлами
3. Нажми "Старт" → сервер запустится
4. Открой в браузере: `http://IP_АДРЕС:8080`
5. Или нажми "Открыть" для встроенного просмотра

## 📦 Структура проекта
```
lite_server/
├── main.py              # Приложение Kivy
├── buildozer.spec       # Конфигурация сборки APK
├── .github/workflows/
│   └── build.yml        # GitHub Actions для автосборки
└── README.md            # Эта инструкция
```

---

## 📝 Статус проекта (обновлено 2025-05-24)

### ✅ Что сделано
1. **main.py** (434 строки) — полноценное Kivy-приложение:
   - HTTP-сервер на порту 8080 с раздачей файлов
   - Выбор папки через файловый диалог
   - Отображение IP-адреса и порта
   - Кнопки Старт/Стоп, Открыть в браузере
   - Список подключённых клиентов
   - Сохранение настроек (последняя папка, порт)
   - Лог запросов в реальном времени
2. **buildozer.spec** — конфигурация сборки APK:
   - API 31, NDK 25b, SDK 33 (понижено для стабильности)
   - Архитектура: arm64-v8a (убрано armeabi-v7a для скорости)
   - Права: INTERNET, WiFi, хранилище
   - android.accept_sdk_license = True
   - android.enable_androidx = True
   - Убрана ссылка на несуществующий service.py
3. **build.yml** — GitHub Actions для автосборки:
   - Ветка `master`
   - Buildozer Action v1.2.0
   - Upload APK как Artifact
   - Создание Release при ручном запуске
4. **build_apk_colab.ipynb** — Jupyter ноутбук для сборки в Google Colab
5. **test_gemini35.py** — тестовый скрипт

### ⚠️ Что нужно исправить / доделать
1. **Сборка APK** — основная проблема:
   - Docker build падает с ошибкой Annotations (1 error)
   - Возможные причины: несовместимость NDK/SDK версий, проблемы с Buildozer
   - **Решение**: попробовать понизить `android.api = 31`, `android.ndk = 25b`, `android.sdk = 33`
   - Или собрать через Google Colab (build_apk_colab.ipynb)
2. **presplash.png** — файл не существует, но ссылка была в buildozer.spec (убрана)
3. **service.py** — файл не существует, ссылка убрана из buildozer.spec
4. **icon.png** — существует в корне и в icons/, используется корневой
5. **session/sessions.json** — хранит сессии, работает корректно

### 🔧 Рекомендации по исправлению сборки
- Попробовать `android.api = 31` вместо 33
- Попробовать `android.ndk = 25b` вместо 27b
- Убрать `android.archs = armeabi-v7a` (оставить только arm64)
- Добавить `android.accept_sdk_license = True`
- Проверить совместимость Kivy версии с Buildozer
