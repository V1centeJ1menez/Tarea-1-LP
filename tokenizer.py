import re

''' 
    TOKENIZER - LEXER ( Analisis Lexico ) 

-> Generar patrones con el uso de expresiones regulares.
-> Luego generar tokens

'''


patrones = {
    
# DECLARACIÓN DE VARIABLES #
'DECLARATION_REGEX': r'\bDEFINE\b',

# Tipos de Datos

'INT_REGEX': r'\b(0|[1-9]\d*)\b',
'BOOL_REGEX': r'\b(True|False)\b',
'STRING_REGEX': r'(#\s*(.*?)\s*#)',
'VARIABLE_REGEX': r'\$_[A-Z][a-zA-Z]*'
}