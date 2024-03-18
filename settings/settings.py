import logging

# Configurar el sistema de registro
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Configurar el nivel de registro según sea necesario

# Crear un manejador que envíe los registros a la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Configurar el nivel del manejador según sea necesario

# Crear un formato para los registros
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Agregar el manejador al logger
logger.addHandler(console_handler)

# Ejemplo de uso del logger en la librería
def funcion_ejemplo():
    logger.debug('Este es un mensaje de depuración')
    logger.info('Este es un mensaje informativo')
    logger.warning('Este es un mensaje de advertencia')
    logger.error('Este es un mensaje de error')
    logger.critical('Este es un mensaje crítico')
