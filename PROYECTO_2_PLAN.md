# Proyecto 2: Calculadora de Mantenimiento Industrial - Plan de Desarrollo

## 1. Interpretación del Problema
En el entorno industrial moderno, la toma de decisiones basada en datos es fundamental para garantizar la disponibilidad y confiabilidad de los activos. El cálculo automatizado de indicadores clave de rendimiento (KPIs) como el **MTBF** (Mean Time Between Failures - Tiempo Medio Entre Fallas) y **MTTF** (Mean Time To Failure - Tiempo Medio Hasta la Falla) permite a los ingenieros de planta transicionar de un mantenimiento reactivo a uno predictivo/proactivo. 

Al analizar el historial de fechas de fallas y tiempos de reparación, podemos identificar cuellos de botella, optimizar los intervalos de mantenimiento preventivo, reducir el tiempo de inactividad no planificado (downtime) y maximizar el ciclo de vida útil del equipo.

## 2. Lógica Matemática
Para este proyecto, utilizaremos las siguientes fórmulas fundamentales de ingeniería de confiabilidad:

*   **Tiempo de Operación (Uptime):** Tiempo Total Disponible - Tiempo de Inactividad (Downtime).
*   **MTBF (Equipos Reparables):** $\frac{\text{Tiempo Total de Operación}}{\text{Número de Fallas}}$
    *   *Mide la confiabilidad del equipo. Un MTBF mayor indica un equipo más confiable.*
*   **MTTR (Mean Time To Repair - Tiempo Medio de Reparación):** $\frac{\text{Tiempo Total de Inactividad}}{\text{Número de Fallas}}$
    *   *Mide la mantenibilidad. Un MTTR menor indica una resolución de problemas y reparación más rápida.*
*   **MTTF (Equipos No Reparables o hasta la primera falla):** $\frac{\text{Tiempo Total de Operación}}{\text{Número de Activos}}$
    *   ⚠️ **Nota:** Esta métrica está definida en el plan pero **aún no implementada** en el código actual.
*   **Disponibilidad (Availability):** $\frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}} \times 100$
*   **Tasa de Fallas ($\lambda$):** $\frac{1}{\text{MTBF}}$

## 3. Estructura del Script (Python)
El script está estructurado modularmente en `reliability_calculator.py`:

*   **Manejo de Datos (Pandas):**
    *   `cargar_datos(filepath)`: Carga CSV con columnas `ID_Equipo`, `Fecha_Falla`, `Fecha_Reparacion`, `Horas_Operacion`. Convierte fechas a `datetime` y calcula TTR en horas.
    *   `calcular_kpis(df)`: Agrupa por `ID_Equipo`, calcula MTBF, MTTR, Disponibilidad y Tasa de Fallas.

*   **Visualización (Matplotlib + NumPy):**
    *   `visualizar_resultados(resumen)`: Genera un panel de 3 gráficos:
        1.  **MTBF vs MTTR** por equipo (barras agrupadas).
        2.  **Disponibilidad Operacional** con código de colores (verde >90%, amarillo >80%, rojo ≤80%) y línea target al 90%.
        3.  **Curva de la Bañera (simulación)** con anotaciones de las 3 zonas de vida del activo.
    *   `simular_curva_banera()`: Genera datos teóricos usando exponenciales decreciente (mortalidad infantil), constante (vida útil) y creciente (desgaste).

*   **Generador de Dataset (`generate_dataset.py`):**
    *   Simula 15 activos con 5 perfiles de comportamiento: `CRITICAL`, `RELIABLE`, `NORMAL`, `WEAR_OUT`, `INFANT_MORTALITY`.
    *   Cada perfil tiene MTBF y MTTR diferenciados con distribuciones `np.random.normal()`.
    *   Los tipos `WEAR_OUT` e `INFANT_MORTALITY` varían su MTBF con el progreso temporal (degradación realista).

## 4. Lógica de Recomendación Automática
La función `generar_recomendaciones(row)` evalúa los KPIs con umbrales definidos (`MTBF_UMBRAL_BAJO = 150`, `MTTR_UMBRAL_ALTO = 10`):

*   **Condición A (MTBF < 150 Y MTTR > 10):** "CRÍTICO: Alta frecuencia de falla y difícil reparación. Realizar RCA y evaluar reemplazo."
*   **Condición B (MTBF < 150, MTTR ≤ 10):** "ALERTA: Fallas frecuentes. Revisar calidad de componentes y mantenimiento preventivo."
    *   ⚠️ **Nota:** El texto del plan original describía una "Condición B" más específica (Bajo MTBF + Bajo MTTR → revisión de repuestos). El código actual mapea esto correctamente pero con texto simplificado.
*   **Condición C (MTBF ≥ 150, MTTR > 10):** "MEJORA: Reparaciones lentas. Optimizar stock de repuestos y capacitación técnica."
*   **Condición D (Else):** "ÓPTIMO: Equipo operando dentro de parámetros normales."
    *   ⚠️ **Pendiente:** La Condición D original del plan (detección de incremento sostenido en Tasa de Fallas) **no está implementada**. Esto requiere análisis de tendencia temporal que actualmente no existe en el código.

---

## 🌟 FASE DE MEJORA: RUMBO A LAS 5 ESTRELLAS

### 🛠️ Mejoras Técnicas Identificadas
1.  ✅ **Implementación de MTTF:** Calculado como tiempo de operación hasta la primera falla por equipo.
2.  ✅ **Detección de Tendencias (Condición D real):** `_detectar_tendencia()` compara la tasa de fallas de los últimos N meses vs el periodo anterior con factor configurable.
3.  ✅ **Modularización para MantOS:** Clase `ReliabilityEngine` con métodos separados para carga, cálculo y recomendación.
4.  ✅ **Configuración Externa:** Clase `UmbralesConfiabilidad` (dataclass) con todos los umbrales parametrizables.
5.  ✅ **Output Organizado:** Gráficos en carpeta `reports/` creada automáticamente.
6.  ✅ **Type Hints:** Anotaciones de tipo en todos los métodos de `ReliabilityEngine`.
7.  ✅ **Tests Unitarios:** 21 tests en `tests/test_reliability.py` — 100% passing. Cubre: fórmulas, recomendaciones, tendencias y visualización.
8.  ✅ **Logging Profesional:** Todos los `print()` reemplazados por `logging` con timestamps.

### 💡 Mejoras Adicionales Implementadas
*   **Dashboard de 4 paneles** (MTBF vs MTTR, Disponibilidad, MTTF, Curva de la Bañera).
*   **5 condiciones de recomendación** (Crítico, Alerta, Mejora, Degradación, Óptimo).
*   **Validación de columnas** al cargar datos con errores descriptivos.
*   **Properties** para acceso seguro a datos y KPIs.

### 💼 Enfoque de Servicio (Futuro)
*   **Dashboard de Entrega:** Integrar en Streamlit reutilizando la lógica de `dash_data`.
*   **Reporte Automatizado:** Generar PDF con recomendaciones usando la lógica de `Auto_report`.

**Estado:** ⭐⭐⭐⭐⭐ Mejoras completadas — 21/21 tests passing.
