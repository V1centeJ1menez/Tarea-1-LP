from tokenizer import Tokenizer
from parser import Parser

def main():

    # Leer el archivo codigo.txt
    with open('codigo.txt', 'r') as f:
        codigo_fuente = f.readlines()

    # Tokenización
    tokenizer = Tokenizer(codigo_fuente)
    tokens = tokenizer.tokenizar()
    contador = 0

    for token in tokens:
        contador += 1
        print(f"Token nº{contador}: Tipo='{token.tipo}', Valor='{token.valor}', Línea={token.linea}")


    parser = Parser(tokens)
    parser.parse()
    print("El código es sintácticamente correcto.")
   

if __name__ == "__main__":
    main()