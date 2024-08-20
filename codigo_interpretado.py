Valor = None
Valor = 25
Texto = None
A = None
A = 25 > 30
if A:
	Texto = "El valor es mayor que 30"
	with open('output.txt', 'a') as archivo:
		archivo.write(str(Texto) + "\n")
else:
	A = 25 > 20
	if A:
		Texto = "El valor es mayor que 20 pero menor o igual a 30"
		Texto = str("El valor es mayor que 20 pero menor o igual a 30") + str(True)
		with open('output.txt', 'a') as archivo:
			archivo.write(str(Texto) + "\n")
	else:
		Texto = "El valor es 20 o menor"
		with open('output.txt', 'a') as archivo:
			archivo.write(str(Texto) + "\n")
