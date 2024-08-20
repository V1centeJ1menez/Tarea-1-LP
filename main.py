from Interprete import analizar_sintaxis, inicializar_archivo


def main():
    '''
        ***
        Parametros:
        None
        ***
        Retorno: None
        ***
        La función main es el punto de entrada del programa. Lee el contenido del archivo 
        `codigo.txt`, que contiene el código fuente a interpretar, y lo procesa mediante
        la función `analizar_sintaxis` para posteriormente generar el código Python
        correspondiente.

        La función primero inicializa el archivo de salida `codigo_interpretado.py` para 
        asegurarse de que esté vacío. Luego, analiza la sintaxis del código fuente con un 
        límite de anidamiento definido, y finalmente genera y ejecuta el código interpretado.
        No retorna ningún valor (None).
        ***
    ''' 
    with open("./codigos/codigo.txt", 'r') as archivo:
        contenido = archivo.read()

    # Analizar con un límite de 4 niveles de anidamiento
    inicializar_archivo()
    analizar_sintaxis(contenido, 4)


    #Leer y ejecutar el contenido del archivo
    with open("codigo_interpretado.py", 'r') as archivo:
        contenido = archivo.read()
    exec(contenido)


if __name__ == "__main__":
    main()