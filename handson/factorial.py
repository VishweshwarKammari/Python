def factorial(n):
    total = 1
    for i in range(1, n + 1):
        total *= i
    return total


if __name__ == '__main__':
    n = int(input())
    res = factorial(n)
    print(res)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
