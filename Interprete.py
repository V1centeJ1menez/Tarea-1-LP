from tokenizer import Tokenizer

if __name__ == "__main__":

    # Leer el archivo codigo.txt
    with open('codigo.txt', 'r') as f:
        codigo_fuente = f.readlines()

    # Tokenización
    tokenizer = Tokenizer(codigo_fuente)
    tokens = tokenizer.tokenizar()