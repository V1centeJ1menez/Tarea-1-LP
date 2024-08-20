from regexPatterns import patterns, string_regex,booleano_regex, entero_regex, variable_regex
import re

variables = {}


def interpretar_valor(token):
    '''
        ***
        Parametros:
        token (str): Representa un token del codigo pysimplex, puede ser un nombre de variable o un tipo de dato int, bool o str. 
        ***
        Retorno:
        tupla (valor interpretado (str,bool, int), identidicador del tipo de dato del valor interpretado (str))
        ***
        La función interpretar_valor toma un token como parámetro y utiliza expresiones regulares para determinar su tipo. 
        Devuelve una tupla que contiene el valor interpretado del token y su tipo. 
        Si el token es un string, devuelve el string sin los caracteres '#' y el tipo 'str'. 
        Si el token es un booleano, devuelve True o False y el tipo 'bool'. 
        Si el token es un entero, devuelve el entero y el tipo 'int'. 
        Si el token es una variable, devuelve el nombre de la variable sin el prefijo '$_' y el tipo 'variable'. 
        Si el token no coincide con ninguna expresión regular, lanza una excepción ValueError.
        ***
    '''
    if re.fullmatch(string_regex, token):  # Es un string si coincide con la expresión regular para strings
        return f'"{token.strip('#')}"', 'str'
    elif re.fullmatch(booleano_regex, token):  # Es un booleano si coincide con la expresión regular para booleanos
        return token == 'True', 'bool'
    elif re.fullmatch(entero_regex, token):  # Es un entero si coincide con la expresión regular para enteros
        return int(token), 'int'
    elif re.fullmatch(variable_regex, token):
        return token.replace('$_',''), 'variable'
    else:
        raise ValueError(f"Token no reconocido o tipo no compatible: {token}")


def levantar_error(tipo, numero, agregado):
    '''
        ***
        Parametros:
        tipo (str)
        numero (int)
        agregado (str)
        ***
        Retorno : None
        ***
        La función levantar_error genera una excepción según su tipo con un 
        mensaje que indica el número de línea y una descripción adicional 
        del error. No retorna ningún valor (None).
        ***
    '''
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
    # Abre el archivo en modo 'w' para borrar todo el contenido y comenzar en blanco
    with open("codigo_interpretado.py", 'w') as archivo:
        pass 
    # Abre el archivo en modo 'w' para borrar todo el contenido y comenzar en blanco
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
        La función `interpretar_operacion` procesa una operación específica representada por los tokens y la escribe en un archivo. 
        Esta función puede manejar la declaración de variables (`DEFINE`), asignaciones y operaciones básicas (`DP`), y mostrar valores (`MOSTRAR`). 
        Dependiendo de los tokens y el operador proporcionado, la función genera el código correspondiente en el archivo con la indentación adecuada. 
        La función también gestiona el valor de las variables en un diccionario global llamado `variables`. 
        Además, verifica si las variables utilizadas están definidas y maneja errores cuando los tipos de datos son incompatibles para ciertas operaciones.
        ***
    '''
    # Declaración de variables
    if tokens[0] == 'DEFINE':
        nombre_variable = tokens[1].replace("$_", "")

        if nombre_variable in variables:
            levantar_error('variableExistente', indice + 1, nombre_variable)
        
        # Si no está definida, se procede a declararla
        variables[nombre_variable] = None
        archivo.write(f'{"\t" * indentacion}{nombre_variable} = None\n')

    elif tokens[0] == 'DP':
        variableDestino = tokens[1].replace("$_", "")
        operador = tokens[2]
        valorUno, tipoUno = interpretar_valor(tokens[3])

        # Si es un tipo 'variable', obtenemos su valor real
        if tipoUno == 'variable':
            if valorUno in variables:
                contenidoValorUno = variables[valorUno]
                tipoUno = type(contenidoValorUno).__name__
                valorUno = contenidoValorUno  # Actualizar con el valor real
            else:
                levantar_error("Nombre", indice + 1, valorUno)
        
        if operador == 'ASIG':
            archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno}\n')
            variables[variableDestino] = valorUno  # Actualizamos el valor en el diccionario
        else:
            valorDos, tipoDos = interpretar_valor(tokens[4])

            if tipoDos == 'variable':
                if valorDos in variables:
                    contenidoValorDos = variables[valorDos]
                    tipoDos = type(contenidoValorDos).__name__
                    valorDos = contenidoValorDos  # Actualizar con el valor real
                else:
                    levantar_error("NoDefinida", indice + 1, valorDos)

            # Validar y procesar la operación binaria
            if operador == '+':
                if tipoUno == 'str' or tipoDos == 'str':
                    # Manejo de concatenación de strings
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = str({valorUno}) {operador} str({valorDos})\n')
                    variables[variableDestino] = str(valorUno) + str(valorDos)  # Actualizar el valor concatenado
                elif tipoUno == 'int' and tipoDos == 'int':
                    # Manejo de suma de enteros
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    variables[variableDestino] = valorUno + valorDos  # Actualizar el valor de la suma
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la suma. Tipos incompatibles.")

            elif operador == '*':
                if tipoUno == 'int' and tipoDos == 'int':
                    # Manejo de multiplicación de enteros
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    variables[variableDestino] = valorUno * valorDos  # Actualizar el valor de la multiplicación
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la multiplicación. Tipos incompatibles.")

            elif operador == '>':
                if tipoUno == 'int' and tipoDos == 'int':
                    # Manejo de comparación mayor que
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    variables[variableDestino] = valorUno > valorDos  # Actualizar el valor de la comparación
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la comparación. Tipos incompatibles.")

            elif operador == '==':
                if tipoUno == tipoDos:
                    # Manejo de igualdad
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    variables[variableDestino] = valorUno == valorDos  # Actualizar el valor de la comparación
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la comparación. Tipos incompatibles.")
    
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
        La función `interpretar` procesa una lista o tupla de tokens que representan las operaciones a realizar y las escribe en un archivo Python para su posterior ejecución.
        Maneja bloques de código, como condicionales `if` y `else`, ajusta la indentación para reflejar correctamente la estructura del código, y llama a la función `interpretar_operacion` para procesar cada operación individual.
        Finalmente, ejecuta el contenido del archivo generado y muestra el estado de las variables después de la ejecución.
        ***
    '''
    indentacion = 0
    with open("codigo_interpretado.py", 'a') as archivo:

        if isinstance(tokens, tuple):
            interpretar_operacion(tokens, archivo, indentacion)
        
        elif isinstance(tokens, list):
            i = 0
            while i < len(tokens):
                if tokens[i][0] == 'if':
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
                    # Inicia un nuevo bloque, aumentar indentación
                    indentacion += 1

                    # Verificar si el próximo token es un '}', lo que indicaría un bloque vacío
                    if i + 1 < len(tokens) and tokens[i + 1] == '}':
                        archivo.write(f'{"\t" * indentacion}pass\n')
                        # Saltar el próximo token '}' para evitar escribir 'pass' nuevamente
                        i += 1

                elif tokens[i] == '}':
                    # Termina un bloque, disminuir indentación
                    indentacion -= 1

                elif tokens[i] == 'else':
                    # Escribir 'else:' al mismo nivel de indentación que el if correspondiente
                    archivo.write(f'{"\t" * indentacion}else:\n')

                    # Verificar si el próximo token es un '{', lo que indicaría el inicio de un bloque
                    if i + 1 < len(tokens) and tokens[i + 1] == '{':
                        # Verificar si el bloque else es vacío
                        if i + 2 < len(tokens) and tokens[i + 2] == '}':
                            archivo.write(f'{"\t" * (indentacion + 1)}pass\n')
                            # Saltar el siguiente '{' y '}' para evitar escribir 'pass' nuevamente
                            i += 2

                elif isinstance(tokens[i], tuple):
                    # Si es una tupla, se procesa como operación
                    interpretar_operacion(tokens[i], archivo, indentacion)

                i += 1


def analizar_sintaxis(codigo_fuente, max_anidamiento):
    '''
        ***
        Parametros: 
        codigo_fuente (str)
        max_anidamiento (int)
        ...
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

            if patterns['procesar'].search(linea):
                # Identificar si es una operación unaria o binaria
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

        # Detectar cierre de bloque
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
