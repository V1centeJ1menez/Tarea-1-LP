Largo = None
Ancho = None
Area = None
Texto = None
Largo = 6
Ancho = 5
Area = 6 * 5
Texto = "La altura del rectangulo es "
Texto = str("La altura del rectangulo es ") + str(30)
with open('output.txt', 'w') as archivo:
	archivo.write(str(Texto))
