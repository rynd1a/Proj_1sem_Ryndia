# Вариант 21
# Описать функцию Power1(A, B) вещественного типа, находящую величину AB по формуле
# AB = exp(B*ln(A)) (параметры A и B — вещественные). В случае нулевого или
# отрицательного параметра A функция возвращает 0. С помощью этой функции найти
# степени AP, BP, CP, если даны числа P, A, B, C.

def Power1(A, B):
    if A <= 0:
        return 0
    else:
        AB = A ** B
        return AB


P = int(input("Введите степень, в которую хотите возвести число: "))
A = int(input("Введите первое число: "))
B = int(input("Введите второе число: "))
C = int(input("Введите третье число: "))

step1 = Power1(A, P)
step2 = Power1(B, P)
step3 = Power1(C, P)

print(A, "в степени", f"{P}:", step1)
print(B, "в степени", f"{P}:", step2)
print(C, "в степени", f"{P}:", step3)