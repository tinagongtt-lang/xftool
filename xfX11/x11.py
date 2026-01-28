import ctypes
import sys
import os
import time
from ctypes import util

# --- 自动探测系统库 ---
def _check_x11_libraries():
    lib_name = util.find_library("X11")
    if not lib_name:
        potential_paths = [
            "/usr/lib/x86_64-linux-gnu/libX11.so.6",
            "/usr/lib/libX11.so.6",
            "/usr/lib/x86_64-linux-gnu/libX11.so"
        ]
        for path in potential_paths:
            if os.path.exists(path): return path
        return None
    return lib_name

# --- X11 坐标点结构体 ---
class XPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_short), ("y", ctypes.c_short)]

class Display:
    """
    绘图引擎类：负责在窗口内绘制几何图形
    """
    def __init__(self, xlib, dpy, win, gc, screen):
        self.xlib = xlib
        self.dpy = dpy
        self.win = win
        self.gc = gc
        self.screen = screen

    def draw(self, shape, size):
        """
        2. 图形创建：支持 triangle, square, rectangle
        size: 可以是整数（边长）或元组 (width, height)
        """
        # 设置白色画笔
        white = self.xlib.XWhitePixel(self.dpy, self.screen)
        self.xlib.XSetForeground(self.dpy, self.gc, white)

        # 默认绘图起点
        start_x, start_y = 150, 150

        shape = shape.lower()
        if shape == "triangle":
            s = size if isinstance(size, int) else size[0]
            # 定义三角形顶点
            points = (XPoint * 3)(
                XPoint(start_x, start_y), 
                XPoint(start_x + s, start_y), 
                XPoint(start_x + s // 2, start_y - int(s * 0.866))
            )
            # 绘制实心多边形
            self.xlib.XFillPolygon(self.dpy, self.win, self.gc, points, 3, 1, 0)
            print(f"📐 Drawing Triangle, size: {s}")

        elif shape == "square":
            s = size if isinstance(size, int) else size[0]
            self.xlib.XFillRectangle(self.dpy, self.win, self.gc, start_x, start_y, s, s)
            print(f"⬜ Drawing Square, size: {s}")

        elif shape == "rectangle":
            w, h = (size, size) if isinstance(size, int) else size
            self.xlib.XFillRectangle(self.dpy, self.win, self.gc, start_x, start_y, w, h)
            print(f"▭ Drawing Rectangle, size: {w}x{h}")
        
        else:
            print(f"⚠️ Unknown shape: {shape}. Use 'triangle', 'square', or 'rectangle'.")

        self.xlib.XFlush(self.dpy)

class X11:
    def __init__(self):
        self.lib_path = _check_x11_libraries()
        if not self.lib_path:
            print("\n❌ 缺失系统依赖: libx11-dev\n")
            sys.exit(1)
        
        self.xlib = ctypes.cdll.LoadLibrary(self.lib_path)
        self.dpy = None

    def display(self, width, height, title="xftool Engine"):
        """创建窗口并返回绘图对象"""
        self.dpy = self.xlib.XOpenDisplay(None)
        if not self.dpy:
            print("❌ 无法连接到 X Server")
            return None

        screen = self.xlib.XDefaultScreen(self.dpy)
        root = self.xlib.XRootWindow(self.dpy, screen)
        black = self.xlib.XBlackPixel(self.dpy, screen)
        
        # 创建窗口与 GC
        win = self.xlib.XCreateSimpleWindow(self.dpy, root, 0, 0, width, height, 1, black, black)
        gc = self.xlib.XCreateGC(self.dpy, win, 0, None)

        self.xlib.XStoreName(self.dpy, win, title.encode('utf-8'))
        self.xlib.XMapWindow(self.dpy, win)
        self.xlib.XFlush(self.dpy)
        
        print(f"🚀 xftool Display active: {width}x{height}")
        return Display(self.xlib, self.dpy, win, gc, screen)