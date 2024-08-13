import re

# ANALISIS LEXICO #

# Definir patrones de tokens #
patrones = [
        (r'(?P<define>DEFINE)', 'DEFINE'),
        (r'(?P<dp>DP)', 'DP'),
        (r'(?P<if>if)', 'IF'),
        (r'(?P<else>else)', 'ELSE'),
        (r'(?P<mostrar>MOSTRAR)', 'MOSTRAR'),
        (r'(?P<variable>\$_[A-Z][A-Za-z]*)', 'VARIABLE'),
        (r'(?P<entero>[1-9][0-9]*)', 'ENTERO'),
        (r'(?P<booleano>True|False)', 'BOOLEANO'),
        (r'(?P<string>#.*?#)', 'STRING'),
        (r'(?P<op_un>ASIG)', 'OPER_UN'),
        (r'(?P<op_bin>\+|\*|>|==)', 'OPER_BIN'),
        (r'(?P<par_abr>\()', 'PAR_ABR'),
        (r'(?P<par_cer>\))', 'PAR_CER'),
        (r'(?P<llave_abr>\{)', 'LLAVE_ABR'),
        (r'(?P<llave_cer>\})', 'LLAVE_CER'),
        (r'(?P<espacio>\s+)', 'ESPACIO'),
    ]

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

# Tokenizer
class Tokenizer:

    def __init__(self, codigo_fuente):
        self.codigo_fuente = codigo_fuente
        self.tokens = []
        self.patrones_compilados = [(re.compile(patron), tipo) for patron, tipo in patrones]

    def tokenizar(self):
        for linea in self.codigo_fuente:
            pos = 0
            while pos < len(linea):
                match = None
                for patron, tipo in self.patrones_compilados:
                    match = patron.match(linea, pos)
                    if match:
                        if tipo != 'ESPACIO':  # Ignorar espacios
                            valor = match.group(0)
                            token = Token(tipo, valor)
                            self.tokens.append(token)
                            self.imprimir_token(token)  # Imprimir el token
                        pos = match.end(0)
                        break
                if not match:
                    raise Exception(f"Error de tokenización en la línea: {linea}")
        return self.tokens
    
    def imprimir_token(self, token):
        print(f"Token: Tipo='{token.tipo}', Valor='{token.valor}'")