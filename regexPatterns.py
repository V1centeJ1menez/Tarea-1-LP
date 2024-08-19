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
