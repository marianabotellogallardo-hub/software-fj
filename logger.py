"""
Módulo de registro (logs) de Software FJ.
Guarda eventos y errores en el archivo 'registro.log'.
"""

# Librería que ya viene con Python para registrar mensajes en archivos
import logging

# Configuración general del registro. Se ejecuta una sola vez, al importar este módulo.
logging.basicConfig(
    filename="registro.log",  # Archivo donde se guardan todos los mensajes
    level=logging.INFO,  # Nivel mínimo: guarda INFO, WARNING, ERROR y CRITICAL
    format="%(asctime)s | %(levelname)s | %(message)s",  # Fecha y hora | tipo | mensaje
    encoding="utf-8",  # Permite guardar tildes y la letra ñ sin problemas
)

# Objeto que usan los demás archivos para escribir en el log.
# Ejemplo: logger.info("algo pasó") o logger.error("algo falló")
logger = logging.getLogger("SoftwareFJ")