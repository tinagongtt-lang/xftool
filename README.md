🚀 xftool (v0.4)
一个专为星际计算设计的高精度数学工具箱。本项目通过 gmpy2 提供了超越标准浮点数（Float64）的数值精度，适用于天文轨道计算、高精度物理模拟等场景。

📜 授权 (License)
本项目采用 MIT License。你可以自由使用、修改和分发，但请保留作者 tinagongtt-lang 的署名。
## 🛠️ 系统依赖 (System Dependencies)
由于 `xfX11` 模块直接调用 Linux 底层 API，请在安装前确保系统已安装 X11 开发库：

```bash
sudo apt update && sudo apt install libx11-dev
```

🛠️ 安装方法 (Installation)
先去Releases下载whl包
```bash
pip install xftool-0.4-py3-none-any.whl
```
📖 快速上手 (Quick Usage)
安装完成后，你可以在任何 Python 环境中直接调用 xmath 模块。

1. 高精度圆周率与天文常数

```python
from xmath.functions import pi.Constants

# 计算 100 位精度的 Pi
print(f"Pi (100 digits): {pi(100)}")

# 获取天文常数 (基于 128 位精度)
print(f"万有引力常数 G: {Constants.G}")
print(f"天文单位 AU: {Constants.AU}")
```
2. 角度转换与反三角函数

```python
from xmath.functions import to_radians, arctan

# 角度转弧度
rad = to_radians(45.0)
print(f"45 degrees in radians: {rad}")

# 使用级数展开计算 ArcTan
print(f"ArcTan(0.5): {arctan(0.5)}")
```
3. 数论工具

```python
from xmath.functions import factor_integer, factorial

# 素因子分解
print(f"Factor 2026: {factor_integer(2026)}")

# 计算大数阶乘
print(f"Factorial 100: {factorial(100)}")
```
🧠 核心逻辑实现 (Implementation Reference)
本工具箱的核心算法（如 Chudnovsky 算法、级数展开等）已在源代码中完整实现。详细代码逻辑请参考 xmath/functions.py。