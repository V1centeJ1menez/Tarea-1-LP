from regexPatterns import patterns, string_regex,booleano_regex, entero_regex, variable_regex
import re

variables = {}


def interpretar_valor(token):
    '''
        ***
        Parametros:
        token (str): Representa un token del código PySimplex, que puede ser un nombre de variable o un tipo de dato int, bool o str.
        ***
        Retorno:
        tupla (valor interpretado (str, bool, int), identificador del tipo de dato del valor interpretado (str))
        ***
        La función interpretar_valor toma un token como parámetro y utiliza expresiones regulares para determinar su tipo.
        Devuelve una tupla que contiene el valor interpretado del token y su tipo.
        - Si el token es un string, devuelve el string sin los caracteres '#' y el tipo 'str'.
        - Si el token es un booleano, devuelve True o False y el tipo 'bool'.
        - Si el token es un entero, devuelve el entero y el tipo 'int'.
        - Si el token es una variable, devuelve el nombre de la variable sin el prefijo '$_' y el tipo 'variable'.
        - Si el token no coincide con ninguna expresión regular, lanza una excepción ValueError.
        ***
    '''
    if re.fullmatch(string_regex, token):  # Verifica si el token es un string según la expresión regular definida
        return f'"{token.strip('#')}"', 'str'
    elif re.fullmatch(booleano_regex, token):  # Verifica si el token es un booleano (True o False)
        return token == 'True', 'bool'
    elif re.fullmatch(entero_regex, token):  # Verifica si el token es un número entero
        return int(token), 'int'
    elif re.fullmatch(variable_regex, token): # Verifica si el token es una variable
        return token.replace('$_',''), 'variable'
    else:
        # Si el token no coincide con ninguna expresión regular, se lanza un error indicando que el token no es válido
        raise ValueError(f"Token no reconocido o tipo no compatible: {token}")


def levantar_error(tipo, numero, agregado):
    '''
        ***
        Parametros:
        tipo (str): Tipo de error a generar (Sintaxis, Tipodato, Nombre, VariableExistente).
        numero (int): Número de línea donde ocurrió el error.
        agregado (str): Información adicional sobre el error.
        ***
        Retorno: None
        ***
        La función levantar_error genera una excepción según su tipo con un
        mensaje que indica el número de línea y una descripción adicional
        del error. No retorna ningún valor (None).
        ***
    '''
    # Dependiendo del tipo de error, se levanta la excepción correspondiente con un mensaje detallado
    if tipo == 'Sintaxis':
        raise SyntaxError(f'Mal Sintaxis: La linea {numero} no está bien escrita. {agregado}')
    elif tipo == 'Tipodato':
        raise TypeError(f'Tipo Incompatible: La operación DP o condicional en la línea {numero} es incompatible al tipo de dato. {agregado}')
    elif tipo == 'Nombre':
        raise NameError(f'Variable No Definida: La variable de nombre {agregado} no ha sido definida o no se le ha asignad valor en la línea {numero}.')
    elif tipo == 'VariableExistente':
        raise ValueError(f'Variable Ya Definida: La variable de nombre {agregado} ya se encuentra definida. Error en la linea {numero}')


def inicializar_archivo():
    '''
        ***
        Parametros:
        None
        ***
        Retorno:
        None
        ***
        La función inicializar_archivo abre el archivo "codigo_interpretado.py" en modo escritura ('w'),
        lo que borra todo el contenido existente y deja el archivo en blanco. No retorna ningún valor (None).
        ***
    '''
    # Abrir el archivo "codigo_interpretado.py" en modo escritura para borrar su contenido y comenzar desde cero
    with open("codigo_interpretado.py", 'w') as archivo:
        pass 
    # También se inicializa el archivo "output.txt" de la misma manera
    with open("output.txt", 'w') as archivo:
        pass 

def interpretar_operacion(tokens, archivo, indentacion):
    '''
        ***
        Parámetros:
        - tokens (tuple): Una tupla que contiene los tokens que representan una operación específica.
        - archivo (file object): Archivo abierto en el que se escribirá el código generado.
        - indentacion (int): Nivel de indentación para formatear el código en el archivo.

        ***
        Retorno:
        None
        ***
        La función interpretar_operacion procesa una operación específica representada por los tokens y la escribe en un archivo.
        Esta función puede manejar la declaración de variables (`DEFINE`), asignaciones y operaciones básicas (`DP`), y mostrar valores (`MOSTRAR`).
        Dependiendo de los tokens y el operador proporcionado, la función genera el código correspondiente en el archivo con la indentación adecuada.
        La función también gestiona el valor de las variables en un diccionario global llamado `variables`.
        Además, verifica si las variables utilizadas están definidas y maneja errores cuando los tipos de datos son incompatibles para ciertas operaciones.
        ***
    '''
    # Manejar la declaración de variables
    if tokens[0] == 'DEFINE':
        nombre_variable = tokens[1].replace("$_", "")

        # Verificar si la variable ya ha sido definida previamente
        if nombre_variable in variables:
            levantar_error('variableExistente', indice + 1, nombre_variable)
        
        # Si la variable no está definida, se agrega al diccionario con un valor inicial de None
        variables[nombre_variable] = None
        archivo.write(f'{"\t" * indentacion}{nombre_variable} = None\n')

    # Manejar la asignación y operaciones (DP)  
    elif tokens[0] == 'DP':
        variableDestino = tokens[1].replace("$_", "")
        operador = tokens[2]
        valorUno, tipoUno = interpretar_valor(tokens[3])

        # Si el valor es una variable, obtener su valor real
        if tipoUno == 'variable':
            if valorUno in variables:
                contenidoValorUno = variables[valorUno]
                tipoUno = type(contenidoValorUno).__name__
                valorUno = contenidoValorUno  # Actualizar con el valor real de la variable
            else:
                levantar_error("Nombre", indice + 1, valorUno)
        
        # Manejo de la operación de asignación (ASIG)
        if operador == 'ASIG':
            archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno}\n')
            variables[variableDestino] = valorUno  # Actualizamos el valor en el diccionario de variables
        else:
            # Para otras operaciones (+, *, >, ==) se procesa un segundo valor
            valorDos, tipoDos = interpretar_valor(tokens[4])

            # Si el segundo valor es una variable, obtener su valor real
            if tipoDos == 'variable':
                if valorDos in variables:
                    contenidoValorDos = variables[valorDos]
                    tipoDos = type(contenidoValorDos).__name__
                    valorDos = contenidoValorDos  # Actualizar con el valor real de la variable
                else:
                    levantar_error("NoDefinida", indice + 1, valorDos)

            # Manejo de operaciones aritméticas y comparativas
            if operador == '+':
                if tipoUno == 'str' or tipoDos == 'str': # Concatenación de strings
                    # Manejo de concatenación de strings
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = str({valorUno}) {operador} str({valorDos})\n')
                    variables[variableDestino] = str(valorUno) + str(valorDos)  # Actualizar el valor concatenado
                elif tipoUno == 'int' and tipoDos == 'int': # Suma de enteros
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    variables[variableDestino] = valorUno + valorDos  # Actualizar el valor de la suma
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la suma. Tipos incompatibles.")

            elif operador == '*':
                if tipoUno == 'int' and tipoDos == 'int': # Multiplicación de enteros
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    variables[variableDestino] = valorUno * valorDos  # Actualizar el valor de la multiplicación
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la multiplicación. Tipos incompatibles.")

            elif operador == '>':
                if tipoUno == 'int' and tipoDos == 'int': # Comparación "mayor que"
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    variables[variableDestino] = valorUno > valorDos  # Actualizar el valor de la comparación
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la comparación. Tipos incompatibles.")

            elif operador == '==':
                if tipoUno == tipoDos: # Comparación de igualdad
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    variables[variableDestino] = valorUno == valorDos  # Actualizar el valor de la comparación
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la comparación. Tipos incompatibles.")
    
    # Manejar la operación de mostrar valores (MOSTRAR)
    elif tokens[0] == 'MOSTRAR':
        variableDestino = tokens[1].replace("$_", "")
        archivo.write(f"{"\t" * indentacion}with open('output.txt', 'a') as archivo:\n{"\t" * (indentacion + 1)}archivo.write(str({variableDestino}) + \"\\n\")\n")


def interpretar(tokens):
    '''
        ***
        Parámetros:
        - tokens (tuple or list): Representa una instrucción o un conjunto de instrucciones a interpretar.
        ***
        Retorno:
        None
        ***
        La función interpretar procesa una lista o tupla de tokens que representan las operaciones a realizar y las escribe en un archivo Python para su posterior ejecución.
        Maneja bloques de código, como condicionales `if` y `else`, ajusta la indentación para reflejar correctamente la estructura del código, y llama a la función interpretar_operacion para procesar cada operación individual.
        Finalmente, ejecuta el contenido del archivo generado y muestra el estado de las variables después de la ejecución.
        ***
    '''
    # para depurar print(tokens)
    indentacion = 0
    with open("codigo_interpretado.py", 'a') as archivo:

        if isinstance(tokens, tuple):
            interpretar_operacion(tokens, archivo, indentacion)
        
        elif isinstance(tokens, list):
            i = 0
            while i < len(tokens):
                if tokens[i][0] == 'if':
                    # Analizar y escribir la condición de un bloque if
                    condicion, tipo_condicion = interpretar_valor(tokens[i][1])
                    if tipo_condicion == 'bool':
                        archivo.write(f'{"\t" * indentacion}if {condicion}:\n')
                    elif tipo_condicion == 'variable':
                        if variables.get(condicion) is not None and isinstance(variables[condicion], bool):
                            archivo.write(f'{"\t" * indentacion}if {condicion}:\n')
                        else:
                            levantar_error("Tipodato", indice + 1, f"La variable {condicion} no es booleana.")
                    else:
                        levantar_error("Tipodato", indice + 1, f"La condición {condicion} no es un booleano válido.")
                    
                elif tokens[i] == '{':
                    # Detecta el inicio de un bloque, aumentando la indentación
                    indentacion += 1

                    # Verificar si el próximo token es un '}', lo que indicaría un bloque vacío
                    if i + 1 < len(tokens) and tokens[i + 1] == '}':
                        archivo.write(f'{"\t" * indentacion}pass\n')
                        # Saltar el próximo token '}' para evitar escribir 'pass' nuevamente
                        i += 1

                elif tokens[i] == '}':
                    # Detecta el fin de un bloque, disminuyendo la indentación
                    indentacion -= 1

                elif tokens[i] == 'else':
                    # Manejo de la estructura else con la indentación correspondiente
                    archivo.write(f'{"\t" * indentacion}else:\n')

                    # Verificar si el próximo token es un '{', lo que indicaría el inicio de un bloque
                    if i + 1 < len(tokens) and tokens[i + 1] == '{':
                        # Verificar si el bloque else es vacío
                        if i + 2 < len(tokens) and tokens[i + 2] == '}':
                            archivo.write(f'{"\t" * (indentacion + 1)}pass\n')
                            # Saltar el siguiente '{' y '}' para evitar escribir 'pass' nuevamente
                            i += 2

                elif isinstance(tokens[i], tuple):
                    # Procesar operaciones individuales dentro de la lista de tokens
                    interpretar_operacion(tokens[i], archivo, indentacion)

                i += 1


def analizar_sintaxis(codigo_fuente, max_anidamiento):
    '''
        ***
        Parametros: 
        codigo_fuente (str): Código fuente en PySimplex que se va a analizar.
        max_anidamiento (int): Máximo nivel de anidamiento permitido para estructuras condicionales.
        ***
        Retorno:
        None
        ***
        La función analizar_sintaxis analiza el código fuente para detectar y
        procesar declaraciones, operaciones y estructuras de control como if y
        else. Verifica la correcta anidación y levanta errores si encuentra
        problemas de sintaxis. No retorna ningún valor (None).
        ***
    '''
    lineas = codigo_fuente.splitlines()
    global indice
    indice = 0
    
    # Pilas para manejar los if y los else
    stack_if = []
    queue_else = []
    
    identificador_if = 0
    bloque_independiente_id = 0
    nivel_anidamiento = 0
    bloque_actual = []

    while indice < len(lineas):
        linea = lineas[indice].strip()
    
        # Detectar declaraciones, procesamientos o mostrar
        if patterns['declaracion'].search(linea) or patterns['procesar'].search(linea) or patterns['mostrar'].search(linea):
            
            match =  patterns['declaracion'].search(linea) or patterns['procesar'].search(linea) or patterns['mostrar'].search(linea)
            groups = match.groups()

            # Identificar si es una operación unaria o binaria
            if patterns['procesar'].search(linea):
                if groups[2]:  # Si el tercer grupo tiene un valor, es unaria
                    groups = (groups[0], groups[1], groups[2], groups[3])
                else:  # Si no, es binaria
                    groups = (groups[0], groups[1], groups[4], groups[5], groups[6])

            if nivel_anidamiento == 0:
                # Procesar inmediatamente si no estamos dentro de un bloque if-else
                interpretar(groups)
            else:
                # Añadir a bloque actual si estamos dentro de un bloque if-else
                bloque_actual.append(groups)

        # Detectar inicio de if
        elif patterns['if'].fullmatch(linea):
            if nivel_anidamiento == 0:  # Nuevo bloque independiente
                bloque_independiente_id += 1
                identificador_if = 0  # Reiniciar la numeración de if
            identificador_if += 1
            stack_if.append(identificador_if)
            bloque_actual.append(('if', patterns['if'].fullmatch(linea).groups()[1]))
            bloque_actual.append('{')
            nivel_anidamiento += 1
            if nivel_anidamiento > max_anidamiento:
                levantar_error('Sintaxis',indice + 1, f"Se sobrepasó el límite de {max_anidamiento} niveles de anidamiento.")

        # Detectar else
        elif patterns['else'].fullmatch(linea):
            if stack_if:
                bloque_actual.append('}')
                bloque_actual.append('else')
                bloque_actual.append('{')
                queue_else.append(stack_if.pop())
            else:
                levantar_error('Sintaxis',indice + 1, "Else sin if correspondiente")

        # Detectar cierre de bloque if-else
        elif patterns['fin_condicional'].fullmatch(linea):
            if queue_else:
                bloque_actual.append('}')
                queue_else.pop(0)
                if nivel_anidamiento == 1:  # Se completa el bloque if-else principal
                    interpretar(bloque_actual)
                    bloque_actual = []  # Reiniciar el bloque actual
            elif stack_if:
                bloque_actual.append('}')
                stack_if.pop()
            else:
                levantar_error('Sintaxis',indice + 1, "Cierre de bloque inesperado")
            nivel_anidamiento -= 1
        
        elif patterns['linea_vacia'].fullmatch(linea):
             levantar_error('Sintaxis',indice + 1, 'Linea vacía.' )
        else:
            levantar_error('Sintaxis',indice + 1, 'Línea no reconocida')

        indice += 1

    # Si al final del archivo quedan bloques sin procesar, lanzamos un error
    if stack_if or queue_else:
        levantar_error('Sintaxis',indice, "Bloques if-else incompletos al final del archivo")
