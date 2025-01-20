def decorator(x):
    def wrapper(func):
        def inner(*args, **kwargs):
            print(f"{x=}")
            res = func(*args, **kwargs)
            return res
        return inner
    return wrapper

@decorator("MIR")
def func1(c, b):
    return c + b

print(func1(200, 400))

