import re

# Expresiones regulares #

# Las expresiones regulares se utilizan para identificar patrones específicos en el código PySimplex.
# El símbolo `(?: ...)` dentro de una expresión regular se utiliza para agrupar subpatrones 
# sin capturarlos, lo que evita capturas innecesarias cuando se usan métodos como .groups().

# Regex de tipos de datos #

# Define el patrón para identificar dígitos (del 1 al 9).
digito_regex = r'[1-9]'

# Define el patrón para identificar dígitos, incluyendo el 0.
digito_o_cero_regex = r'[0-9]'

# Define el patrón para identificar números enteros.
# Puede ser un número que comienza por un dígito no cero seguido de cualquier cantidad de dígitos,
# o simplemente el número 0.
entero_regex = fr'(?:{digito_regex}{digito_o_cero_regex}*|0)'  # Evitar capturas innecesarias

# Define el patrón para identificar valores booleanos (True o False).
booleano_regex = r'(?:True|False)'  

# Define el patrón para identificar cadenas de texto (strings) que están delimitadas por el carácter '#'.
string_regex = r'#(?:[A-Za-z0-9 ]*)#'  

# Define el patrón para identificar el operador de asignación (ASIG).
oper_un_regex = r'ASIG'

# Define el patrón para identificar operadores binarios (+, *, >, ==).
oper_bin_regex = r'(?:\+|\*|>|==)'

# Define el patrón para identificar variables.
# Las variables en PySimplex comienzan con '$_' seguido de una letra mayúscula y pueden contener 
# letras mayúsculas y minúsculas adicionales.
variable_regex = r'\$_[A-Z][A-Za-z]*'

# Define el patrón para identificar operandos, que pueden ser variables, enteros, booleanos o strings.
operando_regex = fr'(?:{variable_regex}|{entero_regex}|{booleano_regex}|{string_regex})'

# Regex de operaciones

# Define el patrón para identificar la declaración de una variable.
# Ejemplo: DEFINE $_Variable
declaracion_regex = fr'\s*(DEFINE)\s+({variable_regex})\s*' # Declaracion

# Define el patrón para identificar operaciones de procesamiento (unarias o binarias).
# Ejemplos: DP $_Variable ASIG 5  o  DP $_Variable + $_OperandoUno $_OperandoDos
procesar_regex = fr'\s*(DP)\s+({variable_regex})\s+' \
                 fr'(?:' \
                 fr'({oper_un_regex})\s+({operando_regex})|' \
                 fr'({oper_bin_regex})\s+({operando_regex})\s+({operando_regex})' \
                 fr')\s*' # Expresión regular unificada para manejar tanto operaciones unarias como binarias

# Define el patrón para identificar la operación MOSTRAR, que es equivalente a un print.
# Ejemplo: MOSTRAR($_Variable)
mostrar_regex = fr'\s*(MOSTRAR)\(\s*({variable_regex})\s*\)\s*' # Mostrar, cercano a un print

# Regex de estructuras condicionales

# Define el patrón para capturar bloques condicionales if-else sin analizar el contenido interno.
# Ejemplo: if ($_Variable) { ... } else { ... }
condicional_regex = fr'(if)\s*\(\s*({variable_regex})\s*\)\s*\{{\n*[^{{}}]*\n*\}}\s*(else)\s*\{{\n*[^{{}}]*\n*\}}' # Captura bloques if-else sin analizar el contenido interno

# Tokenizar condicional( Similar a si capturo los grupos desde condicional_regex)

# Define el patrón para identificar el inicio de un bloque condicional if.
# Ejemplo: if ($_Variable) {
inicio_condicional_regex = fr'\s*(if)\s*\(\s*({variable_regex})\s*\)\s*{{\s*'

# Define el patrón para identificar el else correspondiente a un bloque if.
else_condicional_regex = r'\s*\}\s*(else)\s*\{\s*'

# Define el patrón para identificar el final de un bloque else.
final_else_regex = r'\s*\}\s*'

# Regex de forma de Línea

# Define el patrón para identificar líneas vacías.
linea_vacia_regex=r'^\s*$'

# Define el patrón para identificar cualquier línea que coincida con una declaración,
# una operación de procesamiento, un bloque condicional o una operación MOSTRAR.
linea_regex = fr'({declaracion_regex}|{procesar_regex}|{condicional_regex}|{mostrar_regex})'


# Compilación de patrones

# Compila todas las expresiones regulares definidas anteriormente en patrones que 
# pueden ser reutilizados para analizar el código PySimplex.
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
