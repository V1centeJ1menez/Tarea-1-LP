class Executor:
    def __init__(self):
        self.variables = {}  # Almacena las variables definidas

    def ejecutar(self, nodo):
        if nodo.tipo == "Programa":
            for hijo in nodo.hijos:
                self.ejecutar(hijo)
        elif nodo.tipo == "Linea":
            for hijo in nodo.hijos:
                self.ejecutar(hijo)
        elif nodo.tipo == "Declaracion":
            self.declarar_variable(nodo)
        elif nodo.tipo == "Procesar":
            self.procesar_variable(nodo)
        elif nodo.tipo == "Mostrar":
            self.mostrar_variable(nodo)
        elif nodo.tipo == "Condicional":
            self.ejecutar_condicional(nodo)
        elif nodo.tipo == "Else":
            for hijo in nodo.hijos:
                self.ejecutar(hijo)

    def declarar_variable(self, nodo):
        variable = nodo.hijos[0].valor  # Obtener el nombre de la variable
        self.variables[variable] = None  # Inicialmente, la variable no tiene valor
        print(f"Variable '{variable}' declarada.")

    def procesar_variable(self, nodo):
        variable = nodo.hijos[0].valor  # Obtener el nombre de la variable
        operador = nodo.hijos[1].valor  # Obtener el operador
        operandos = nodo.hijos[2:]  # Obtener los operandos

        if operador == 'ASIG':
            valor = self.obtener_valor(operandos[0])  # Obtener el valor del primer operando
            self.variables[variable] = valor  # Asignar valor a la variable
            print(f"Asignado: {variable} = {valor}")

        # Manejar operadores binarios y unarios aquí según sea necesario

    def mostrar_variable(self, nodo):
        variable = nodo.hijos[0].valor  # Obtener el nombre de la variable
        if variable in self.variables:
            print(f"{variable} = {self.variables[variable]}")
        else:
            raise Exception(f"Error: Variable '{variable}' no definida.")

    def ejecutar_condicional(self, nodo):
        condicion = nodo.hijos[0].valor  # Obtener la condición
        if self.obtener_valor(condicion):
            for hijo in nodo.hijos[1:]:
                self.ejecutar(hijo)  # Ejecutar el bloque if
        elif len(nodo.hijos) > 1 and nodo.hijos[-1].tipo == "Else":
            self.ejecutar(nodo.hijos[-1])  # Ejecutar el bloque else

    def obtener_valor(self, operando):
        if operando.tipo == "Variable":
            return self.variables.get(operando.valor, None)
        elif operando.tipo == "Entero":
            return int(operando.valor)
        elif operando.tipo == "Booleano":
            return operando.valor == 'True'
        elif operando.tipo == "String":
            return operando.valor.strip('#')  # Eliminar los símbolos de número
        else:
            raise Exception(f"Error: tipo de operando no reconocido: {operando.tipo}")
