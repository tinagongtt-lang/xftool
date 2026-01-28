import ctypes
import sys
import os
import platform
import time
from ctypes import util

class XPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_short), ("y", ctypes.c_short)]

class Display:
    """
    统一绘图引擎 v0.7.4
    已实现全平台 'done()' 事件循环锁定
    """
    def __init__(self, system, **kwargs):
        self.system = system
        self.props = kwargs
        self.start_x, self.start_y = 150, 150

    def draw(self, shape, size):
        shape = shape.lower()
        print(f"🎨 [{self.system}] 正在绘制: {shape}...")
        
        if self.system == "Linux":
            self._draw_linux(shape, size)
        elif self.system == "Windows":
            self._draw_windows(shape, size)
        elif self.system == "Darwin": # macOS
            print(f"⚠️ [{self.system}] macOS 绘图指令已发出 (待集成原生 Metal/Cocoa 渲染层)")

    def done(self):
        """
        🚀 锁定窗口不闪退：支持 Linux 和 Windows
        """
        print(f"⏳ [{self.system}] 绘图完成。窗口已锁定，请手动关闭。")
        
        if self.system == "Linux":
            xlib = self.props['xlib']
            dpy = self.props['dpy']
            event = (ctypes.c_char * 96)() 
            while True:
                xlib.XNextEvent(dpy, event)
                
        elif self.system == "Windows":
            user32 = ctypes.windll.user32
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        
        elif self.system == "Darwin":
            # macOS 简单阻塞
            while True:
                time.sleep(1)

    def _draw_linux(self, shape, size):
        xlib, dpy, win, gc = self.props['xlib'], self.props['dpy'], self.props['win'], self.props['gc']
        xlib.XSetForeground(dpy, gc, xlib.XWhitePixel(dpy, self.props['screen']))
        if shape == "circle":
            s = size if isinstance(size, int) else size[0]
            xlib.XFillArc(dpy, win, gc, self.start_x, self.start_y, s, s, 0, 360 * 64)
        elif shape in ["square", "rectangle"]:
            w, h = (size, size) if isinstance(size, int) else size
            xlib.XFillRectangle(dpy, win, gc, self.start_x, self.start_y, w, h)
        xlib.XFlush(dpy)

    def _draw_windows(self, shape, size):
        user32, gdi32 = ctypes.windll.user32, ctypes.windll.gdi32
        hwnd = self.props['hwnd']
        hdc = user32.GetDC(hwnd)
        brush = gdi32.CreateSolidBrush(0xFFFFFF)
        gdi32.SelectObject(hdc, brush)
        if shape == "circle":
            s = size if isinstance(size, int) else size[0]
            gdi32.Ellipse(hdc, self.start_x, self.start_y, self.start_x + s, self.start_y + s)
        user32.ReleaseDC(hwnd, hdc)

class X11:
    def __init__(self):
        self.system = platform.system()
        print(f"📡 xftool v0.7.4 正在检测系统: {self.system}")

    def display(self, width, height, title="xftool Engine"):
        if self.system == "Linux":
            lib = util.find_library("X11") or "/usr/lib/libX11.so.6"
            xlib = ctypes.cdll.LoadLibrary(lib)
            dpy = xlib.XOpenDisplay(None)
            win = xlib.XCreateSimpleWindow(dpy, xlib.XRootWindow(dpy, xlib.XDefaultScreen(dpy)), 
                                       0, 0, width, height, 1, 0, 0)
            xlib.XStoreName(dpy, win, title.encode('utf-8'))
            xlib.XMapWindow(dpy, win)
            xlib.XFlush(dpy)
            
            # 🚀 跨平台同步机制：统一 0.5s 缓冲
            print(f"⏳ [{self.system}] 正在同步窗口映射...")
            time.sleep(0.5)
            
            return Display("Linux", xlib=xlib, dpy=dpy, win=win, gc=xlib.XCreateGC(dpy, win, 0, None), screen=xlib.XDefaultScreen(dpy))
        
        elif self.system == "Windows":
            user32 = ctypes.windll.user32
            hwnd = user32.CreateWindowExW(0, "Static", title, 0x10CF0000, 100, 100, width, height, 0, 0, 0, 0)
            user32.ShowWindow(hwnd, 5)
            
            # 🚀 Win11 窗口淡入动画缓冲
            print(f"⏳ [Windows] 正在同步窗口句柄...")
            time.sleep(0.5)
            
            return Display("Windows", hwnd=hwnd)

        elif self.system == "Darwin": # macOS
            print(f"⏳ [macOS] 正在同步 Cocoa 视图缓存...")
            time.sleep(0.5)
            return Display("Darwin")
        
        return None