import math
f = lambda x: math.exp(-x) - x
df = lambda x: -math.exp(-x) - 1

def newton(f, df, x0, epsilon):
    x_i = x0
    fx_i = f(x0)
    while abs(fx_i) > epsilon:
        dfx_i = df(x_i)
        x_i = x_i - fx_i/dfx_i
        fx_i = f(x_i)
    return x_i

newton(f, df, 1, 1e-8)

