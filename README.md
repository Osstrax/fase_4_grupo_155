# Proyecto Software FJ - Grupo 155

Universidad Nacional Abierta y a Distancia (UNAD)  
Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)  
Curso: Programación (Código 213023) - Fase 4: Prácticas Simuladas  

## Integrantes
- Lucas Torres Cadavid
- Mateo Marmolejo Velásquez

## Descripción del Ejercicio
Desarrollo de un sistema orientado a objetos en Python para la empresa "Software FJ", enfocado en la gestión de clientes, reservas y tres tipos de servicios:
1. Reserva de salas.
2. Alquiler de equipos.
3. Asesorías especializadas.

El sistema opera en memoria (sin base de datos) y su objetivo principal es garantizar estabilidad y tolerancia a fallos mediante el uso de excepciones personalizadas y el registro de eventos y errores en un archivo de bitácora (`software_fj.log`).

## Reglas de Uso del Repositorio y Trabajo en Equipo
Para mantener el orden y cumplir con las evidencias de trabajo colaborativo en GitHub:

1. **Rama `main` (Principal):** Contiene únicamente versiones estables y verificadas del proyecto.
2. **Ramas de trabajo individuales:** Cada integrante debe trabajar en su propia rama:
   - Rama de Lucas: `lutorres`
   - Compañeros: crear su rama personal con su nombre o usuario (ejemplo: `mateo`, `nombre_usuario`).
3. **Verificación antes de integrar a `main`:**
   - Todo cambio debe probarse localmente antes de solicitar integración, asegurando que el código corra sin caídas y que las excepciones y logs funcionen correctamente.
   - La integración a `main` se realizará mediante Pull Request en GitHub para que los demás compañeros puedan revisar y aprobar los cambios.

## Ejecución
Para correr la simulación de pruebas:
```bash
python software_fj.py
```
El sistema generará el archivo `software_fj.log` en la raíz del proyecto con el registro detallado de las operaciones.

