# ==========================================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==========================================================

# Clase base para todos los errores controlados de la empresa Software FJ.
class ErrorSistema(Exception): 
    pass

# Se activa cuando un dato ingresado (nombre, tarifa, identificador) no cumple las reglas.
class DatoInvalidoError(ErrorSistema): 
    pass

# Se activa cuando se intenta reservar una sala, equipo o asesoría que está inactivo.
class ServicioNoDisponibleError(ErrorSistema):
    pass

# Se activa cuando hay fallos de vinculación entre el cliente y el servicio en la reserva.
class ReservaInvalidaError(ErrorSistema):
    pass

# Se activa cuando se intenta una acción ilógica (ej. confirmar una reserva ya cancelada).
class OperacionNoPermitidaError(ErrorSistema):
    pass
