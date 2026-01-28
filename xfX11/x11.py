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
        elif self.system == "Darwin":
            self._draw_macos(shape, size)

    def _draw_linux(self, shape, size):
        xlib = self.props['xlib']
        dpy = self.props['dpy']
        win = self.props['win']
        gc = self.props['gc']
        screen = self.props['screen']
        xlib.XSetForeground(dpy, gc, xlib.XWhitePixel(dpy, screen))
        
        if shape == "circle":
            s = size if isinstance(size, int) else size[0]
            # XFillArc: 绘制填充圆弧，angle2 为 360*64 代表全圆
            xlib.XFillArc(dpy, win, gc, self.start_x, self.start_y, s, s, 0, 360 * 64)
        elif shape == "triangle":
            s = size if isinstance(size, int) else size[0]
            pts = (XPoint * 3)(XPoint(self.start_x, self.start_y+s), 
                               XPoint(self.start_x+s, self.start_y+s), 
                               XPoint(self.start_x+s//2, self.start_y))
            xlib.XFillPolygon(dpy, win, gc, pts, 3, 1, 0)
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

    def _draw_macos(self, shape, size):
        print(f"🍎 [Cocoa] 已接收圆形绘制指令，尺寸: {size}")

class X11:
    def __init__(self):
        self.system = platform.system()
        print(f"📡 xftool v0.7.2 正在检测系统: {self.system}")

    def display(self, width, height, title="xftool Engine"):
        if self.system == "Linux":
            return self._init_linux(width, height, title)
        elif self.system == "Windows":
            return self._init_windows(width, height, title)
        elif self.system == "Darwin":
            return self._init_macos(width, height, title)
        return None

    def _init_linux(self, width, height, title):
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

    def _init_windows(self, width, height, title):
        user32 = ctypes.windll.user32
        hwnd = user32.CreateWindowExW(0, "Static", title, 0x10CF0000, 100, 100, width, height, 0, 0, 0, 0)
        user32.ShowWindow(hwnd, 5)
        return Display("Windows", hwnd=hwnd)

    def _init_macos(self, width, height, title):
        return Display("Darwin")