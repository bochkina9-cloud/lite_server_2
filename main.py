"""
Lite Server — минималистичный HTTP-сервер для Android
Kivy + Buildozer → APK
"""
import os
import socket
import threading
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform

# Цвета
BG_DARK = "#1a1a2e"
BG_CARD = "#16213e"
ACCENT = "#0f3460"
ACCENT2 = "#e94560"
TEXT_WHITE = "#ffffff"
TEXT_GRAY = "#a0a0a0"
TEXT_GREEN = "#4ecca3"
TEXT_RED = "#e94560"


def get_local_ip():
    """Получить локальный IP адрес"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


class QuietHandler(SimpleHTTPRequestHandler):
    """HTTP handler без лишнего вывода"""
    def log_message(self, format, *args):
        pass  # Тихий режим

    def end_headers(self):
        # CORS заголовки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()


class ServerThread(threading.Thread):
    """Поток HTTP-сервера"""
    def __init__(self, directory, port=8080):
        super().__init__(daemon=True)
        self.directory = directory
        self.port = port
        self.server = None
        self.running = False

    def run(self):
        os.chdir(self.directory)
        self.server = HTTPServer(('0.0.0.0', self.port), QuietHandler)
        self.running = True
        try:
            self.server.serve_forever()
        except Exception:
            pass
        self.running = False

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.running = False


class LiteServerApp(App):
    def build(self):
        self.title = "Lite Server"
        self.server_thread = None
        self.server_running = False
        self.serve_dir = "/sdcard"
        self.port = 8080

        Window.clearcolor = self._hex_to_rgb(BG_DARK)

        # Главный layout
        root = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # === Заголовок ===
        title = Label(
            text="📡 Lite Server",
            font_size='28sp',
            size_hint_y=0.08,
            color=self._hex_to_rgb(TEXT_WHITE),
            bold=True
        )
        root.add_widget(title)

        # === Статус ===
        self.status_label = Label(
            text="⏹ Сервер остановлен",
            font_size='18sp',
            size_hint_y=0.06,
            color=self._hex_to_rgb(TEXT_GRAY)
        )
        root.add_widget(self.status_label)

        # === IP адрес ===
        self.ip_label = Label(
            text=f"IP: {get_local_ip()}",
            font_size='16sp',
            size_hint_y=0.05,
            color=self._hex_to_rgb(TEXT_GREEN)
        )
        root.add_widget(self.ip_label)

        # === Папка ===
        folder_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.08,
            spacing=10
        )

        self.folder_input = TextInput(
            text=self.serve_dir,
            multiline=False,
            font_size='14sp',
            size_hint_x=0.7,
            background_color=self._hex_to_rgb(BG_CARD),
            foreground_color=self._hex_to_rgb(TEXT_WHITE),
            cursor_color=self._hex_to_rgb(TEXT_WHITE)
        )
        folder_box.add_widget(self.folder_input)

        btn_browse = Button(
            text="📂 Папка",
            size_hint_x=0.3,
            background_color=self._hex_to_rgb(ACCENT),
            color=self._hex_to_rgb(TEXT_WHITE),
            font_size='14sp'
        )
        btn_browse.bind(on_press=self.show_folder_chooser)
        folder_box.add_widget(btn_browse)

        root.add_widget(folder_box)

        # === Порт ===
        port_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.08,
            spacing=10
        )

        port_label = Label(
            text="Порт:",
            font_size='16sp',
            size_hint_x=0.2,
            color=self._hex_to_rgb(TEXT_GRAY)
        )
        port_box.add_widget(port_label)

        self.port_input = TextInput(
            text=str(self.port),
            multiline=False,
            font_size='16sp',
            size_hint_x=0.3,
            input_filter='int',
            background_color=self._hex_to_rgb(BG_CARD),
            foreground_color=self._hex_to_rgb(TEXT_WHITE),
            cursor_color=self._hex_to_rgb(TEXT_WHITE)
        )
        port_box.add_widget(self.port_input)

        root.add_widget(port_box)

        # === Кнопка Старт/Стоп ===
        self.btn_toggle = Button(
            text="▶  ЗАПУСТИТЬ СЕРВЕР",
            size_hint_y=0.12,
            background_color=self._hex_to_rgb(TEXT_GREEN),
            color=self._hex_to_rgb(TEXT_WHITE),
            font_size='20sp',
            bold=True
        )
        self.btn_toggle.bind(on_press=self.toggle_server)
        root.add_widget(self.btn_toggle)

        # === Кнопка "Открыть в браузере" ===
        self.btn_browser = Button(
            text="🌐 Открыть в браузере",
            size_hint_y=0.08,
            background_color=self._hex_to_rgb(ACCENT),
            color=self._hex_to_rgb(TEXT_WHITE),
            font_size='16sp',
            disabled=True
        )
        self.btn_browser.bind(on_press=self.open_in_browser)
        root.add_widget(self.btn_browser)

        # === Кнопка "Открыть WebView" ===
        self.btn_webview = Button(
            text="📱 Открыть внутри",
            size_hint_y=0.08,
            background_color=self._hex_to_rgb(ACCENT),
            color=self._hex_to_rgb(TEXT_WHITE),
            font_size='16sp',
            disabled=True
        )
        self.btn_webview.bind(on_press=self.open_webview)
        root.add_widget(self.btn_webview)

        # === Лог ===
        log_label = Label(
            text="📋 Лог:",
            font_size='14sp',
            size_hint_y=0.04,
            color=self._hex_to_rgb(TEXT_GRAY),
            halign='left',
            valign='bottom'
        )
        root.add_widget(log_label)

        scroll = ScrollView(size_hint_y=0.25)
        self.log_label = Label(
            text="Готов к запуску...",
            font_size='12sp',
            color=self._hex_to_rgb(TEXT_GRAY),
            halign='left',
            valign='top',
            size_hint_y=None
        )
        self.log_label.bind(
            width=lambda *x: setattr(self.log_label, 'text_size', (self.log_label.width, None))
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        scroll.add_widget(self.log_label)
        root.add_widget(scroll)

        # Обновление IP
        Clock.schedule_interval(self.update_ip, 5)

        return root

    def _hex_to_rgb(self, hex_color):
        """Конвертировать hex в RGB tuple (0-1)"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def log(self, msg):
        """Добавить сообщение в лог"""
        current = self.log_label.text
        lines = current.split('\n')
        if len(lines) > 50:
            lines = lines[-50:]
        lines.append(msg)
        self.log_label.text = '\n'.join(lines)

    def update_ip(self, dt=None):
        """Обновить IP адрес"""
        ip = get_local_ip()
        self.ip_label.text = f"IP: {ip}"

    def show_folder_chooser(self, instance):
        """Показать выбор папки"""
        content = BoxLayout(orientation='vertical', spacing=10)
        
        fc = FileChooserListView(
            path=self.serve_dir,
            dirselect=True,
            fileselect=False
        )
        content.add_widget(fc)

        btn_box = BoxLayout(
            size_hint_y=0.15,
            spacing=10
        )

        btn_cancel = Button(
            text="Отмена",
            background_color=self._hex_to_rgb(TEXT_RED),
            color=self._hex_to_rgb(TEXT_WHITE)
        )
        btn_select = Button(
            text="✅ Выбрать",
            background_color=self._hex_to_rgb(TEXT_GREEN),
            color=self._hex_to_rgb(TEXT_WHITE)
        )

        popup = Popup(
            title="Выберите папку",
            content=content,
            size_hint=(0.95, 0.9),
            background_color=self._hex_to_rgb(BG_DARK)
        )

        def select_folder(instance):
            selection = fc.selection
            if selection:
                self.serve_dir = selection[0]
                self.folder_input.text = self.serve_dir
                self.log(f"📁 Папка: {self.serve_dir}")
            popup.dismiss()

        def cancel(instance):
            popup.dismiss()

        btn_select.bind(on_press=select_folder)
        btn_cancel.bind(on_press=cancel)
        btn_box.add_widget(btn_cancel)
        btn_box.add_widget(btn_select)
        content.add_widget(btn_box)

        popup.open()

    def toggle_server(self, instance):
        """Запуск/остановка сервера"""
        if self.server_running:
            self.stop_server()
        else:
            self.start_server()

    def start_server(self):
        """Запустить HTTP-сервер"""
        self.serve_dir = self.folder_input.text.strip()
        try:
            self.port = int(self.port_input.text.strip())
        except ValueError:
            self.port = 8080

        if not os.path.isdir(self.serve_dir):
            self.log("❌ Папка не найдена!")
            return

        try:
            self.server_thread = ServerThread(self.serve_dir, self.port)
            self.server_thread.start()
            self.server_running = True

            ip = get_local_ip()
            self.status_label.text = "🟢 Сервер работает"
            self.status_label.color = self._hex_to_rgb(TEXT_GREEN)
            self.btn_toggle.text = "⏹  ОСТАНОВИТЬ"
            self.btn_toggle.background_color = self._hex_to_rgb(TEXT_RED)
            self.btn_browser.disabled = False
            self.btn_webview.disabled = False

            self.log(f"✅ Сервер запущен на {ip}:{self.port}")
            self.log(f"📁 Папка: {self.serve_dir}")
            self.log(f"🔗 http://{ip}:{self.port}")

        except Exception as e:
            self.log(f"❌ Ошибка: {e}")

    def stop_server(self):
        """Остановить HTTP-сервер"""
        if self.server_thread:
            self.server_thread.stop()
            self.server_thread = None

        self.server_running = False
        self.status_label.text = "⏹ Сервер остановлен"
        self.status_label.color = self._hex_to_rgb(TEXT_GRAY)
        self.btn_toggle.text = "▶  ЗАПУСТИТЬ СЕРВЕР"
        self.btn_toggle.background_color = self._hex_to_rgb(TEXT_GREEN)
        self.btn_browser.disabled = True
        self.btn_webview.disabled = True

        self.log("⏹ Сервер остановлен")

    def open_in_browser(self, instance):
        """Открыть в браузере"""
        ip = get_local_ip()
        url = f"http://{ip}:{self.port}"
        self.log(f"🌐 Открытие: {url}")

        try:
            if platform == 'android':
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                
                intent = Intent()
                intent.setAction(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(url))
                currentActivity = PythonActivity.mActivity
                currentActivity.startActivity(intent)
            else:
                import webbrowser
                webbrowser.open(url)
        except Exception as e:
            self.log(f"❌ Не удалось открыть: {e}")

    def open_webview(self, instance):
        """Открыть встроенный WebView"""
        ip = get_local_ip()
        url = f"http://{ip}:{self.port}"
        self.log(f"📱 WebView: {url}")

        try:
            if platform == 'android':
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                
                intent = Intent()
                intent.setAction(Intent.ACTION_VIEW)
                intent.setData(Uri.parse(url))
                currentActivity = PythonActivity.mActivity
                currentActivity.startActivity(intent)
            else:
                import webbrowser
                webbrowser.open(url)
        except Exception as e:
            self.log(f"❌ WebView ошибка: {e}")

    def on_stop(self):
        """При закрытии приложения"""
        self.stop_server()


if __name__ == '__main__':
    LiteServerApp().run()
