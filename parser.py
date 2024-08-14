class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.max_if_depth = 4
        self.current_if_depth = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None  # Devolver None si no hay más tokens

    def consume(self):
        self.pos += 1

    def expect(self, tipo_token):
        if self.pos < len(self.tokens) and self.current_token().tipo == tipo_token:
            self.consume()
        else:
            raise Exception(f"Error de sintaxis: se esperaba '{tipo_token}' en línea {self.current_token().linea if self.current_token() else 'desconocida'}")

    def parse(self):
        previous_was_newline = False  # Variable para rastrear saltos de línea
        while self.pos < len(self.tokens):
            token = self.current_token()

            if token.tipo == 'NUEVA_LINEA':
                if previous_was_newline:  # Verificar si hay dos saltos de línea consecutivos
                    raise Exception(f"Error de sintaxis: línea vacía detectada en línea {token.linea}")
                previous_was_newline = True  # Marcar que encontramos un salto de línea
                self.consume()  # Consumir el salto de línea
                continue  # Saltar a la siguiente iteración

            previous_was_newline = False  # Reiniciar si encontramos un token que no sea un salto de línea
            self.linea()  # Procesar la línea

    def linea(self):
        token = self.current_token()
        if token is None:
            return  # Salir si no hay más tokens

        if token.tipo == 'DEFINE':
            self.declaracion()
        elif token.tipo == 'DP':
            self.procesar()
        elif token.tipo == 'MOSTRAR':
            self.mostrar()
        elif token.tipo == 'IF':
            self.condicional()
        elif token.tipo == 'NUEVA_LINEA':
            self.consume()  # Consumir la nueva línea
        else:
            raise Exception(f"Error de sintaxis: declaración desconocida en línea {token.linea} = {token.valor}")

    def declaracion(self):
        self.expect('DEFINE')
        self.expect('VARIABLE')

    def procesar(self):
        self.expect('DP')
        self.expect('VARIABLE')

        if self.current_token().tipo == 'OPER_UN':
            self.expect('OPER_UN')
            self.operando()
        elif self.current_token().tipo == 'OPER_BIN':
            self.expect('OPER_BIN')
            self.operando()
            self.operando()
        else:
            raise Exception(f"Error de sintaxis: operación no válida en línea {self.current_token().linea}")

    def mostrar(self):
        self.expect('MOSTRAR')
        self.expect('PAR_ABR')
        self.expect('VARIABLE')
        self.expect('PAR_CER')

    def operando(self):
        token = self.current_token()
        if token.tipo in ['VARIABLE', 'ENTERO', 'BOOLEANO', 'STRING']:
            self.expect(token.tipo)
        else:
            raise Exception(f"Error de sintaxis: operando no válido en línea {token.linea}")

    def condicional(self):
        if self.current_if_depth >= self.max_if_depth:
            raise Exception(f"Error de sintaxis: se excedió el máximo de {self.max_if_depth} if anidados")

        self.expect('IF')
        self.expect('PAR_ABR')

        # Verificar que hay un token actual antes de acceder a su tipo
        if self.current_token() is None:
            raise Exception("Error de sintaxis: se esperaba una variable en la condición del 'if'")

        self.expect('VARIABLE')  # Se espera que la condición sea una variable
        self.expect('PAR_CER')
        self.current_if_depth += 1

        # Parsear el bloque de código dentro del if
        self.expect('LLAVE_ABR')  # Esperamos la llave de apertura del bloque if

        # Verificar si hay más tokens
        while self.pos < len(self.tokens) and self.current_token() is not None and self.current_token().tipo != 'LLAVE_CER':
            self.linea()

        self.expect('LLAVE_CER')  # Esperamos la llave de cierre del bloque if
        self.current_if_depth -= 1

        # Comprobar si hay un else correspondiente
        if self.pos < len(self.tokens) and self.current_token() and self.current_token().tipo == 'ELSE':
            self.expect('ELSE')
            self.expect('LLAVE_ABR')
            # Parsear el bloque de código dentro del else
            while self.pos < len(self.tokens) and self.current_token() and self.current_token().tipo != 'LLAVE_CER':
                self.linea()
            self.expect('LLAVE_CER')
        else:
            raise Exception(f"Error de sintaxis: se esperaba 'else' después del 'if' en línea {self.current_token().linea if self.current_token() else 'desconocida'}")
