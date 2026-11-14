from abc import ABC, abstractmethod
from datetime import datetime
import logging
import math


# ==========================================================
# 1. CONFIGURACION DEL ARCHIVO DE REGISTROS
# ==========================================================

# Configura el sistema de logs para registrar eventos y errores en un archivo
logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ==========================================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==========================================================

class ErrorSistema(Exception):
    """Excepción base para todos los errores controlados del sistema Software FJ."""
    pass


class DatoInvalidoError(ErrorSistema):
    """Excepción lanzada cuando un dato ingresado no cumple con las validaciones."""
    pass


class ServicioNoDisponibleError(ErrorSistema):
    """Excepción lanzada cuando se intenta usar un servicio marcado como no disponible."""
    pass


class ReservaInvalidaError(ErrorSistema):
    """Excepción lanzada cuando los parámetros de una reserva son incorrectos."""
    pass


class OperacionNoPermitidaError(ErrorSistema):
    """Excepción lanzada cuando se intenta realizar una acción no permitida según el estado."""
    pass


# ==========================================================
# 3. CLASE ABSTRACTA ENTIDAD
# ==========================================================

class Entidad(ABC):
    """
    Clase abstracta base que representa entidades generales del sistema.
    Provee la estructura básica para el identificador único.
    """

    def __init__(self, identificador):
        """
        Inicializa una entidad con un identificador único.

        Args:
            identificador (str): ID único de la entidad (no puede estar vacío).

        Raises:
            DatoInvalidoError: Si el identificador está vacío o no es una cadena.
        """
        # Validación: el identificador debe ser texto y no estar vacío
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatoInvalidoError(
                "El identificador no puede estar vacio."
            )

        self._identificador = identificador.strip()

    @property
    def identificador(self):
        """Retorna el identificador único de la entidad."""
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        """Método abstracto para mostrar la información de la entidad."""
        pass


# ==========================================================
# 4. CLASE CLIENTE
# ==========================================================

class Cliente(Entidad):
    """
    Representa a un cliente de Software FJ.
    Encapsula los datos personales y valida estrictamente su formato.
    """

    def __init__(self, identificador, nombre, correo, telefono):
        """
        Inicializa un nuevo cliente con validaciones robustas.

        Args:
            identificador (str): ID único del cliente.
            nombre (str): Nombre completo (no vacío).
            correo (str): Correo electrónico (formato válido usuario@dominio.ext).
            telefono (str): Número de teléfono (solo dígitos, entre 7 y 15).

        Raises:
            DatoInvalidoError: Si algún parámetro no cumple las reglas.
        """
        super().__init__(identificador)

        # Validación del nombre: debe ser texto no vacío
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre es obligatorio.")

        # Validación del correo: exactamente una '@' y un '.' en el dominio
        if (
            not isinstance(correo, str)
            or correo.count("@") != 1
            or "." not in correo.split("@")[1]
        ):
            raise DatoInvalidoError("El correo no es valido.")

        # Validación del teléfono: solo dígitos y longitud entre 7 y 15
        if (
            not isinstance(telefono, str)
            or not telefono.isdigit()
            or not 7 <= len(telefono) <= 15
        ):
            raise DatoInvalidoError("El telefono no es valido.")

        # Atributos privados (encapsulación)
        self.__nombre = nombre.strip()
        self.__correo = correo.strip().lower()
        self.__telefono = telefono

    @property
    def nombre(self):
        """Retorna el nombre del cliente."""
        return self.__nombre

    @property
    def correo(self):
        """Retorna el correo del cliente."""
        return self.__correo

    @property
    def telefono(self):
        """Retorna el teléfono del cliente."""
        return self.__telefono

    def mostrar_informacion(self):
        """Retorna una cadena con la información formateada del cliente."""
        return (
            f"ID: {self.identificador} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Telefono: {self.telefono}"
        )


# ==========================================================
# 5. CLASE ABSTRACTA SERVICIO
# ==========================================================

class Servicio(Entidad):
    """
    Clase abstracta que representa un servicio ofrecido por Software FJ.
    Define la estructura base para el cálculo de costos y disponibilidad.
    """

    def __init__(self, identificador, nombre, tarifa_base):
        """
        Inicializa un servicio con su tarifa base.

        Args:
            identificador (str): ID único del servicio.
            nombre (str): Nombre del servicio.
            tarifa_base (float/int): Costo por hora (debe ser mayor a cero).

        Raises:
            DatoInvalidoError: Si el nombre está vacío o la tarifa es inválida.
        """
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")

        # Validación de tarifa: debe ser numérica, finita y mayor que cero
        if (
            isinstance(tarifa_base, bool)
            or not isinstance(tarifa_base, (int, float))
            or not math.isfinite(tarifa_base)
            or tarifa_base <= 0
        ):
            raise DatoInvalidoError("La tarifa debe ser mayor que cero.")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = True

    @property
    def nombre(self):
        """Retorna el nombre del servicio."""
        return self._nombre

    @property
    def tarifa_base(self):
        """Retorna la tarifa base por hora del servicio."""
        return self._tarifa_base

    @property
    def disponible(self):
        """Retorna el estado de disponibilidad del servicio."""
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        """
        Cambia el estado de disponibilidad del servicio y lo registra en el log.

        Args:
            estado (bool): True para disponible, False para no disponible.
        """
        if not isinstance(estado, bool):
            raise DatoInvalidoError("Estado de disponibilidad incorrecto.")

        self._disponible = estado

        logging.info(
            "Disponibilidad del servicio %s: %s",
            self.nombre,
            estado
        )

    def validar_disponibilidad(self):
        """
        Verifica que el servicio esté disponible antes de usarlo.
        
        Raises:
            ServicioNoDisponibleError: Si el servicio no está disponible.
        """
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.nombre} no esta disponible."
            )

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """
        Calcula el costo total del servicio.
        Simula sobrecarga mediante parámetros opcionales.

        Args:
            duracion (float): Horas de servicio (debe ser positiva).
            descuento (float): Porcentaje de descuento (0 a 100).
            impuesto (float): Porcentaje de impuesto (0 a 100).

        Returns:
            float: Costo total redondeado a 2 decimales.

        Raises:
            DatoInvalidoError: Si la duración, descuento o impuesto son inválidos.
            ErrorSistema: Si el cálculo resulta en un valor inconsistente.
        """
        self.validar_disponibilidad()

        # Validación de duración
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not math.isfinite(duracion)
            or duracion <= 0
        ):
            raise DatoInvalidoError("La duracion debe ser positiva.")

        # Validación de descuento
        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise DatoInvalidoError("El descuento debe estar entre 0 y 100.")

        # Validación de impuesto
        if (
            isinstance(impuesto, bool)
            or not isinstance(impuesto, (int, float))
            or not math.isfinite(impuesto)
            or not 0 <= impuesto <= 100
        ):
            raise DatoInvalidoError("El impuesto debe estar entre 0 y 100.")

        # Cálculos matemáticos
        subtotal = self._tarifa_base * duracion
        valor_descuento = subtotal * descuento / 100
        subtotal_final = subtotal - valor_descuento
        total = subtotal_final * (1 + impuesto / 100)

        # Verificación final de consistencia
        if not math.isfinite(total) or total < 0:
            raise ErrorSistema("El calculo del costo es inconsistente.")

        return round(total, 2)

    @abstractmethod
    def validar_parametros(self, **kwargs):
        """Método abstracto para validar parámetros específicos de cada servicio."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Método abstracto para obtener una descripción del servicio."""
        pass

    @abstractmethod
    def mostrar_informacion(self):
        """Método abstracto para mostrar la información del servicio."""
        pass


# ==========================================================
# 6. SERVICIO DE RESERVA DE SALAS
# ==========================================================

class ReservaSala(Servicio):
    """
    Servicio especializado para la reserva de salas.
    Hereda de Servicio y aplica polimorfismo.
    """

    def validar_parametros(self, **kwargs):
        """
        Valida que se especifique una capacidad válida para la sala.

        Raises:
            DatoInvalidoError: Si la capacidad no es un entero positivo.
        """
        capacidad = kwargs.get("capacidad")

        if (
            isinstance(capacidad, bool)
            or not isinstance(capacidad, int)
            or capacidad <= 0
        ):
            raise DatoInvalidoError("La capacidad de la sala es invalida.")

        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Sobrescribe el cálculo de costo para salas."""
        self.validar_disponibilidad()
        return super().calcular_costo(duracion, descuento, impuesto)

    def describir_servicio(self):
        """Retorna la descripción específica de las salas."""
        return "Reserva de salas para reuniones y eventos."

    def mostrar_informacion(self):
        """Retorna la información formateada de la sala."""
        return (
            f"Servicio: {self.nombre} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f} | "
            f"Disponible: {self.disponible}"
        )


# ==========================================================
# 7. SERVICIO DE ALQUILER DE EQUIPOS
# ==========================================================

class AlquilerEquipo(Servicio):
    """
    Servicio especializado para el alquiler de equipos tecnológicos.
    Hereda de Servicio y aplica polimorfismo.
    """

    def validar_parametros(self, **kwargs):
        """
        Valida que se especifique el nombre del equipo.

        Raises:
            DatoInvalidoError: Si no se indica el equipo o está vacío.
        """
        equipo = kwargs.get("equipo")

        if not isinstance(equipo, str) or not equipo.strip():
            raise DatoInvalidoError("Debe indicar el equipo solicitado.")

        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Sobrescribe el cálculo de costo para equipos."""
        self.validar_disponibilidad()
        return super().calcular_costo(duracion, descuento, impuesto)

    def describir_servicio(self):
        """Retorna la descripción específica de los equipos."""
        return "Alquiler de equipos tecnologicos."

    def mostrar_informacion(self):
        """Retorna la información formateada del equipo."""
        return (
            f"Servicio: {self.nombre} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f} | "
            f"Disponible: {self.disponible}"
        )


# ==========================================================
# 8. SERVICIO DE ASESORIAS ESPECIALIZADAS
# ==========================================================

class AsesoriaEspecializada(Servicio):
    """
    Servicio especializado para asesorías.
    Hereda de Servicio y aplica polimorfismo.
    """

    def validar_parametros(self, **kwargs):
        """
        Valida que se especifique la especialidad requerida.

        Raises:
            DatoInvalidoError: Si la especialidad está vacía.
        """
        especialidad = kwargs.get("especialidad")

        if (
            not isinstance(especialidad, str)
            or not especialidad.strip()
        ):
            raise DatoInvalidoError("Debe indicar la especialidad.")

        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Sobrescribe el cálculo de costo para asesorías."""
        self.validar_disponibilidad()
        return super().calcular_costo(duracion, descuento, impuesto)

    def describir_servicio(self):
        """Retorna la descripción específica de las asesorías."""
        return "Asesorias profesionales especializadas."

    def mostrar_informacion(self):
        """Retorna la información formateada de la asesoría."""
        return (
            f"Servicio: {self.nombre} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f} | "
            f"Disponible: {self.disponible}"
        )


# ==========================================================
# 9. CLASE RESERVA
# ==========================================================

class Reserva(Entidad):
    """
    Representa una reserva que integra un cliente, un servicio, duración y estado.
    Gestiona la confirmación, cancelación y procesamiento de la misma.
    """

    def __init__(self, identificador, cliente, servicio, duracion, **kwargs):
        """
        Inicializa una reserva validando cliente, servicio y duración.

        Args:
            identificador (str): ID único de la reserva.
            cliente (Cliente): Objeto cliente válido.
            servicio (Servicio): Objeto servicio válido.
            duracion (float): Horas de reserva (positivas).
            **kwargs: Parámetros específicos del servicio (ej. capacidad, equipo).

        Raises:
            ReservaInvalidaError: Si los datos base no son válidos.
        """
        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente no es valido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio no es valido.")

        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not math.isfinite(duracion)
            or duracion <= 0
        ):
            raise ReservaInvalidaError("La duracion no es valida.")

        # Se validan los parámetros específicos del servicio heredado
        servicio.validar_parametros(**kwargs)

        # Atributos privados
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = float(duracion)
        self.__estado = "Pendiente"
        self.__costo = 0.0
        self.__fecha = datetime.now()

    @property
    def estado(self):
        """Retorna el estado actual de la reserva."""
        return self.__estado

    @property
    def costo(self):
        """Retorna el costo calculado de la reserva."""
        return self.__costo

    def confirmar(self, descuento=0, impuesto=0):
        """
        Confirma la reserva calculando su costo. Utiliza try/except y encadenamiento.
        """
        try:
            # Validación de estado
            if self.__estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    "La reserva no se encuentra pendiente."
                )

            # Cálculo del costo
            costo = self.__servicio.calcular_costo(
                self.__duracion,
                descuento,
                impuesto
            )

            self.__costo = costo
            self.__estado = "Confirmada"

            logging.info(
                "Reserva %s confirmada. Costo: %.2f",
                self.identificador,
                self.__costo
            )

            print("Reserva confirmada correctamente.")
            print(f"Costo total: ${self.__costo:,.2f}")

        except ErrorSistema as error:
            logging.error(
                "Error al confirmar reserva %s: %s",
                self.identificador,
                error
            )
            raise

        except Exception as error:
            # Encadenamiento de excepciones
            logging.exception("Error inesperado al confirmar.")
            raise ErrorSistema(
                "No fue posible confirmar la reserva."
            ) from error

    def cancelar(self):
        """Cancela la reserva si su estado lo permite."""
        try:
            if self.__estado not in ("Pendiente", "Confirmada"):
                raise OperacionNoPermitidaError(
                    "No se puede cancelar esta reserva."
                )

            self.__estado = "Cancelada"
            logging.info("Reserva %s cancelada.", self.identificador)
            print("Reserva cancelada correctamente.")

        except ErrorSistema as error:
            logging.error("Error al cancelar: %s", error)
            raise

    def procesar(self):
        """
        Procesa la reserva (intenta confirmarla).
        Demuestra el uso de try/except/else/finally.
        """
        try:
            self.confirmar()
        except ErrorSistema:
            print("No fue posible procesar la reserva.")
            raise
        else:
            print("Procesamiento exitoso.")
        finally:
            print("Finalizo el intento de procesamiento.")

    def mostrar_informacion(self):
        """Retorna los detalles formateados de la reserva."""
        return (
            f"\nReserva: {self.identificador}\n"
            f"Cliente: {self.__cliente.nombre}\n"
            f"Servicio: {self.__servicio.nombre}\n"
            f"Duracion: {self.__duracion} horas\n"
            f"Fecha: {self.__fecha.strftime('%d/%m/%Y %H:%M')}\n"
            f"Estado: {self.__estado}\n"
            f"Costo: ${self.__costo:,.2f}\n"
        )


# ==========================================================
# 10. SISTEMA PRINCIPAL SOFTWARE FJ
# ==========================================================

class SoftwareFJ:
    """
    Sistema principal que gestiona clientes, servicios y reservas utilizando listas internas.
    No utiliza base de datos.
    """

    def __init__(self):
        """Inicializa las listas vacías para almacenar los objetos."""
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    def registrar_cliente(self, cliente):
        """Registra un cliente en el sistema, validando que no esté duplicado."""
        try:
            if not isinstance(cliente, Cliente):
                raise DatoInvalidoError("Objeto cliente incorrecto.")

            if any(c.identificador == cliente.identificador for c in self.__clientes):
                raise DatoInvalidoError("El cliente ya esta registrado.")

            self.__clientes.append(cliente)
            logging.info("Cliente registrado: %s", cliente.nombre)
            print("Cliente registrado correctamente.")

        except ErrorSistema as error:
            logging.error("Error registrando cliente: %s", error)
            print(f"Error controlado: {error}")

    def registrar_servicio(self, servicio):
        """Registra un servicio en el sistema, validando que no exista."""
        try:
            if not isinstance(servicio, Servicio):
                raise DatoInvalidoError("Servicio incorrecto.")

            if any(s.identificador == servicio.identificador for s in self.__servicios):
                raise DatoInvalidoError("El servicio ya existe.")

            self.__servicios.append(servicio)
            logging.info("Servicio registrado: %s", servicio.nombre)
            print("Servicio registrado correctamente.")

        except ErrorSistema as error:
            logging.error("Error registrando servicio: %s", error)
            print(f"Error controlado: {error}")

    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion, **kwargs):
        """Crea una reserva buscando al cliente y el servicio por su ID."""
        try:
            cliente = next(
                (c for c in self.__clientes if c.identificador == str(id_cliente)),
                None
            )
            servicio = next(
                (s for s in self.__servicios if s.identificador == str(id_servicio)),
                None
            )

            if cliente is None:
                raise ReservaInvalidaError("El cliente solicitado no existe.")

            if servicio is None:
                raise ReservaInvalidaError("El servicio solicitado no existe.")

            if any(r.identificador == str(identificador) for r in self.__reservas):
                raise ReservaInvalidaError("El identificador de reserva ya existe.")

            reserva = Reserva(identificador, cliente, servicio, duracion, **kwargs)
            self.__reservas.append(reserva)
            logging.info("Reserva creada: %s", identificador)
            print("Reserva creada correctamente.")

            return reserva

        except ErrorSistema as error:
            logging.error("Error creando reserva: %s", error)
            raise

        except Exception as error:
            logging.exception("Error inesperado creando reserva.")
            raise ErrorSistema("No se pudo crear la reserva.") from error

    def listar_clientes(self):
        """Imprime en consola todos los clientes registrados."""
        print("\n========== LISTA DE CLIENTES ==========")
        for cliente in self.__clientes:
            print(cliente.mostrar_informacion())

    def listar_servicios(self):
        """Imprime en consola todos los servicios registrados."""
        print("\n========== LISTA DE SERVICIOS ==========")
        for servicio in self.__servicios:
            print(servicio.mostrar_informacion())
            print(servicio.describir_servicio())
            print("--------------------------------------")

    def listar_reservas(self):
        """Imprime en consola todas las reservas registradas."""
        print("\n========== LISTA DE RESERVAS ==========")
        for reserva in self.__reservas:
            print(reserva.mostrar_informacion())


# ==========================================================
# 11. PRUEBAS AUTOMATICAS DEL SISTEMA
# ==========================================================

def ejecutar_pruebas():
    """
    Ejecuta 20 operaciones completas (válidas e inválidas) para demostrar
    la estabilidad, robustez y el manejo de excepciones del sistema.
    """
    sistema = SoftwareFJ()

    print("\n" + "=" * 60)
    print("       SISTEMA INTEGRAL DE GESTION SOFTWARE FJ")
    print("=" * 60)

    # OPERACION 1: Registro válido
    print("\nOPERACION 1: Registro de cliente.")
    cliente1 = Cliente("C001", "Carlos Ramirez", "carlos@gmail.com", "3001234567")
    sistema.registrar_cliente(cliente1)

    # OPERACION 2: Registro válido
    print("\nOPERACION 2: Registro de segundo cliente.")
    cliente2 = Cliente("C002", "Maria Lopez", "maria@gmail.com", "3101234567")
    sistema.registrar_cliente(cliente2)

    # OPERACION 3: Registro inválido (fuerza error)
    print("\nOPERACION 3: Registro de cliente invalido.")
    try:
        cliente3 = Cliente("C003", "", "correo incorrecto", "abc123")
        sistema.registrar_cliente(cliente3)
    except ErrorSistema as error:
        logging.error("Cliente invalido: %s", error)
        print(f"Error controlado: {error}")

    # OPERACION 4: Registro duplicado
    print("\nOPERACION 4: Registro de cliente duplicado.")
    cliente_duplicado = Cliente("C001", "Pedro Gomez", "pedro@gmail.com", "3201234567")
    sistema.registrar_cliente(cliente_duplicado)

    # OPERACION 5: Servicio válido
    print("\nOPERACION 5: Registro de sala.")
    sala = ReservaSala("S001", "Sala de reuniones", 50000)
    sistema.registrar_servicio(sala)

    # OPERACION 6: Servicio válido
    print("\nOPERACION 6: Registro de equipo.")
    equipo = AlquilerEquipo("S002", "Computador portatil", 25000)
    sistema.registrar_servicio(equipo)

    # OPERACION 7: Servicio válido
    print("\nOPERACION 7: Registro de asesoria.")
    asesoria = AsesoriaEspecializada("S003", "Asesoria informatica", 80000)
    sistema.registrar_servicio(asesoria)

    # OPERACION 8: Servicio inválido (tarifa negativa)
    print("\nOPERACION 8: Creacion de servicio invalido.")
    try:
        servicio_invalido = ReservaSala("S004", "Sala incorrecta", -5000)
        sistema.registrar_servicio(servicio_invalido)
    except ErrorSistema as error:
        logging.error("Servicio invalido: %s", error)
        print(f"Error controlado: {error}")

    # OPERACION 9: Reserva válida
    print("\nOPERACION 9: Reserva de sala.")
    reserva1 = sistema.crear_reserva("R001", "C001", "S001", 2, capacidad=20)
    reserva1.confirmar(descuento=10, impuesto=19)

    # OPERACION 10: Reserva válida
    print("\nOPERACION 10: Reserva de equipo.")
    reserva2 = sistema.crear_reserva("R002", "C002", "S002", 3, equipo="Computador portatil")
    reserva2.confirmar()

    # OPERACION 11: Reserva válida
    print("\nOPERACION 11: Reserva de asesoria.")
    reserva3 = sistema.crear_reserva("R003", "C001", "S003", 1.5, especialidad="Programacion")
    reserva3.confirmar()

    # OPERACION 12: Reserva fallida (cliente no existe)
    print("\nOPERACION 12: Reserva con cliente inexistente.")
    try:
        sistema.crear_reserva("R004", "C999", "S001", 2, capacidad=10)
    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # OPERACION 13: Servicio no disponible
    print("\nOPERACION 13: Servicio no disponible.")
    try:
        equipo.cambiar_disponibilidad(False)
        reserva4 = sistema.crear_reserva("R005", "C001", "S002", 2, equipo="Computador portatil")
        reserva4.confirmar()
    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # OPERACION 14: Cancelación
    print("\nOPERACION 14: Cancelacion de reserva.")
    reserva1.cancelar()

    # OPERACION 15: Confirmar reserva cancelada (falla controlada)
    print("\nOPERACION 15: Confirmacion de reserva cancelada.")
    try:
        reserva1.confirmar()
    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # OPERACION 16: Cálculo inválido
    print("\nOPERACION 16: Calculo con descuento incorrecto.")
    try:
        sala.calcular_costo(2, descuento=150)
    except ErrorSistema as error:
        logging.error("Calculo incorrecto: %s", error)
        print(f"Error controlado: {error}")

    # OPERACION 17: Reserva duplicada
    print("\nOPERACION 17: Intentar crear reserva duplicada.")
    try:
        sistema.crear_reserva("R002", "C001", "S001", 1, capacidad=10)
    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # OPERACIONES 18-20: Listados
    print("\nOPERACION 18: Listado de clientes.")
    sistema.listar_clientes()

    print("\nOPERACION 19: Listado de servicios.")
    sistema.listar_servicios()

    print("\nOPERACION 20: Listado de reservas.")
    sistema.listar_reservas()

    print("\n" + "=" * 60)
    print("       TODAS LAS PRUEBAS HAN FINALIZADO")
    print("       Revise el archivo software_fj.log")
    print("=" * 60)


# ==========================================================
# 12. EJECUCION PRINCIPAL
# ==========================================================

if __name__ == "__main__":
    try:
        ejecutar_pruebas()
    except Exception as error:
        logging.exception("Error critico en el sistema.")
        print(f"Error general controlado: {error}")
    finally:
        logging.info("Ejecucion del sistema finalizada.")
        print("\nSistema Software FJ finalizado.")