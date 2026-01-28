import ctypes
import sys
import os
import time
from ctypes import util

def _check_x11_libraries():
    """探测系统中的 libX11.so"""
    lib_name = util.find_library("X11")
    if not lib_name:
        potential_paths = [
            "/usr/lib/x86_64-linux-gnu/libX11.so.6",
            "/usr/lib64/libX11.so.6",
            "/usr/lib/libX11.so.6",
            "/usr/lib/x86_64-linux-gnu/libX11.so"
        ]
        for path in potential_paths:
            if os.path.exists(path):
                return path
        return None
    return lib_name

class X11:
    def __init__(self):
        self.lib_path = _check_x11_libraries()
        self.display_ptr = None
        self.window = None
        
        # 依赖自检提示
        if not self.lib_path:
            print("\n" + "!"*60)
            print("🚀 xftool 系统环境检查未通过！")
            print("检测到缺失关键组件: libX11-dev")
            print("-" * 60)
            print("💡 请执行以下命令安装：")
            print("   sudo apt update && sudo apt install libx11-dev")
            print("-" * 60)
            sys.exit(1)

        self.xlib = ctypes.cdll.LoadLibrary(self.lib_path)

    def display(self, width=800, height=600, title="xftool Navigator"):
        """创建并显示 X11 窗口"""
        self.display_ptr = self.xlib.XOpenDisplay(None)
        if not self.display_ptr:
            print("❌ 无法连接到 X Server。")
            return

        screen = self.xlib.XDefaultScreen(self.display_ptr)
        root = self.xlib.XRootWindow(self.display_ptr, screen)
        black = self.xlib.XBlackPixel(self.display_ptr, screen)
        
        self.window = self.xlib.XCreateSimpleWindow(
            self.display_ptr, root, 0, 0, width, height, 1, black, black
        )

        self.xlib.XStoreName(self.display_ptr, self.window, title.encode('utf-8'))
        self.xlib.XMapWindow(self.display_ptr, self.window)
        self.xlib.XFlush(self.display_ptr)
        
        print(f"✅ xftool 窗口已创建: {width}x{height}")

        try:
            while True:
                self.xlib.XFlush(self.display_ptr)
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.close()

    def close(self):
        if self.display_ptr and self.window:
            self.xlib.XDestroyWindow(self.display_ptr, self.window)
            self.xlib.XCloseDisplay(self.display_ptr)
            print("🛑 X11 已断开。")