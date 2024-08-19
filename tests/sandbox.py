import re

# Diccionario global para almacenar el valor de las variables
variables = {}

# Expresiones regulares
digito_regex = r'[1-9]'
digito_o_cero_regex = r'[0-9]'
entero_regex = fr'(?:{digito_regex}{digito_o_cero_regex}*|0)'  # Evitar capturas innecesarias
booleano_regex = r'(?:True|False)'  
string_regex = r'#(?:[A-Za-z0-9 ]*)#'  
oper_un_regex = r'ASIG'
oper_bin_regex = r'(?:\+|\*|>|==)'
variable_regex = r'\$_[A-Z][A-Za-z]*'
operando_regex = fr'(?:{variable_regex}|{entero_regex}|{booleano_regex}|{string_regex})'

declaracion_regex = fr'\s*(DEFINE)\s+({variable_regex})\s*'
procesar_regex = fr'\s*(DP)\s+({variable_regex})\s+' \
                 fr'(?:' \
                 fr'({oper_un_regex})\s+({operando_regex})|' \
                 fr'({oper_bin_regex})\s+({operando_regex})\s+({operando_regex})' \
                 fr')\s*'
mostrar_regex = fr'\s*(MOSTRAR)\(\s*({variable_regex})\s*\)\s*'
inicio_condicional_regex = fr'\s*(if)\s*\(\s*({variable_regex})\s*\)\s*{{\s*'
else_condicional_regex = r'\s*\}\s*(else)\s*\{\s*'
final_else_regex = r'\s*\}\s*'
linea_vacia_regex = r'^\s*$'

condicional_regex = fr'if\s*\({variable_regex}\)\s*\{{\n*[^{{}}]*\n*\}}\s*else\s*\{{\n*[^{{}}]*\n*\}}'
linea_regex = fr'({declaracion_regex}|{procesar_regex}|{condicional_regex}|{mostrar_regex})'

patterns = {
    'digito': re.compile(digito_regex),
    'digito_o_cero': re.compile(digito_o_cero_regex),
    'entero': re.compile(entero_regex),
    'booleano': re.compile(booleano_regex),
    'string': re.compile(string_regex),
    'oper_un': re.compile(oper_un_regex),
    'oper_bin': re.compile(oper_bin_regex),
    'variable': re.compile(variable_regex),
    'operando': re.compile(operando_regex),
    'declaracion': re.compile(declaracion_regex),
    'procesar': re.compile(procesar_regex),
    'mostrar': re.compile(mostrar_regex),
    'condicional': re.compile(condicional_regex),
    'if': re.compile(inicio_condicional_regex),
    'else': re.compile(else_condicional_regex),
    'fin_condicional': re.compile(final_else_regex),
    'linea': re.compile(linea_regex),
    'linea_vacia': re.compile(linea_vacia_regex),
}

def interpretar_valor(token):
    """Interpreta un token y devuelve su valor y tipo usando expresiones regulares."""
    if re.fullmatch(string_regex, token):
        return f'"{token.strip("#")}"', 'str'
    elif re.fullmatch(booleano_regex, token):
        return token == 'True', 'bool'
    elif re.fullmatch(entero_regex, token):
        return int(token), 'int'
    elif re.fullmatch(variable_regex, token):
        return token.replace('$_', ''), 'variable'
    else:
        raise ValueError(f"Token no reconocido o tipo no compatible: {token}")

def levantar_error(tipo, numero, agregado):
    if tipo == 'sintaxis':
        raise SyntaxError(f'Mal Sintaxis: La linea {numero} no está bien escrita. {agregado}')
    elif tipo == 'Tipodato':
        raise TypeError(f'Tipo Incompatible: La operación DP o condicional en la línea {numero} es incompatible al tipo de dato. {agregado}')
    elif tipo == 'Nombre':
        raise NameError(f'Variable No Definida: La variable de nombre {agregado} no ha sido definida o no se le ha asignado valor en la línea {numero}.')
    elif tipo == 'variableExistente':
        raise ValueError()

def inicializar_archivo():
    with open("codigo_interpretado.py", 'w') as archivo:
        pass

def interpretar_tupla(tokens, archivo, indent=''):
    """Interpreta una tupla y escribe el código Python equivalente en el archivo."""
    if tokens[0] == 'DEFINE':
        nombre_variable = tokens[1].replace("$_", "")
        variables[nombre_variable] = None
        archivo.write(f'{indent}{nombre_variable} = None\n')

    elif tokens[0] == 'DP':
        variableDestino = tokens[1].replace("$_", "")
        operador = tokens[2]
        valorUno, tipoUno = interpretar_valor(tokens[3])

        if tipoUno == 'variable':
            if valorUno in variables:
                contenidoValorUno = variables[valorUno]
                tipoUno = type(contenidoValorUno).__name__
            else:
                levantar_error("Nombre", indice + 1, valorUno)
        
        if operador == 'ASIG':
            archivo.write(f'{indent}{variableDestino} = {valorUno}\n')
            variables[variableDestino] = valorUno
        else:
            valorDos, tipoDos = interpretar_valor(tokens[4])

            if tipoDos == 'variable':
                if valorDos in variables:
                    contenidoValorDos = variables[valorDos]
                    tipoDos = type(contenidoValorDos).__name__
                else:
                    levantar_error("Nombre", indice + 1, valorDos)

            if operador == '+':
                if tipoUno == 'str' or tipoDos == 'str':
                    archivo.write(f'{indent}{variableDestino} = str({valorUno}) {operador} str({valorDos})\n')
                elif tipoUno == 'int' and tipoDos == 'int':
                    archivo.write(f'{indent}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la suma. Tipos incompatibles.")
            elif operador == '*':
                if tipoUno == 'int' and tipoDos == 'int':
                    archivo.write(f'{indent}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la multiplicación. Tipos incompatibles.")
            elif operador == '>':
                if tipoUno == 'int' and tipoDos == 'int':
                    archivo.write(f'{indent}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la comparación. Tipos incompatibles.")
            elif operador == '==':
                if tipoUno == tipoDos:
                    archivo.write(f'{indent}{variableDestino} = {valorUno} {operador} {valorDos}\n')
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la comparación. Tipos incompatibles.")

    elif tokens[0] == 'MOSTRAR':
        variableDestino = tokens[1].replace("$_", "")
        archivo.write(f'{indent}with open("output.txt", "w") as archivo:\n')
        archivo.write(f'{indent}    archivo.write(str({variableDestino}))\n')

def interpretar(tokens):
    with open("codigo_interpretado.py", 'a') as archivo:
        if isinstance(tokens, tuple):
            interpretar_tupla(tokens, archivo)
        elif isinstance(tokens, list):
            interpretar_bloque(tokens, archivo)

    if indice == len(lineas):
        with open("codigo_interpretado.py", 'r') as archivo:
            contenido = archivo.read()
        exec(contenido)

def interpretar_bloque(bloque, archivo, nivel_indent=0):
    indent = '    ' * nivel_indent

    i = 0
    while i < len(bloque):
        instruccion = bloque[i]
        
        if isinstance(instruccion, tuple):  # Si es una tupla, es una instrucción
            if instruccion[0] == 'if':
                valorCondicion, tipoCondicion = interpretar_valor(instruccion[1])

                if tipoCondicion == 'variable':
                    if valorCondicion in variables:
                        contenidoValorDos = variables[valorCondicion]
                        tipoCondicion = type(contenidoValorDos).__name__
                    else:
                        levantar_error("Nombre", indice + 1, valorCondicion)

                if tipoCondicion == 'bool':
                    archivo.write(f"{indent}if {valorCondicion}:\n")
                else:
                    levantar_error("Tipodato", indice + 1, "Error en la condición. Tipos incompatibles.")

            interpretar_tupla(instruccion, archivo, indent + '    ')

        elif instruccion == 'else':
            archivo.write(f"{indent}else:\n")
        
        elif instruccion == '{':
            nivel_indent += 1
            indent = '    ' * nivel_indent
        elif instruccion == '}':
            nivel_indent -= 1
            indent = '    ' * nivel_indent

        i += 1

def analizar_sintaxis(codigo_fuente, max_anidamiento):
    global lineas 
    global indice
    lineas = codigo_fuente.splitlines()
    indice = 0
    
    stack_if = []
    queue_else = []
    
    identificador_if = 0
    bloque_independiente_id = 0
    nivel_anidamiento = 0
    bloque_actual = []

    while indice < len(lineas):
        linea = lineas[indice].strip()

        if patterns['declaracion'].search(linea) or patterns['procesar'].search(linea) or patterns['mostrar'].search(linea):
            match = patterns['declaracion'].search(linea) or patterns['procesar'].search(linea) or patterns['mostrar'].search(linea)
            groups = match.groups()

            if patterns['procesar'].search(linea):
                if groups[2]:  # Si el tercer grupo tiene un valor, es unaria
                    groups = (groups[0], groups[1], groups[2], groups[3])
                else:  # Si no, es binaria
                    groups = (groups[0], groups[1], groups[4], groups[5], groups[6])

            if nivel_anidamiento == 0:
                interpretar(groups)
            else:
                bloque_actual.append(groups)

        elif patterns['if'].fullmatch(linea):
            if nivel_anidamiento == 0:  # Nuevo bloque independiente
                bloque_independiente_id += 1
                identificador_if = 0
            identificador_if += 1
            stack_if.append(identificador_if)
            bloque_actual.append(('if', patterns['if'].fullmatch(linea).groups()[1]))
            bloque_actual.append('{')
            nivel_anidamiento += 1
            if nivel_anidamiento > max_anidamiento:
                levantar_error('sintaxis', indice + 1, f"Se sobrepasó el límite de {max_anidamiento} niveles de anidamiento.")

        elif patterns['else'].fullmatch(linea):
            if stack_if:
                bloque_actual.append('}')
                bloque_actual.append('else')
                bloque_actual.append('{')
                queue_else.append(stack_if.pop())
            else:
                levantar_error('sintaxis', indice + 1, "Else sin if correspondiente")

        elif patterns['fin_condicional'].fullmatch(linea):
            if queue_else:
                bloque_actual.append('}')
                queue_else.pop(0)
                if nivel_anidamiento == 1:  # Se completa el bloque if-else principal
                    interpretar(bloque_actual)
                    bloque_actual = []
            elif stack_if:
                bloque_actual.append('}')
                stack_if.pop()
            else:
                levantar_error('sintaxis', indice + 1, "Cierre de bloque inesperado")
            nivel_anidamiento -= 1
        
        elif patterns['linea_vacia'].fullmatch(linea):
            levantar_error('sintaxis', indice + 1, 'Línea vacía.')
        else:
            levantar_error('sintaxis', indice + 1, 'Línea no reconocida')

        indice += 1

    if stack_if or queue_else:
        levantar_error('sintaxis', indice, "Bloques if-else incompletos al final del archivo")

with open("codigo.txt", 'r') as archivo:
    contenido = archivo.read()

inicializar_archivo()
analizar_sintaxis(contenido, 4)
