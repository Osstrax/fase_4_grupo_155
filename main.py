import logging

from excepciones import (
    ErrorSistema,
    DatoInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError
)
from modelos import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from sistema import SoftwareFJ


def ejecutar_pruebas():
    # Instanciamos el sistema central en memoria
    sistema = SoftwareFJ()

    print("\n" + "=" * 60)
    print("       SISTEMA INTEGRAL DE GESTION SOFTWARE FJ")
    print("=" * 60)

    # 1. Registro de cliente valido
    print("\nOPERACION 1: Registro de primer cliente valido.")
    cliente1 = Cliente("C001", "Carlos Ramirez", "carlos@gmail.com", "3001234567")
    sistema.registrar_cliente(cliente1)

    # 2. Registro de segundo cliente valido
    print("\nOPERACION 2: Registro de segundo cliente valido.")
    cliente2 = Cliente("C002", "Maria Lopez", "maria@gmail.com", "3101234567")
    sistema.registrar_cliente(cliente2)

    # 3. Intento de registro con datos invalidos (captura de DatoInvalidoError)
    print("\nOPERACION 3: Intento de registro de cliente con datos invalidos.")
    try:
        cliente_invalido = Cliente("C003", "", "correo_invalido", "abc123")
        sistema.registrar_cliente(cliente_invalido)
    except ErrorSistema as error:
        logging.error("Captura de cliente invalido: %s", error)
        print(f"Error controlado: {error}")

    # 4. Intento de registro con ID duplicado
    print("\nOPERACION 4: Intento de registro de cliente con ID duplicado.")
    cliente_duplicado = Cliente("C001", "Pedro Gomez", "pedro@gmail.com", "3201234567")
    sistema.registrar_cliente(cliente_duplicado)

    # 5. Registro de sala de reuniones
    print("\nOPERACION 5: Registro de servicio - Sala de reuniones.")
    sala = ReservaSala("S001", "Sala de juntas principal", 50000)
    sistema.registrar_servicio(sala)

    # 6. Registro de alquiler de equipo
    print("\nOPERACION 6: Registro de servicio - Alquiler de equipo.")
    equipo = AlquilerEquipo("S002", "Portatil para desarrollo", 25000)
    sistema.registrar_servicio(equipo)

    # 7. Registro de asesoria especializada
    print("\nOPERACION 7: Registro de servicio - Asesoria especializada.")
    asesoria = AsesoriaEspecializada("S003", "Consultoria en arquitectura de software", 80000)
    sistema.registrar_servicio(asesoria)

    # 8. Intento de crear servicio con tarifa negativa
    print("\nOPERACION 8: Intento de crear servicio con tarifa negativa.")
    try:
        sala_invalida = ReservaSala("S004", "Sala economica", -5000)
        sistema.registrar_servicio(sala_invalida)
    except ErrorSistema as error:
        logging.error("Captura de servicio invalido: %s", error)
        print(f"Error controlado: {error}")

    # 9. Creacion y confirmacion de reserva con sobrecarga (descuento e impuesto)
    print("\nOPERACION 9: Creacion y confirmacion de reserva con parametros opcionales.")
    reserva1 = sistema.crear_reserva("R001", "C001", "S001", 2, capacidad=20)
    reserva1.confirmar(descuento=10, impuesto=19)

    # 10. Demostracion visible de try / except / else / finally solicitada por el tutor
    print("\nOPERACION 10: Procesamiento de reserva mediante try / except / else / finally.")
    reserva2 = sistema.crear_reserva("R002", "C002", "S002", 3, equipo="Portatil para desarrollo")
    reserva2.procesar()

    # 11. Reserva de asesoria especializada
    print("\nOPERACION 11: Creacion y confirmacion de reserva de asesoria.")
    reserva3 = sistema.crear_reserva("R003", "C001", "S003", 1.5, especialidad="Arquitectura de software")
    reserva3.confirmar()

    # 12. Intento de reserva con cliente inexistente
    print("\nOPERACION 12: Intento de reserva con cliente inexistente.")
    try:
        sistema.crear_reserva("R004", "C999", "S001", 2, capacidad=10)
    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # 13. Intento de reserva con servicio no disponible
    print("\nOPERACION 13: Intento de uso de servicio deshabilitado.")
    try:
        equipo.cambiar_disponibilidad(False)
        reserva_bloqueada = sistema.crear_reserva("R005", "C001", "S002", 2, equipo="Portatil para desarrollo")
        reserva_bloqueada.confirmar()
    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # 14. Cancelacion de reserva
    print("\nOPERACION 14: Cancelacion formal de reserva activa.")
    reserva1.cancelar()

    # 15. Intento de confirmar reserva ya cancelada
    print("\nOPERACION 15: Intento de confirmacion sobre reserva cancelada.")
    try:
        reserva1.confirmar()
    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # 16. Calculo con porcentaje de descuento invalido (> 100%)
    print("\nOPERACION 16: Intento de calculo con descuento fuera de rango.")
    try:
        sala.calcular_costo(2, descuento=150)
    except ErrorSistema as error:
        logging.error("Captura de calculo invalido: %s", error)
        print(f"Error controlado: {error}")

    # 17. Intento de crear reserva con identificador duplicado
    print("\nOPERACION 17: Intento de reserva con ID duplicado.")
    try:
        sistema.crear_reserva("R002", "C001", "S001", 1, capacidad=10)
    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # 18. Demostracion visible de encadenamiento de excepciones (raise ... from)
    print("\nOPERACION 18: Demostracion de encadenamiento de excepciones (raise ... from).")
    try:
        # Simulamos un fallo imprevisto pasando un parámetro que rompa internamente
        sistema.crear_reserva("R006", "C001", "S001", 2, capacidad="capacidad_no_numerica")
    except ErrorSistema as error:
        print(f"Error capturado: {error}")
        if error.__cause__:
            print(f"Causa original encadenada (__cause__): {type(error.__cause__).__name__} -> {error.__cause__}")

    # 19. Listado de entidades en memoria
    print("\nOPERACION 19: Consulta general de clientes y servicios registrados.")
    sistema.listar_clientes()
    sistema.listar_servicios()

    # 20. Listado final de reservas
    print("\nOPERACION 20: Consulta general del historial de reservas.")
    sistema.listar_reservas()

    print("\n" + "=" * 60)
    print("       TODAS LAS PRUEBAS HAN FINALIZADO EXITOSAMENTE")
    print("       Consulte el archivo software_fj.log para ver la bitacora")
    print("=" * 60)


if __name__ == "__main__":
    try:
        ejecutar_pruebas()
    except Exception as error:
        logging.exception("Fallo critico general en la aplicacion.")
        print(f"Error general: {error}")
    finally:
        logging.info("Ciclo de ejecucion del sistema Software FJ completado.")
        print("\nEjecucion finalizada de forma segura.")