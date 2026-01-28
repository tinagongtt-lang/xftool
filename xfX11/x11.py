import ctypes
import sys
import os
import platform
import time
from ctypes import util

# --- 跨平台结构体定义 ---
class XPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_short), ("y", ctypes.c_short)]

class Display:
    """
    统一绘图引擎：支持 'triangle', 'square', 'rectangle', 'circle'
    新增 'done()' 方法用于维持窗口状态
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

    def done(self):
        """
        🚀 核心更新：进入事件循环，防止窗口闪退
        """
        print(f"⏳ [{self.system}] 绘图完成。窗口已锁定，请手动关闭窗口以退出程序。")
        
        if self.system == "Linux":
            xlib = self.props['xlib']
            dpy = self.props['dpy']
            # 创建一个足够大的缓冲区来接收 XEvent 结构体
            event = (ctypes.c_char * 96)() 
            while True:
                xlib.XNextEvent(dpy, event)
                # 此时窗口会保持响应，不再闪退
                
        elif self.system == "Windows":
            user32 = ctypes.windll.user32
            msg = ctypes.wintypes.MSG()
            # 标准 Win32 消息循环
            while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))

    def _draw_linux(self, shape, size):
        xlib = self.props['xlib']
        dpy = self.props['dpy']
        win = self.props['win']
        gc = self.props['gc']
        screen = self.props['screen']
        xlib.XSetForeground(dpy, gc, xlib.XWhitePixel(dpy, screen))
        
        if shape == "circle":
            s = size if isinstance(size, int) else size[0]
            xlib.XFillArc(dpy, win, gc, self.start_x, self.start_y, s, s, 0, 360 * 64)
        elif shape in ["square", "rectangle"]:
            w, h = (size, size) if isinstance(size, int) else size
            xlib.XFillRectangle(dpy, win, gc, self.start_x, self.start_y, w, h)
        xlib.XFlush(dpy)

    def _draw_windows(self, shape, size):
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        hwnd = self.props['hwnd']
        hdc = user32.GetDC(hwnd)
        brush = gdi32.CreateSolidBrush(0xFFFFFF)
        old_brush = gdi32.SelectObject(hdc, brush)
        
        if shape == "circle":
            s = size if isinstance(size, int) else size[0]
            gdi32.Ellipse(hdc, self.start_x, self.start_y, self.start_x + s, self.start_y + s)
        elif shape in ["square", "rectangle"]:
            w, h = (size, size) if isinstance(size, int) else size
            rect = ctypes.wintypes.RECT(self.start_x, self.start_y, self.start_x + w, self.start_y + h)
            user32.FillRect(hdc, ctypes.byref(rect), brush)
            
        gdi32.SelectObject(hdc, old_brush)
        gdi32.DeleteObject(brush)
        user32.ReleaseDC(hwnd, hdc)

class X11:
    def __init__(self):
        self.system = platform.system()
        print(f"📡 xftool v0.7.3 系统感应: {self.system}")

    def display(self, width, height, title="xftool Engine"):
        if self.system == "Linux":
            lib = util.find_library("X11") or "/usr/lib/libX11.so.6"
            xlib = ctypes.cdll.LoadLibrary(lib)
            dpy = xlib.XOpenDisplay(None)
            win = xlib.XCreateSimpleWindow(dpy, xlib.XRootWindow(dpy, xlib.XDefaultScreen(dpy)), 
                                       0, 0, width, height, 1, 0, 0)
            gc = xlib.XCreateGC(dpy, win, 0, None)
            xlib.XStoreName(dpy, win, title.encode('utf-8'))
            xlib.XMapWindow(dpy, win)
            xlib.XFlush(dpy)
            return Display("Linux", xlib=xlib, dpy=dpy, win=win, gc=gc, screen=xlib.XDefaultScreen(dpy))
        
        elif self.system == "Windows":
            user32 = ctypes.windll.user32
            hwnd = user32.CreateWindowExW(0, "Static", title, 0x10CF0000, 100, 100, width, height, 0, 0, 0, 0)
            user32.ShowWindow(hwnd, 5)
            return Display("Windows", hwnd=hwnd)
        
        return None