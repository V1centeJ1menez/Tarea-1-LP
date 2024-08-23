from regexPatterns import patterns, string_regex,booleano_regex, entero_regex, variable_regex
import re

ambitos = [{}]
global instruccion
instruccion = 0

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
    elif tipo == 'NoDefinida':
        raise NameError(f'Variable No Definida: La variable de nombre {agregado} no ha sido definida o no se le ha asignado valor en la línea {numero}.')
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


def buscar_variable(nombre_variable):
    '''
        ***
        Parámetros:
        - nombre_variable (str): El nombre de la variable que se desea buscar en los ámbitos actuales.

        ***
        Retorno:
        tuple: Una tupla que contiene:
        - El valor de la variable si se encuentra (cualquiera que sea su valor), o `None` si no se encuentra.
        - Un valor booleano `True` si la variable existe en alguno de los ámbitos, o `False` si no existe.

        ***
        La función `buscar_variable` busca una variable en los ámbitos disponibles.
        Comienza desde el ámbito más interno (el más reciente) y avanza hacia el más externo,
        verificando si la variable está definida. Si se encuentra, se devuelve el valor de la variable
        junto con `True`. Si no se encuentra en ningún ámbito, devuelve `None` y `False`.
        ***
    '''
     
    for ambito in reversed(ambitos):
        if nombre_variable in ambito:
            return ambito[nombre_variable], True
    return None,False  # Si no se encuentra en ningún ámbito

def interpretar_operacion(tokens, archivo, indentacion):
    '''
        interpretar_operacion(tokens, archivo, indentacion)
        ----------------------------
        Procesa y ejecuta una operación basada en los tokens proporcionados, escribiendo el código 
        resultante en el archivo especificado.

        Parámetros:
        - tokens (list): Una lista de tokens que representa la operación a realizar. Los tokens 
        incluyen la instrucción, las variables y los operadores.
        - archivo (file object): El archivo donde se escribirá el código Python generado.
        - indentacion (int): El nivel de indentación para el código generado.

        Retorno:
        None

        La función `interpretar_operacion` interpreta los tokens y realiza diferentes operaciones 
        basadas en el tipo de instrucción (`DEFINE`, `DP`, `MOSTRAR`). Dependiendo de la instrucción, 
        la función puede definir variables, realizar asignaciones y operaciones aritméticas, y 
        escribir el resultado en el archivo. La función también maneja errores de tipo y variables 
        no definidas, y escribe el código Python correspondiente en el archivo.
        '''
    ambito_actual = ambitos[-1]

    if tokens[0] == 'DEFINE':
        nombre_variable = tokens[1].replace("$_", "")

        # Verificar si la variable ya ha sido definida previamente en el mismo ámbito
        if nombre_variable in ambito_actual:
            levantar_error('VariableExistente', instruccion + 1, nombre_variable)
        # Guardar el valor original si la variable ya existe en un ámbito superior
        valor_anterior, existe_variable = buscar_variable(nombre_variable)

        if existe_variable:
            ambito_actual[f'_backup_{nombre_variable}'] = valor_anterior
        
        # Redefinir la variable en el ámbito actual
        ambito_actual[nombre_variable] = None
        archivo.write(f'{"\t" * indentacion}{nombre_variable} = None\n')

    elif tokens[0] == 'DP':
        variableDestino = tokens[1].replace("$_", "")
        valor_variableDestino, existeVariable = buscar_variable(variableDestino)

        if not existeVariable:
            levantar_error("NoDefinida", instruccion, variableDestino)

        operador = tokens[2]
        valorUno, tipoUno = interpretar_valor(tokens[3])

        if tipoUno == 'variable':
            valor_variableUno, _ = buscar_variable(valorUno)
            if valor_variableUno is not None:
                tipoUno = type(valor_variableUno).__name__
                valorUno = valor_variableUno
            else:
                levantar_error("NoDefinida", instruccion, valorUno)

        if operador == 'ASIG':
            ambito_actual[variableDestino] = valorUno
            archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno}\n')

        else:
            valorDos, tipoDos = interpretar_valor(tokens[4])

            if tipoDos == 'variable':
                valor_variableDos, _ = buscar_variable(valorDos)
                if valor_variableDos is not None:
                    tipoDos = type(valor_variableDos).__name__
                    valorDos = valor_variableDos
                else:
                    levantar_error("NoDefinida", instruccion, valorDos)

            if operador == '+':
                if tipoUno == 'str' or tipoDos == 'str':
                    if tipoUno == 'bool' or tipoDos == 'bool':
                        levantar_error("Tipodato", instruccion, "Error en la suma. Tipos incompatibles.")
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = str({valorUno}) {operador} str({valorDos})\n')
                    ambito_actual[variableDestino] = str(valorUno) + str(valorDos)
                elif tipoUno == 'int' and tipoDos == 'int':
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    ambito_actual[variableDestino] = valorUno + valorDos
                else:
                    levantar_error("Tipodato", instruccion, "Error en la suma. Tipos incompatibles.")

            elif operador == '*':
                if tipoUno == 'int' and tipoDos == 'int':
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    ambito_actual[variableDestino] = valorUno * valorDos
                else:
                    levantar_error("Tipodato", instruccion, "Error en la multiplicación. Tipos incompatibles.")

            elif operador == '>':
                if tipoUno == 'int' and tipoDos == 'int':
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    ambito_actual[variableDestino] = valorUno > valorDos
                else:
                    levantar_error("Tipodato", instruccion, "Error en la comparación. Tipos incompatibles.")

            elif operador == '==':
                if tipoUno == tipoDos:
                    if tipoUno == 'bool' or tipoDos == 'bool':
                        levantar_error("Tipodato", instruccion, "Error en la comparación. Tipos incompatibles.")
                    archivo.write(f'{"\t" * indentacion}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                    ambito_actual[variableDestino] = valorUno == valorDos
                else:
                    levantar_error("Tipodato", instruccion, "Error en la comparación. Tipos incompatibles.")

    elif tokens[0] == 'MOSTRAR':
        variableDestino = tokens[1].replace("$_", "")
        valor_variableDestino, _ = buscar_variable(variableDestino)
        if valor_variableDestino is None:
            levantar_error("NoDefinida", instruccion, variableDestino)
        archivo.write(f'{"\t" * indentacion}with open("output.txt", "a") as archivo:\n{"\t" * (indentacion + 1)}archivo.write(str({variableDestino}) + "\\n")\n')

def interpretar(tokens):
    '''
        interpretar(tokens)
        ---------------------
        Interpreta una lista de tokens y convierte las instrucciones en código Python, 
        escribiéndolo en un archivo. Maneja bloques de código, estructuras condicionales 
        y operaciones.

        Parámetros:
        - tokens (list): Una lista de tokens que representa el código a interpretar.

        Retorno:
        None

        La función `interpretar` recorre los tokens y escribe el código Python equivalente 
        en el archivo `codigo_interpretado.py`. Maneja estructuras de control como `if` y 
        `else`, así como bloques de código delimitados por `{` y `}`. La función también 
        llama a `interpretar_operacion` para procesar las operaciones individuales y 
        mantiene el nivel de indentación para asegurar que el código generado sea 
        sintácticamente correcto.
    '''
    indentacion = 0
    global instruccion
    with open("codigo_interpretado.py", 'a') as archivo:

        if isinstance(tokens, tuple):
            instruccion = instruccion + 1
            interpretar_operacion(tokens, archivo, indentacion)
        
        elif isinstance(tokens, list):
            i = 0
            while i < len(tokens):
                
                if tokens[i][0] == 'if':
                    instruccion = instruccion + 1
                    condicion, tipo_condicion = interpretar_valor(tokens[i][1])
                    if tipo_condicion == 'bool':
                        archivo.write(f'{"\t" * indentacion}if {condicion}:\n')
                    elif tipo_condicion == 'variable':
                        valor_condicion, _ = buscar_variable(condicion)
                        if valor_condicion is not None and isinstance(valor_condicion, bool):
                            archivo.write(f'{"\t" * indentacion}if {condicion}:\n')
                        else:
                            levantar_error("Tipodato", instruccion, f"La variable {condicion} no es booleana.")
                    else:
                        levantar_error("Tipodato", instruccion, f"La condición {condicion} no es un booleano válido.")
                    
                elif tokens[i] == '{':
                    indentacion += 1
                    ambitos.append({})

                    # Verificar si el próximo token es un '}', lo que indicaría un bloque vacío
                    if i + 1 < len(tokens) and tokens[i + 1] == '}':
                        archivo.write(f'{"\t" * indentacion}pass\n')
                        # Saltar el próximo token '}' para evitar escribir 'pass' nuevamente
                        i += 1

                elif tokens[i] == '}':

                    for variable, valor in ambitos[-1].items():
                        if variable.startswith('_backup_'):
                            nombre_original = variable.replace('_backup_', '')
                            # Restaurar el valor del ámbito superior si fue redefinida
                            archivo.write(f'{"\t" * indentacion }{nombre_original} = {valor}\n')
                    indentacion -= 1
                    
                    
                    ambitos.pop()
                    

                    

                elif tokens[i] == 'else':
                    instruccion = instruccion + 1
                    archivo.write(f'{"\t" * indentacion}else:\n')

                    # Verificar si el próximo token es un '{', lo que indicaría el inicio de un bloque
                    if i + 1 < len(tokens) and tokens[i + 1] == '{':
                        # Verificar si el bloque else es vacío
                        if i + 2 < len(tokens) and tokens[i + 2] == '}':
                            archivo.write(f'{"\t" * (indentacion + 1)}pass\n')
                            # Saltar el siguiente '{' y '}' para evitar escribir 'pass' nuevamente
                            i += 2
                    

                elif isinstance(tokens[i], tuple):
                    instruccion = instruccion + 1
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
