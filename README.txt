# Intérprete de Código PySimplex

### Autor: Vicente Andrés Jiménez Sepúlveda  
### Rol: 202373523-K

## Descripción

Este proyecto implementa un intérprete para un lenguaje de programación sencillo llamado **PySimplex**. El intérprete lee un archivo de código fuente escrito en el lenguaje PySimplex, lo procesa y genera código Python ejecutable. El programa soporta operaciones básicas como declaraciones de variables, asignaciones, operaciones matemáticas, y estructuras condicionales (`if`, `else`).

El intérprete utiliza **expresiones regulares** para identificar y analizar la sintaxis del código PySimplex. Estas expresiones permiten reconocer patrones específicos en el código, como la declaración de variables, las operaciones aritméticas, y las estructuras de control, asegurando que el código fuente sea interpretado correctamente.

El propósito del intérprete es traducir el código fuente escrito en PySimplex a código Python válido, el cual se guarda en un archivo llamado `codigo_interpretado.py`. Luego, este archivo es ejecutado automáticamente, y cualquier salida del programa se guarda en `output.txt`.


## Estructura del Proyecto

- **`main.py`**: Punto de entrada del programa. Lee el código fuente de un archivo, lo procesa utilizando el módulo `Interprete.py` y ejecuta el código Python generado.
- **`Interprete.py`**: Contiene las funciones principales que analizan y procesan el código PySimplex. Aquí se maneja la lógica de interpretación y generación del código Python.
- **`regexPatterns.py`**: Define los patrones de expresiones regulares utilizados para identificar y procesar los diferentes elementos del lenguaje PySimplex.
- **`./codigos/codigo.txt`**: Archivo que contiene el código fuente en PySimplex que será interpretado. Se pueden agregar otros archivos de prueba con diferentes ejemplos de código en el directorio `./codigos`.

## Ejecución

### Requisitos

1. **Python 3.x**: Asegúrate de tener Python 3 instalado en tu sistema.
2. **Archivos del proyecto**: Los archivos `main.py`, `Interprete.py`, `regexPatterns.py`, y `./codigos/codigo.txt` deben estar en la misma carpeta para que el intérprete funcione correctamente.

### Pasos para ejecutar el programa

1. **Preparar el código fuente**: Asegúrate de que el archivo `codigo.txt` en la carpeta `./codigos` contiene el código en PySimplex que deseas interpretar. Puedes agregar otros archivos con ejemplos de código en este directorio.

2. **Ejecutar el intérprete**: Abre una terminal en la carpeta donde se encuentran los archivos del proyecto y ejecuta el siguiente comando:

   ```bash
   python3 main.py
   ```
3. **Resultado**: El programa generará un archivo codigo_interpretado.py con el código Python equivalente al código PySimplex que se procesó. Luego, este código se ejecutará automáticamente, y la salida se guardará en el archivo output.txt.

4. **Ver el resultado**: Revisa el archivo output.txt para ver el resultado de la ejecución del código interpretado.

## Ejemplos de Código PySimplex
El archivo `./codigos/codigo.txt` debe seguir el siguiente formato:

   ```bash
      DEFINE $_variable
      DP $_variable ASIG 5
      MOSTRAR($_variable)
   ```
Este ejemplo declara una variable, le asigna un valor, y luego lo muestra en el archivo de salida.
## Notas
- El intérprete soporta un máximo de 4 estructuras condicionales (if-else) consecutivas. Aceptando algo como:
   ```bash
      if(True):
         if(True):
            #Primer if anidado
            if(True):
               #Segundo if anidado
               if(True):
                  #Tercer if anidado
   ```
- Cualquier error de sintaxis o tipo de dato en el código PySimplex generará una excepción con un mensaje descriptivo, indicando la línea del error.