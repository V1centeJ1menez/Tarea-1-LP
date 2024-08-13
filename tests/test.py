import re


# ANALISIS LEXICO #

# Clase Token

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

# Nodo AST
class NodoAST:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.variables = {}

    def error(self):
        raise Exception("Error de análisis sintáctico")

    def consumir(self, tipo_token):
        if self.pos < len(self.tokens) and self.tokens[self.pos].tipo == tipo_token:
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        else:
            self.error()

    def programa(self):
        nodos = []
        while self.pos < len(self.tokens):
            nodos.append(self.linea())
        return nodos
    
    #   Esto  funciona
    def linea(self):
        if self.tokens[self.pos].tipo == 'DEFINE':
            return self.declaracion()
        elif self.tokens[self.pos].tipo == 'DP':
            return self.procesar()
        elif self.tokens[self.pos].tipo == 'IF':
            return self.condicional()
        elif self.tokens[self.pos].tipo == 'MOSTRAR':
            return self.mostrar()
        else:
            self.error()
    
    #   Esto  funciona
    def declaracion(self):
        self.consumir('DEFINE')
        variable = self.consumir('VARIABLE').valor
        self.variables[variable] = None
        return NodoAST('Declaracion', variable)

    #   Esto  funciona
    def procesar(self):
        self.consumir('DP')
        variable = self.consumir('VARIABLE').valor
        if self.tokens[self.pos].tipo == 'OPER_UN':
            operacion = self.consumir('OPER_UN').valor
            operando = self.operando()
            self.variables[variable] = operando.valor
            nodo_procesar = NodoAST('Procesar', operacion)
            nodo_procesar.agregar_hijo(NodoAST('Variable', variable))
            nodo_procesar.agregar_hijo(operando)
            return nodo_procesar
        elif self.tokens[self.pos].tipo == 'OPER_BIN':
            operacion = self.consumir('OPER_BIN').valor
            operando1 = self.operando()
            operando2 = self.operando()
            if operacion == '+':
                self.variables[variable] = operando1.valor + operando2.valor
            elif operacion == '*':
                self.variables[variable] = operando1.valor * operando2.valor
            elif operacion == '>':
                self.variables[variable] = operando1.valor > operando2.valor
            elif operacion == '==':
                self.variables[variable] = operando1.valor == operando2.valor
            nodo_procesar = NodoAST('Procesar', operacion)
            nodo_procesar.agregar_hijo(NodoAST('Variable', variable))
            nodo_procesar.agregar_hijo(operando1)
            nodo_procesar.agregar_hijo(operando2)
            return nodo_procesar
        else:
            self.error()

    def operando(self):
        if self.tokens[self.pos].tipo == 'VARIABLE':
            variable = self.consumir('VARIABLE').valor
            return NodoAST('Variable', self.variables[variable])
        elif self.tokens[self.pos].tipo == 'ENTERO':
            return NodoAST('Entero', int(self.consumir('ENTERO').valor))
        elif self.tokens[self.pos].tipo == 'BOOLEANO':
            valor = self.consumir('BOOLEANO').valor
            return NodoAST('Booleano', valor == 'True')
        elif self.tokens[self.pos].tipo == 'STRING':
            return NodoAST('String', self.consumir('STRING').valor.strip('#'))
        else:
            self.error()

    def condicional(self):
        self.consumir('IF')
        self.consumir('PAR_ABR')
        variable = self.consumir('VARIABLE').valor
        self.consumir('PAR_CER')
        self.consumir('LLAVE_ABR')
        linea_if = self.linea()
        self.consumir('LLAVE_CER')
        self.consumir('ELSE')
        self.consumir('LLAVE_ABR')
        linea_else = self.linea()
        self.consumir('LLAVE_CER')
        if self.variables[variable]:
            return linea_if
        else:
            return linea_else

    def mostrar(self):
        self.consumir('MOSTRAR')
        self.consumir('PAR_ABR')
        variable = self.consumir('VARIABLE').valor
        self.consumir('PAR_CER')
        with open('output.txt', 'w') as f:
            f.write(str(self.variables[variable]))
        return NodoAST('Mostrar', variable)


# Main

if __name__ == "__main__":

    # Leer el archivo codigo.txt
    with open('tests/operaciones_binarias.txt', 'r') as f:
        codigo_fuente = f.readlines()

    # Definir patrones de tokens
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

    # Tokenización
    tokenizer = Tokenizer(codigo_fuente)
    tokens = tokenizer.tokenizar()

    # Análisis sintáctico
    parser = Parser(tokens)
    ast = parser.programa()
