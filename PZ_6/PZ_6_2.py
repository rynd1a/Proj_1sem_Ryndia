# Вариант 21.
# Дан целочисленный список размера N. Если он является перестановкой, то есть
# содержит все числа от 1 до N, то вывести 0; в противном случае вывести номер первого
# недопустимого элемента.

a = list(map(int, input("Введите целые числа через пробел: ").split()))
A = sorted(a)

N = len(a)

for i in range(1, N + 1):
    if i != A[i - 1]:
        break

if i == N:
    print("0")
else:
    for i in range(1, N + 1):
        if i != a[i - 1]:
            print("Номер первого недопустимого элемента: ", a[i - 1])
            break