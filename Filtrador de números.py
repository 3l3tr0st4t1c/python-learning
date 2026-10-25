payload = "A1B2C3D4"
contador = 0

for char in payload:
  if char.isdigit() and int(char) % 2 == 0:
      contador +=1
      print(contador)
