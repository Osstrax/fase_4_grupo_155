import unittest
import sys
import os

# Importación de las clases del sistema principal
from software_fj import (
    Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada, 
    Reserva, SoftwareFJ, DatoInvalidoError, ReservaInvalidaError
)

class TestSoftwareFJ(unittest.TestCase):
    """Pruebas unitarias para validar la estabilidad del sistema Software FJ."""

    def setUp(self):
        """Configuración inicial que se ejecuta antes de cada prueba."""
        self.sistema = SoftwareFJ()
        self.cliente_valido = Cliente("C100", "Test User", "test@test.com", "3001234567")
        self.sala_valida = ReservaSala("S100", "Sala Test", 50000)
        self.sistema.registrar_cliente(self.cliente_valido)
        self.sistema.registrar_servicio(self.sala_valida)

    def test_registro_cliente_duplicado(self):
        """Prueba que el sistema no permita registrar dos clientes con el mismo ID."""
        cliente_duplicado = Cliente("C100", "Otro Nombre", "otro@test.com", "3109876543")
        self.sistema.registrar_cliente(cliente_duplicado)
        self.assertEqual(len(self.sistema._SoftwareFJ__clientes), 1)

    def test_creacion_reserva_exitosa(self):
        """Prueba que una reserva válida se cree y confirme correctamente."""
        reserva = self.sistema.crear_reserva("R100", "C100", "S100", 2, capacidad=10)
        reserva.confirmar()
        self.assertEqual(reserva.estado, "Confirmada")
        self.assertEqual(reserva.costo, 100000.0) 

    def test_error_reserva_cliente_inexistente(self):
        """Prueba que el sistema lance una excepción si el cliente no existe."""
        with self.assertRaises(ReservaInvalidaError):
            self.sistema.crear_reserva("R101", "C999", "S100", 2, capacidad=10)

    def test_validacion_correo_invalido(self):
        """Prueba que el sistema rechace correos electrónicos mal formados."""
        with self.assertRaises(DatoInvalidoError):
            Cliente("C101", "Error", "correo_sin_arroba.com", "3001234567")

    def test_calculo_costo_negativo(self):
        """Prueba que el sistema rechace tarifas negativas."""
        with self.assertRaises(DatoInvalidoError):
            ReservaSala("S101", "Sala Error", -1000)

if __name__ == '__main__':
    print("Iniciando pruebas unitarias de Software FJ...\n")
    unittest.main()