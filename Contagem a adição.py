portas = [21, 22, 23, 25, 80, 443, 8080]
portas_altas = []

for i in portas:
    if i >100:
        portas_altas.append(i)
        print(portas_altas)
