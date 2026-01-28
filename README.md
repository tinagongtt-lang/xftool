# 🚀 xftool (v0.7.4)
## 专为多系统原生渲染设计的通用工具箱。

xftool 是一个高性能的 Python 库，旨在为开发者提供高精度的数学计算以及跨平台、零依赖的原生图形渲染能力。无论你是在 Linux、Windows 还是 MacOS，xftool 都能自动感应环境并建立通信。
## 🌌 核心特性
 - 多系统环境感应 (Multi-OS Sensing)：

   -  **Linux**: 深度集成原生 X11 API。

   - **Windows**: 直接驱动 Win32 GDI 渲染引擎。

   - **MacOS**: 建立与 Cocoa (AppKit) 框架的底层桥接。

- **零依赖几何引擎 (Zero-Dep Graphics)**：无需安装庞大的 GUI 框架，直接通过 ctypes 调用硬件接口，支持绘制：

 - `triangle` (三角形)

 - `square` (正方形)

 - `rectangle` (长方形)
 - `circle` （圆形）

- **高精度数学 (xmath)**：利用 gmpy2 提供超越常规精度的计算能力。

## 🛠️ 安装指南
Linux 用户
在使用图形功能前，请确保安装了 X11 开发库：
```bash
sudo apt update && sudo apt install libx11-dev
```
##### 全系统安装
先去[Releases](https://github.com/tinagongtt-lang/xftool/releases "Releases")下载whl包
```bash
pip install xftool-0.4-py3-none-any.whl
```

## 🚀 快速上手
使用 v0.7 最新的 xfX11 模块，只需几行代码即可创建原生窗口并绘图：

```python
import xftool.xfX11 as x11

# 1. 初始化引擎（自动感应当前操作系统）
tool = x11.X11()

# 2. 创建导航窗口 (宽度, 高度, 标题)
dis = tool.display(1024, 768, title="xftool Galactic Navigator")

# 3. 绘制星际几何图形 (图形名称, 大小)
dis.draw("triangle", 200)      # 绘制三角形
dis.draw("square", 150)        # 绘制正方形
dis.draw("rectangle", (300, 50)) # 绘制长方形
dis.draw("circle", 150) # 绘制圆形
done() # 主循环
```
## 📜 许可证
本项目基于 MIT 协议开源。