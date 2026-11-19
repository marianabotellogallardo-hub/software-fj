"""
Módulo de registro (logs) de Software FJ.
Guarda eventos y errores en el archivo 'registro.log'.
"""

import logging

# Configuración del logger: archivo de salida, nivel y formato de cada línea
logging.basicConfig(
    filename="registro.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

# Objeto logger que usaremos en todo el proyecto
logger = logging.getLogger("SoftwareFJ")