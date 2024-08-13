import re

INT_REGEX = r'^(0|[1-9]\d*)$'

# Ejemplos de uso
ejemplos = ["0", "123", "980ddf", "01", "0001", "00123", "456"]

for ejemplo in ejemplos:
    if re.match(INT_REGEX, ejemplo):
        print(f"'{ejemplo}' es un número entero válido.")
    else:
        print(f"'{ejemplo}' NO es un número entero válido.")




BOOL_REGEX = r'^(True|False)$'

# Ejemplos de uso
ejemplos = ["True", "False", "true", "false", "TRUE", "FALSE", "Tru", "Falsee"]

for ejemplo in ejemplos:
    if re.match(BOOL_REGEX, ejemplo):
        print(f"'{ejemplo}' es un booleano válido.")
    else:
        print(f"'{ejemplo}' NO es un booleano válido.")

STRING_REGEX = r'(#\s*(.*?)\s*#)'


# Ejemplos de uso
texto = "variable = # Esto es un string válido #; variable1 = # Este es otro string válido #; variable2 = # Esto #no es válido #;"

# Captura de los strings
matches = re.findall(STRING_REGEX, texto)

print("Strings:", matches)  # Output: ['Esto es un string válido', 'Este es otro string válido']



VARIABLE_REGEX = r'\$_[A-Z][a-zA-Z]*'

# Ejemplos de uso
texto = "$_Var; $_OtraVariable; $VariableInvalida; $1Variable; $_hola; $Variable;"

matches = re.findall(VARIABLE_REGEX, texto)

print(matches)  # Output: ['$_Var', '$_OtraVariable']
