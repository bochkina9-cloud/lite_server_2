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
# Инициализация
cd lite_server
git init
git add .
git commit -m "feat: initial Lite Server app"
git remote add origin https://github.com/ТВОЙ_ЛОГИН/lite_server.git
git push -u origin main
```

### Шаг 2: Включи GitHub Actions
1. Открой репозиторий → вкладка **Actions**
2. Нажми **"I understand my workflows, go ahead and enable them"**
3. Нажми **"Run workflow"** → **"Build APK"**

### Шаг 3: Скачай APK
1. После завершения сборки (~15-20 минут)
2. Открой **Actions** → последний запуск → **Artifacts**
3. Скачай `lite_server.apk`

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
