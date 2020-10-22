class Leaf:
    def __init__(self, a):
        self.a = a

    def sum(self):
        return self.a


class Composite:

    def __init__(self, ad: list):
        self.ad = ad

    def sum(self):
        result = 0
        for item in self.ad:
            result += item.sum()
        return result


# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
# 1 2 3 4 5
# 1 5 8 9 12
V = [0, 1, 5, 8, 9, 12]
F = [0]
N = 10
x = [i for i in range(N + 1)]
for i in range(1, N + 1, 1):
    _max = 0
    for j in range(1, i, 1):
        if _max < F[i - j] + F[j]:
            _max = F[i - j] + F[j]
    if i > 5:
        F.append(_max)
    else:
        F.append(max(_max, V[i]))
print(x)
print(F)
