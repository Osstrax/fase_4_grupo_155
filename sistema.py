import logging

from excepciones import (
    ErrorSistema,
    DatoInvalidoError,
    ReservaInvalidaError
)
from modelos import Cliente, Servicio, Reserva


# Configuración del archivo de bitácora para registrar eventos y fallos
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


class SoftwareFJ:
    # Controlador central que gestiona el negocio en memoria sin base de datos
    def __init__(self):
        # Listas privadas para almacenar las entidades en memoria
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        logging.info("Sistema Software FJ iniciado en memoria.")

    def registrar_cliente(self, cliente):
        # Registra un nuevo cliente validando que sea el objeto adecuado y que no esté duplicado
        try:
            if not isinstance(cliente, Cliente):
                raise DatoInvalidoError("Objeto cliente incorrecto.")

            # Comprobamos si ya existe un cliente con el mismo ID
            if any(c.identificador == cliente.identificador for c in self.__clientes):
                raise DatoInvalidoError("El cliente ya esta registrado.")

            self.__clientes.append(cliente)
            logging.info("Cliente registrado: %s (%s)", cliente.nombre, cliente.identificador)
            print("Cliente registrado correctamente.")

        except ErrorSistema as error:
            logging.error("Error al registrar cliente: %s", error)
            print(f"Error controlado: {error}")

    def registrar_servicio(self, servicio):
        # Registra un servicio en el catálogo validando que no se repita el ID
        try:
            if not isinstance(servicio, Servicio):
                raise DatoInvalidoError("Servicio incorrecto.")

            if any(s.identificador == servicio.identificador for s in self.__servicios):
                raise DatoInvalidoError("El servicio ya existe.")

            self.__servicios.append(servicio)
            logging.info("Servicio registrado: %s (%s)", servicio.nombre, servicio.identificador)
            print("Servicio registrado correctamente.")

        except ErrorSistema as error:
            logging.error("Error al registrar servicio: %s", error)
            print(f"Error controlado: {error}")

    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion, **kwargs):
        # Crea y vincula una reserva buscando el cliente y el servicio por su ID
        try:
            # Búsqueda en listas internas mediante coincidencia de identificador
            cliente = next((c for c in self.__clientes if c.identificador == str(id_cliente)), None)
            servicio = next((s for s in self.__servicios if s.identificador == str(id_servicio)), None)

            if cliente is None:
                raise ReservaInvalidaError("El cliente solicitado no existe.")

            if servicio is None:
                raise ReservaInvalidaError("El servicio solicitado no existe.")

            if any(r.identificador == str(identificador) for r in self.__reservas):
                raise ReservaInvalidaError("El identificador de reserva ya existe.")

            # Instanciamos la reserva con las fichas encontradas
            reserva = Reserva(identificador, cliente, servicio, duracion, **kwargs)
            self.__reservas.append(reserva)

            logging.info("Reserva creada con ID %s para cliente %s", identificador, id_cliente)
            print("Reserva creada correctamente.")
            return reserva

        except ErrorSistema as error:
            # Control de errores esperados del dominio
            logging.error("Error controlado creando reserva: %s", error)
            raise

        except Exception as error:
            # Captura de cualquier fallo inesperado y encadenamiento con raise ... from
            logging.exception("Fallo imprevisto durante la creacion de la reserva.")
            raise ErrorSistema("No se pudo crear la reserva debido a un fallo interno.") from error

    # Métodos informativos para listar el estado actual del negocio
    def listar_clientes(self):
        print("\n--- LISTA DE CLIENTES REGISTRADOS ---")
        for cliente in self.__clientes:
            print(cliente.mostrar_informacion())

    def listar_servicios(self):
        print("\n--- CATÁLOGO DE SERVICIOS ---")
        for servicio in self.__servicios:
            print(servicio.mostrar_informacion())
            print(f"  Detalle: {servicio.describir_servicio()}")

    def listar_reservas(self):
        print("\n--- HISTORIAL DE RESERVAS ---")
        for reserva in self.__reservas:
            print(reserva.mostrar_informacion())