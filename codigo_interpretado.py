NumeroUno = None
NumeroDos = None
NumeroUno = 670
NumeroDos = 670
Cond = None
Cond = 670 > 670
if Cond:
	Texto = None
	Texto = "Numero Uno es mayo a Numero Dos"
	with open('output.txt', 'w') as archivo:
		archivo.write(str(Texto))
else:
	Cond = 670 == 670
	if Cond:
		Texto = None
		Texto = "Numero Uno es igual a Numero Dos"
		with open('output.txt', 'w') as archivo:
			archivo.write(str(Texto))
	else:
		Texto = None
		Texto = "Numero Uno es menor a Numero Dos"
		with open('output.txt', 'w') as archivo:
			archivo.write(str(Texto))
