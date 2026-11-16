from abc import ABC, abstractmethod
from datetime import datetime
import logging
import math

from excepciones import (
    ErrorSistema,
    DatoInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError
)


# Molde base para todos los objetos del sistema que requieren identificador único
class Entidad(ABC):
    def __init__(self, identificador):
        # El identificador debe ser texto no vacío
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatoInvalidoError("El identificador debe ser una cadena de texto no vacía.")
        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        pass

    def __str__(self):
        return f"[{self.__class__.__name__}] ID: {self._identificador}"


# Representa a un cliente con datos personales protegidos y validados
class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        # Validación del nombre
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre es obligatorio.")

        # Validación del correo electrónico (debe tener arroba y punto en el dominio)
        if not isinstance(correo, str) or correo.count("@") != 1 or "." not in correo.split("@")[1]:
            raise DatoInvalidoError("El correo no es valido.")

        # Validación del teléfono (solo dígitos, longitud comercial de 7 a 15)
        if not isinstance(telefono, str) or not telefono.isdigit() or not (7 <= len(telefono) <= 15):
            raise DatoInvalidoError("El telefono no es valido.")

        self.__nombre = nombre.strip()
        self.__correo = correo.strip().lower()
        self.__telefono = telefono.strip()

    # Propiedades para lectura de atributos privados
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
        return f"Cliente: {self.__nombre} | ID: {self.identificador} | Correo: {self.__correo} | Tel: {self.__telefono}"


# Clase abstracta base para los servicios del portafolio
class Servicio(Entidad, ABC):
    def __init__(self, identificador, nombre, tarifa_base):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")

        # La tarifa debe ser un valor numérico positivo
        if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
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
        logging.info("Disponibilidad del servicio %s: %s", self.nombre, estado)

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio {self.nombre} no esta disponible.")

    # Simulación de sobrecarga para cálculo de costo con parámetros opcionales
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_disponibilidad()

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duracion debe ser positiva.")

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not (0 <= descuento <= 100):
            raise DatoInvalidoError("El descuento debe estar entre 0 y 100.")

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)) or not (0 <= impuesto <= 100):
            raise DatoInvalidoError("El impuesto debe estar entre 0 y 100.")

        # Cálculo financiero: subtotal, descuento aplicado y adición de impuestos
        subtotal = self._tarifa_base * duracion
        monto_descuento = subtotal * (descuento / 100)
        base = subtotal - monto_descuento
        total = base * (1 + (impuesto / 100))

        if total < 0:
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


# Servicio especializado en salas de reunión y conferencias
class ReservaSala(Servicio):
    def validar_parametros(self, **kwargs):
        capacidad = kwargs.get("capacidad")
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala es invalida.")
        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_disponibilidad()
        return super().calcular_costo(duracion, descuento, impuesto)

    def describir_servicio(self):
        return "Reserva de salas para reuniones y eventos."

    def mostrar_informacion(self):
        return f"Servicio: {self.nombre} | Tarifa por hora: ${self.tarifa_base:,.2f} | Disponible: {self.disponible}"


# Servicio especializado en préstamo de equipos de cómputo
class AlquilerEquipo(Servicio):
    def validar_parametros(self, **kwargs):
        equipo = kwargs.get("equipo")
        if not isinstance(equipo, str) or not equipo.strip():
            raise DatoInvalidoError("Debe indicar el equipo solicitado.")
        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_disponibilidad()
        return super().calcular_costo(duracion, descuento, impuesto)

    def describir_servicio(self):
        return "Alquiler de equipos tecnologicos."

    def mostrar_informacion(self):
        return f"Servicio: {self.nombre} | Tarifa por hora: ${self.tarifa_base:,.2f} | Disponible: {self.disponible}"


# Servicio especializado en consultoría técnica profesional
class AsesoriaEspecializada(Servicio):
    def validar_parametros(self, **kwargs):
        especialidad = kwargs.get("especialidad")
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatoInvalidoError("Debe indicar la especialidad.")
        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_disponibilidad()
        return super().calcular_costo(duracion, descuento, impuesto)

    def describir_servicio(self):
        return "Asesorias profesionales especializadas."

    def mostrar_informacion(self):
        return f"Servicio: {self.nombre} | Tarifa por hora: ${self.tarifa_base:,.2f} | Disponible: {self.disponible}"


# Integra cliente, servicio, duración y gestiona el ciclo de vida de la reserva
class Reserva(Entidad):
    def __init__(self, identificador, cliente, servicio, duracion, **kwargs):
        super().__init__(identificador)

        # Verificamos que los objetos asociados pertenezcan a los tipos correctos
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente asignado no es válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio asignado no es válido.")

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duracion debe ser positiva.")

        # Valida parámetros puntuales del servicio (aforo, máquina o especialidad)
        servicio.validar_parametros(**kwargs)

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__kwargs = kwargs
        self.__fecha = datetime.now()
        self.__estado = "Pendiente"
        self.__costo = 0.0

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def fecha(self):
        return self.__fecha

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    # Confirma la reserva y calcula su valor final
    def confirmar(self, descuento=0, impuesto=0):
        try:
            if self.__estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva en estado '{self.__estado}'."
                )

            self.__servicio.validar_disponibilidad()
            self.__servicio.validar_parametros(**self.__kwargs)
            self.__costo = self.__servicio.calcular_costo(self.__duracion, descuento, impuesto)
            self.__estado = "Confirmada"

            logging.info("Reserva %s confirmada exitosamente. Costo: %s", self.identificador, self.__costo)
            print("Reserva confirmada correctamente.")

        except ErrorSistema as error:
            logging.error("Fallo al confirmar la reserva %s: %s", self.identificador, error)
            raise

    # Cancela una reserva existente si no ha sido cancelada previamente
    def cancelar(self):
        try:
            if self.__estado == "Cancelada":
                raise OperacionNoPermitidaError("La reserva ya esta cancelada.")

            self.__estado = "Cancelada"
            logging.info("Reserva %s cancelada.", self.identificador)
            print("Reserva cancelada correctamente.")

        except ErrorSistema as error:
            logging.error("Error al cancelar la reserva %s: %s", self.identificador, error)
            raise

    # Demuestra el uso de la estructura completa try / except / else / finally solicitada en la guía
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