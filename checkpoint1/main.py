from polynomial import Polynomial

def test():
    a = Polynomial([2, 0, 4, -1, 0, 6])
    b = Polynomial([-1, -3, 0, 4.5])

    print(a.order())
    print(a+b)
    derivative = a.derivative()
    print(derivative)
    print(derivative.indefinite_integral(2))

if __name__ == "__main__":
    test()