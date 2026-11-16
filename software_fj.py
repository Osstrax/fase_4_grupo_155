# Modulo fachada para mantener retrocompatibilidad con pruebas unitarias y ejecuciones directas
from excepciones import *
from modelos import *
from sistema import *


if __name__ == "__main__":
    from main import ejecutar_pruebas
    ejecutar_pruebas()