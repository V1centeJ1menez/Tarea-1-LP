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

    # Abrir el archivo que contiene el código fuente en PySimplex
    # El archivo 'codigo.txt' se encuentra en el directorio './codigos'
    with open("./codigos/codigo.txt", 'r') as archivo:
        contenido = archivo.read() # Leer todo el contenido del archivo

    # Inicializar el archivo de salida ('codigo_interpretado.py'), asegurando que esté vacío
    inicializar_archivo()

    # Analizar la sintaxis del código fuente PySimplex
    # Se establece un límite de 4 niveles de anidamiento para las estructuras condicionales
    analizar_sintaxis(contenido, 4)


    # Leer y ejecutar el código Python generado en 'codigo_interpretado.py'
    with open("codigo_interpretado.py", 'r') as archivo:
        contenido = archivo.read() # Leer el contenido del archivo generado
    exec(contenido) # Ejecutar el código Python interpretado

# Verificar si el script se está ejecutando como el programa principal
if __name__ == "__main__":
    main() # Llamar a la función main para iniciar el programa