import gmpy2
import random
from gmpy2 import mpfr, mpz, mpc
def pi(digits=100):
    """计算高精度 Pi"""
    prec = int(digits * 3.322) + 64
    gmpy2.get_context().precision = prec
    
    C1, C2, C3 = 13591409, 545140134, 640320
    C3_3 = C3**3 // 24

    def bsplit(a, b):
        if b - a == 1:
            if a == 0:
                P = Q = mpz(1)
            else:
                P = mpz((6*a-5)*(2*a-1)*(6*a-1))
                Q = mpz(a**3 * C3_3)
            T = mpz(P * (C1 + a*C2))
            if a % 2 == 1: T = -T
            return P, Q, T
        else:
            mid = (a + b) // 2
            P1, Q1, T1 = bsplit(a, mid)
            P2, Q2, T2 = bsplit(mid, b)
            return P1*P2, Q1*Q2, Q2*T1 + P1*T2

    n = int(digits / 14.18) + 1
    P, Q, T = bsplit(0, n)
    sqrt_C3 = gmpy2.sqrt(mpfr(10005))
    return (mpfr(426880) * sqrt_C3 * Q) / T

class Constants:
    # --- 基础常数 ---
    # 使用你 v0.3 里的 pi(100) 来确保 Degree 的超高精度
    PI = pi(100)
    
    # Degree: 1度对应的弧度值 (pi / 180)
    DEGREE = PI / 180
    
    # --- 物理与天文常数 ---
    C = mpfr('299792458')
    G = mpfr('6.67430e-11')
    AU = mpfr('149597870700')
    EARTH_MASS = mpfr('5.9722e24')
    EARTH_RADIUS = mpfr('6371000')

# 快捷转换工具函数 (可以加在 functions.py 里)
def to_radians(deg):
    return deg * Constants.DEGREE

def to_degrees(rad):
    return rad / Constants.DEGREE
# ==========================================
# 1. 核心精度设置 (128位精度，约 38 位有效数字)
# ==========================================
gmpy2.get_context().precision = 128

# ==========================================
# 2. 圆周率 Pi (Chudnovsky 算法 - 二分递归版)
# ==========================================

# ==========================================
# 3. 反三角函数与级数展开
# ==========================================
def arctan(x, j=50):
    """ArcTan[x] 展开 (适用于 |x| < 1)"""
    x = mpfr(x)
    result = mpfr(0)
    for i in range(j):
        term = ((-1)**i) * (x**(2*i+1)) / (2*i+1)
        result += term
    return result

def arcsin(x, j=50):
    """ArcSin[x] 展开"""
    x = mpfr(x)
    res = x
    num, den = mpz(1), mpz(2)
    for i in range(1, j):
        p = 2 * i + 1
        res += (mpfr(num)/den) * (x**p) / p
        num *= (2*i + 1)
        den *= (2*i + 2)
    return res

def arccos(x, j=50):
    """ArcCos[x] = Pi/2 - ArcSin[x]"""
    return (pi(50) / 2) - arcsin(x, j)

# ==========================================
# 4. 基础工具与数论函数
# ==========================================
def factorial(n):
    """n! 阶乘"""
    return gmpy2.fac(int(n))

def abs_val(x):
    """Abs[x] 绝对值"""
    return abs(mpfr(x))

def round_val(x):
    """Round[x] 最近整数"""
    return int(gmpy2.rint(mpfr(x)))

def mod_val(n, m):
    """Mod[n, m] 模除"""
    return mpz(n) % mpz(m)

def factor_integer(n):
    """FactorInteger[n] 素数因子分解"""
    factors = []
    d, temp = 2, mpz(n)
    while d * d <= temp:
        while (temp % d) == 0:
            factors.append(int(d))
            temp //= d
        d += 1
    if temp > 1: factors.append(int(temp))
    return factors

# ==========================================
# 5. 辅助工具 (Random, Max, Min)
# ==========================================
def random_real():
    """RandomReal[] 0-1 随机数"""
    return random.random()

def max_val(*args):
    """Max[x, y, ...]"""
    return max(args)

def min_val(*args):
    """Min[x, y, ...]"""
    return min(args)