import customtkinter as ctk
import customtkinter as ctk
import psutil
import keyboard
import threading
import sys
import os
import ctypes
import socket

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

PORT = 47201
_global_lock_socket = None

def check_single_instance():
    global _global_lock_socket
    _global_lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        _global_lock_socket.bind(('127.0.0.1', PORT))
        _global_lock_socket.listen(5)
    except socket.error:
        try:
            with socket.create_connection(('127.0.0.1', PORT), timeout=0.5) as s:
                s.sendall(b'WAKE_UP')
        except: pass
        os._exit(0)

ctk.set_appearance_mode("Dark")

class AcerProcessManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Acer 进程管理")
        self.geometry("400x450")
        self.attributes("-topmost", True)
        self.configure(fg_color="#1A1A1A")
        

        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 33, ctypes.byref(ctypes.c_int(2)), 4)
        except: pass


        icon_path = resource_path("acer.ico")
        if HAS_PIL and os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except: pass

        self.target_name = "SduEdu.exe"
        self.is_hidden = False
        self.protocol('WM_DELETE_WINDOW', self.on_minimize)


        self.tabview = ctk.CTkTabview(self, fg_color="#242424", segmented_button_selected_color="#3498DB")
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.tab_main = self.tabview.add("控制中心")
        self.tab_about = self.tabview.add("关于")

        ctk.CTkLabel(self.tab_main, text="Acer 进程管理", font=("Microsoft YaHei", 20, "bold"), text_color="#3498DB").pack(pady=(20, 10))
        self.status_text = ctk.StringVar(value="状态：等待指令")
        ctk.CTkLabel(self.tab_main, textvariable=self.status_text, font=("Microsoft YaHei", 16)).pack(pady=10)
        
        ctk.CTkButton(self.tab_main, text="挂起进程 (F1)", command=self.suspend_proc, fg_color="#C0392B", hover_color="#E74C3C", height=40, width=200).pack(pady=15)
        ctk.CTkButton(self.tab_main, text="恢复进程 (F2)", command=self.resume_proc, fg_color="#27AE60", hover_color="#2ECC71", height=40, width=200).pack(pady=5)

        ctk.CTkLabel(self.tab_about, text="作者：小天不困.", font=("Microsoft YaHei", 22, "bold"), text_color="#3498DB").pack(pady=(50, 20))
        ctk.CTkLabel(self.tab_about, text="版本：V1.9", font=("Microsoft YaHei", 14)).pack(pady=5)
        ctk.CTkLabel(self.tab_about, text="热键绑定：\nF1 挂起 | F2 恢复\nF3 隐藏 | F4 退出", font=("Microsoft YaHei", 14), justify="center").pack(pady=30)

        self.setup_hotkeys()
        threading.Thread(target=self.listen_for_wakeup, daemon=True).start()

    def listen_for_wakeup(self):
        while True:
            try:
                conn, addr = _global_lock_socket.accept()
                with conn:
                    if conn.recv(1024) == b'WAKE_UP': self.after(0, self.on_restore)
            except: break

    def on_minimize(self):
        self.withdraw()
        self.is_hidden = True

    def on_restore(self):
        self.deiconify()
        self.state('normal')
        self.focus_force()
        self.is_hidden = False

    def setup_hotkeys(self):
        keyboard.add_hotkey('f1', self.suspend_proc)
        keyboard.add_hotkey('f2', self.resume_proc)
        keyboard.add_hotkey('f3', self.toggle_window)
        keyboard.add_hotkey('f4', lambda: os._exit(0))

    def toggle_window(self):
        if self.is_hidden: self.on_restore()
        else: self.on_minimize()

    def get_process(self):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() == self.target_name.lower(): return proc
        return None

    def suspend_proc(self):
        proc = self.get_process()
        if proc:
            try:
                proc.suspend()
                self.status_text.set("状态：已成功挂起")
            except: self.status_text.set("错误：权限不足")
        else: self.status_text.set("错误：未检测到目标")

    def resume_proc(self):
        proc = self.get_process()
        if proc:
            try:
                proc.resume()
                self.status_text.set("状态：已恢复正常运行")
            except: self.status_text.set("错误：无法恢复")

if __name__ == "__main__":
    check_single_instance()
    app = AcerProcessManager()
    app.mainloop()
