Var = None
Cond = None
Var = 1
Cond = 1 == 1
with open("output.txt", "a") as archivo:
	archivo.write(str(Var) + "\n")
if Cond:
	Var = None
	Var = 2
	with open("output.txt", "a") as archivo:
		archivo.write(str(Var) + "\n")
	if Cond:
		Var = None
		Var = "HOLA"
		with open("output.txt", "a") as archivo:
			archivo.write(str(Var) + "\n")
		Var = 2
	else:
		pass
	Var = 1
else:
	Var = None
	Var = " ELSE"
	with open("output.txt", "a") as archivo:
		archivo.write(str(Var) + "\n")
	Var = 1
with open("output.txt", "a") as archivo:
	archivo.write(str(Var) + "\n")
