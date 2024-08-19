import re

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
# Expresión regular unificada para manejar tanto operaciones unarias como binarias
procesar_regex = fr'\s*(DP)\s+({variable_regex})\s+' \
                 fr'(?:' \
                 fr'({oper_un_regex})\s+({operando_regex})|' \
                 fr'({oper_bin_regex})\s+({operando_regex})\s+({operando_regex})' \
                 fr')\s*'
mostrar_regex = fr'\s*(MOSTRAR)\(\s*({variable_regex})\s*\)\s*'
# Tokenizar condicional
inicio_condicional_regex = fr'\s*(if)\s*\(\s*({variable_regex})\s*\)\s*{{\s*'
else_condicional_regex = r'\s*\}\s*(else)\s*\{\s*'
final_else_regex = r'\s*\}\s*'
linea_vacia_regex=r'^\s*$'

# Captura bloques if-else sin analizar el contenido interno
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
    'linea_vacia':re.compile(linea_vacia_regex),
}

def interpretar_valor(token):
    """Interpreta un token y devuelve su valor y tipo usando expresiones regulares."""
    if re.fullmatch(string_regex, token):  # Es un string si coincide con la expresión regular para strings
        return token.strip('#'), 'string'
    elif re.fullmatch(booleano_regex, token):  # Es un booleano si coincide con la expresión regular para booleanos
        return token == 'True', 'bool'
    elif re.fullmatch(entero_regex, token):  # Es un entero si coincide con la expresión regular para enteros
        return int(token), 'int'
    else:
        raise ValueError(f"Token no reconocido o tipo no compatible: {token}")


def levantar_error(numero, agregado):
    raise SyntaxError(f'Mal Sintaxis: La linea {numero} no está bien escrita. {agregado}')

def ejecutar(tokens):

    print(tokens)

def analizar_sintaxis(codigo_fuente, max_anidamiento=4):
    lineas = codigo_fuente.splitlines()
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
                ejecutar(groups)
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
                levantar_error(indice + 1, f"Se sobrepasó el límite de {max_anidamiento} niveles de anidamiento.")

        # Detectar else
        elif patterns['else'].fullmatch(linea):
            if stack_if:
                bloque_actual.append('}')
                bloque_actual.append('else')
                bloque_actual.append('{')
                queue_else.append(stack_if.pop())
            else:
                levantar_error(indice + 1, "Else sin if correspondiente")

        # Detectar cierre de bloque
        elif patterns['fin_condicional'].fullmatch(linea):
            if queue_else:
                bloque_actual.append('}')
                queue_else.pop(0)
                if nivel_anidamiento == 1:  # Se completa el bloque if-else principal
                    ejecutar(bloque_actual)
                    bloque_actual = []  # Reiniciar el bloque actual
            elif stack_if:
                bloque_actual.append('}')
                stack_if.pop()
            else:
                levantar_error(indice + 1, "Cierre de bloque inesperado")
            nivel_anidamiento -= 1
        
        elif patterns['linea_vacia'].fullmatch(linea):
             levantar_error(indice + 1, 'Linea vacía.' )
        else:
            levantar_error(indice + 1, 'Línea no reconocida')

        indice += 1

    # Si al final del archivo quedan bloques sin procesar, lanzamos un error
    if stack_if or queue_else:
        levantar_error(indice, "Bloques if-else incompletos al final del archivo")


with open("codigo2.txt", 'r') as archivo:
    contenido = archivo.read()

# Analizar con un límite de 4 niveles de anidamiento
analizar_sintaxis(contenido, max_anidamiento=4)