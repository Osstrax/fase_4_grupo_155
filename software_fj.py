
from abc import ABC, abstractmethod
from datetime import datetime
import logging
import math


# ==========================================================
# 1. CONFIGURACION DEL ARCHIVO DE REGISTROS
# ==========================================================

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
    pass


class DatoInvalidoError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class ReservaInvalidaError(ErrorSistema):
    pass


class OperacionNoPermitidaError(ErrorSistema):
    pass


# ==========================================================
# 3. CLASE ABSTRACTA ENTIDAD
# ==========================================================

class Entidad(ABC):

    def __init__(self, identificador):

        if not isinstance(identificador, str) or not identificador.strip():
            raise DatoInvalidoError(
                "El identificador no puede estar vacio."
            )

        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ==========================================================
# 4. CLASE CLIENTE
# ==========================================================

class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):

        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre es obligatorio.")

        if (
            not isinstance(correo, str)
            or correo.count("@") != 1
            or "." not in correo.split("@")[1]
        ):
            raise DatoInvalidoError("El correo no es valido.")

        if (
            not isinstance(telefono, str)
            or not telefono.isdigit()
            or not 7 <= len(telefono) <= 15
        ):
            raise DatoInvalidoError("El telefono no es valido.")

        self.__nombre = nombre.strip()
        self.__correo = correo.strip().lower()
        self.__telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_informacion(self):

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

    def __init__(self, identificador, nombre, tarifa_base):

        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")

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
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):

        if not isinstance(estado, bool):
            raise DatoInvalidoError("Estado de disponibilidad incorrecto.")

        self._disponible = estado

        logging.info(
            "Disponibilidad del servicio %s: %s",
            self.nombre,
            estado
        )

    def validar_disponibilidad(self):

        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.nombre} no esta disponible."
            )

    # Metodo con parametros opcionales para simular sobrecarga

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        self.validar_disponibilidad()

        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not math.isfinite(duracion)
            or duracion <= 0
        ):
            raise DatoInvalidoError("La duracion debe ser positiva.")

        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 100
        ):
            raise DatoInvalidoError("El descuento debe estar entre 0 y 100.")

        if (
            isinstance(impuesto, bool)
            or not isinstance(impuesto, (int, float))
            or not math.isfinite(impuesto)
            or not 0 <= impuesto <= 100
        ):
            raise DatoInvalidoError("El impuesto debe estar entre 0 y 100.")

        subtotal = self._tarifa_base * duracion

        valor_descuento = subtotal * descuento / 100

        subtotal_final = subtotal - valor_descuento

        total = subtotal_final * (1 + impuesto / 100)

        if not math.isfinite(total) or total < 0:
            raise ErrorSistema("El calculo del costo es inconsistente.")

        return round(total, 2)

    @abstractmethod
    def validar_parametros(self, **kwargs):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ==========================================================
# 6. SERVICIO DE RESERVA DE SALAS
# ==========================================================

class ReservaSala(Servicio):

    def validar_parametros(self, **kwargs):

        capacidad = kwargs.get("capacidad")

        if (
            isinstance(capacidad, bool)
            or not isinstance(capacidad, int)
            or capacidad <= 0
        ):
            raise DatoInvalidoError("La capacidad de la sala es invalida.")

        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        self.validar_disponibilidad()

        return super().calcular_costo(
            duracion, descuento, impuesto
        )

    def describir_servicio(self):

        return "Reserva de salas para reuniones y eventos."

    def mostrar_informacion(self):

        return (
            f"Servicio: {self.nombre} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f} | "
            f"Disponible: {self.disponible}"
        )


# ==========================================================
# 7. SERVICIO DE ALQUILER DE EQUIPOS
# ==========================================================

class AlquilerEquipo(Servicio):

    def validar_parametros(self, **kwargs):

        equipo = kwargs.get("equipo")

        if not isinstance(equipo, str) or not equipo.strip():
            raise DatoInvalidoError("Debe indicar el equipo solicitado.")

        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        self.validar_disponibilidad()

        return super().calcular_costo(
            duracion, descuento, impuesto
        )

    def describir_servicio(self):

        return "Alquiler de equipos tecnologicos."

    def mostrar_informacion(self):

        return (
            f"Servicio: {self.nombre} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f} | "
            f"Disponible: {self.disponible}"
        )


# ==========================================================
# 8. SERVICIO DE ASESORIAS ESPECIALIZADAS
# ==========================================================

class AsesoriaEspecializada(Servicio):

    def validar_parametros(self, **kwargs):

        especialidad = kwargs.get("especialidad")

        if (
            not isinstance(especialidad, str)
            or not especialidad.strip()
        ):
            raise DatoInvalidoError("Debe indicar la especialidad.")

        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        self.validar_disponibilidad()

        return super().calcular_costo(
            duracion, descuento, impuesto
        )

    def describir_servicio(self):

        return "Asesorias profesionales especializadas."

    def mostrar_informacion(self):

        return (
            f"Servicio: {self.nombre} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f} | "
            f"Disponible: {self.disponible}"
        )


# ==========================================================
# 9. CLASE RESERVA
# ==========================================================

class Reserva(Entidad):

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        duracion,
        **kwargs
    ):

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

        servicio.validar_parametros(**kwargs)

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = float(duracion)
        self.__estado = "Pendiente"
        self.__costo = 0.0
        self.__fecha = datetime.now()

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    def confirmar(self, descuento=0, impuesto=0):

        try:

            if self.__estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    "La reserva no se encuentra pendiente."
                )

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

            logging.exception("Error inesperado al confirmar.")

            raise ErrorSistema(
                "No fue posible confirmar la reserva."
            ) from error

    def cancelar(self):

        try:

            if self.__estado not in ("Pendiente", "Confirmada"):
                raise OperacionNoPermitidaError(
                    "No se puede cancelar esta reserva."
                )

            self.__estado = "Cancelada"

            logging.info(
                "Reserva %s cancelada.",
                self.identificador
            )

            print("Reserva cancelada correctamente.")

        except ErrorSistema as error:

            logging.error("Error al cancelar: %s", error)

            raise

    def procesar(self):

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

    def __init__(self):

        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    def registrar_cliente(self, cliente):

        try:

            if not isinstance(cliente, Cliente):
                raise DatoInvalidoError("Objeto cliente incorrecto.")

            if any(
                c.identificador == cliente.identificador
                for c in self.__clientes
            ):
                raise DatoInvalidoError("El cliente ya esta registrado.")

            self.__clientes.append(cliente)

            logging.info(
                "Cliente registrado: %s",
                cliente.nombre
            )

            print("Cliente registrado correctamente.")

        except ErrorSistema as error:

            logging.error("Error registrando cliente: %s", error)

            print(f"Error controlado: {error}")

    def registrar_servicio(self, servicio):

        try:

            if not isinstance(servicio, Servicio):
                raise DatoInvalidoError("Servicio incorrecto.")

            if any(
                s.identificador == servicio.identificador
                for s in self.__servicios
            ):
                raise DatoInvalidoError("El servicio ya existe.")

            self.__servicios.append(servicio)

            logging.info(
                "Servicio registrado: %s",
                servicio.nombre
            )

            print("Servicio registrado correctamente.")

        except ErrorSistema as error:

            logging.error("Error registrando servicio: %s", error)

            print(f"Error controlado: {error}")

    def crear_reserva(
        self,
        identificador,
        id_cliente,
        id_servicio,
        duracion,
        **kwargs
    ):

        try:

            cliente = next(
                (
                    c for c in self.__clientes
                    if c.identificador == str(id_cliente)
                ),
                None
            )

            servicio = next(
                (
                    s for s in self.__servicios
                    if s.identificador == str(id_servicio)
                ),
                None
            )

            if cliente is None:
                raise ReservaInvalidaError(
                    "El cliente solicitado no existe."
                )

            if servicio is None:
                raise ReservaInvalidaError(
                    "El servicio solicitado no existe."
                )

            if any(
                r.identificador == str(identificador)
                for r in self.__reservas
            ):
                raise ReservaInvalidaError(
                    "El identificador de reserva ya existe."
                )

            reserva = Reserva(
                identificador,
                cliente,
                servicio,
                duracion,
                **kwargs
            )

            self.__reservas.append(reserva)

            logging.info(
                "Reserva creada: %s",
                identificador
            )

            print("Reserva creada correctamente.")

            return reserva

        except ErrorSistema as error:

            logging.error("Error creando reserva: %s", error)

            raise

        except Exception as error:

            logging.exception("Error inesperado creando reserva.")

            raise ErrorSistema(
                "No se pudo crear la reserva."
            ) from error

    def listar_clientes(self):

        print("\n========== LISTA DE CLIENTES ==========")

        for cliente in self.__clientes:
            print(cliente.mostrar_informacion())

    def listar_servicios(self):

        print("\n========== LISTA DE SERVICIOS ==========")

        for servicio in self.__servicios:

            print(servicio.mostrar_informacion())
            print(servicio.describir_servicio())
            print("--------------------------------------")

    def listar_reservas(self):

        print("\n========== LISTA DE RESERVAS ==========")

        for reserva in self.__reservas:
            print(reserva.mostrar_informacion())


# ==========================================================
# 11. PRUEBAS AUTOMATICAS DEL SISTEMA
# ==========================================================

def ejecutar_pruebas():

    sistema = SoftwareFJ()

    print("\n" + "=" * 60)
    print("       SISTEMA INTEGRAL DE GESTION SOFTWARE FJ")
    print("=" * 60)

    # OPERACION 1

    print("\nOPERACION 1: Registro de cliente.")

    cliente1 = Cliente(
        "C001",
        "Carlos Ramirez",
        "carlos@gmail.com",
        "3001234567"
    )

    sistema.registrar_cliente(cliente1)

    # OPERACION 2

    print("\nOPERACION 2: Registro de segundo cliente.")

    cliente2 = Cliente(
        "C002",
        "Maria Lopez",
        "maria@gmail.com",
        "3101234567"
    )

    sistema.registrar_cliente(cliente2)

    # OPERACION 3

    print("\nOPERACION 3: Registro de cliente invalido.")

    try:

        cliente3 = Cliente(
            "C003",
            "",
            "correo incorrecto",
            "abc123"
        )

        sistema.registrar_cliente(cliente3)

    except ErrorSistema as error:

        logging.error("Cliente invalido: %s", error)

        print(f"Error controlado: {error}")

    # OPERACION 4

    print("\nOPERACION 4: Registro de cliente duplicado.")

    cliente_duplicado = Cliente(
        "C001",
        "Pedro Gomez",
        "pedro@gmail.com",
        "3201234567"
    )

    sistema.registrar_cliente(cliente_duplicado)

    # OPERACION 5

    print("\nOPERACION 5: Registro de sala.")

    sala = ReservaSala(
        "S001",
        "Sala de reuniones",
        50000
    )

    sistema.registrar_servicio(sala)

    # OPERACION 6

    print("\nOPERACION 6: Registro de equipo.")

    equipo = AlquilerEquipo(
        "S002",
        "Computador portatil",
        25000
    )

    sistema.registrar_servicio(equipo)

    # OPERACION 7

    print("\nOPERACION 7: Registro de asesoria.")

    asesoria = AsesoriaEspecializada(
        "S003",
        "Asesoria informatica",
        80000
    )

    sistema.registrar_servicio(asesoria)

    # OPERACION 8

    print("\nOPERACION 8: Creacion de servicio invalido.")

    try:

        servicio_invalido = ReservaSala(
            "S004",
            "Sala incorrecta",
            -5000
        )

        sistema.registrar_servicio(servicio_invalido)

    except ErrorSistema as error:

        logging.error("Servicio invalido: %s", error)

        print(f"Error controlado: {error}")

    # OPERACION 9

    print("\nOPERACION 9: Reserva de sala.")

    reserva1 = sistema.crear_reserva(
        "R001",
        "C001",
        "S001",
        2,
        capacidad=20
    )

    reserva1.confirmar(descuento=10, impuesto=19)

    # OPERACION 10

    print("\nOPERACION 10: Reserva de equipo.")

    reserva2 = sistema.crear_reserva(
        "R002",
        "C002",
        "S002",
        3,
        equipo="Computador portatil"
    )

    reserva2.confirmar()

    # OPERACION 11

    print("\nOPERACION 11: Reserva de asesoria.")

    reserva3 = sistema.crear_reserva(
        "R003",
        "C001",
        "S003",
        1.5,
        especialidad="Programacion"
    )

    reserva3.confirmar()

    # OPERACION 12

    print("\nOPERACION 12: Reserva con cliente inexistente.")

    try:

        sistema.crear_reserva(
            "R004",
            "C999",
            "S001",
            2,
            capacidad=10
        )

    except ErrorSistema as error:

        print(f"Error controlado: {error}")

    # OPERACION 13

    print("\nOPERACION 13: Servicio no disponible.")

    try:

        equipo.cambiar_disponibilidad(False)

        reserva4 = sistema.crear_reserva(
            "R005",
            "C001",
            "S002",
            2,
            equipo="Computador portatil"
        )

        reserva4.confirmar()

    except ErrorSistema as error:

        print(f"Error controlado: {error}")

    # OPERACION 14

    print("\nOPERACION 14: Cancelacion de reserva.")

    reserva1.cancelar()

    # OPERACION 15

    print("\nOPERACION 15: Confirmacion de reserva cancelada.")

    try:

        reserva1.confirmar()

    except ErrorSistema as error:

        print(f"Error controlado: {error}")

    # OPERACION 16

    print("\nOPERACION 16: Calculo con descuento incorrecto.")

    try:

        sala.calcular_costo(
            2,
            descuento=150
        )

    except ErrorSistema as error:

        logging.error("Calculo incorrecto: %s", error)

        print(f"Error controlado: {error}")

    # OPERACION 17

    print("\nOPERACION 17: Intentar crear reserva duplicada.")

    try:

        sistema.crear_reserva(
            "R002",
            "C001",
            "S001",
            1,
            capacidad=10
        )

    except ErrorSistema as error:

        print(f"Error controlado: {error}")

    # OPERACION 18

    print("\nOPERACION 18: Listado de clientes.")

    sistema.listar_clientes()

    # OPERACION 19

    print("\nOPERACION 19: Listado de servicios.")

    sistema.listar_servicios()

    # OPERACION 20

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
