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
*   **Disponibilidad (Availability):** $\frac{\text{MTBF}}{\text{MTBF} + \text{MTTR}} \times 100$
*   **Tasa de Fallas ($\lambda$):** $\frac{1}{\text{MTBF}}$

## 3. Estructura del Script (Python)
El script estará estructurado modularmente para asegurar su escalabilidad:

*   **Manejo de Datos (Pandas):**
    *   **Ingesta:** Carga de un dataset (CSV) con columnas clave: `ID_Equipo`, `Fecha_Falla`, `Fecha_Reparacion`, `Horas_Operacion`.
    *   **Procesamiento temporal:** Conversión de tipos de datos a `datetime` para realizar operaciones temporales precisas.
    *   **Cálculo de deltas:** Obtención automática de Tiempos de Reparación (TTR) y Tiempos Entre Fallas (TBF) calculando las diferencias entre fechas.
    *   **Agregación:** Generación de un DataFrame resumen con el total de horas, fallas y métricas calculadas por equipo.

*   **Visualización (Matplotlib / Seaborn):**
    *   **Curva de Confiabilidad / Curva de la Bañera (Bathtub Curve):** Representación visual de la tasa de fallas a lo largo del tiempo de operación para identificar la etapa de vida del activo (Mortalidad Infantil, Vida Útil, Desgaste).
    *   **Panel de Control Básico:** Gráficos de barras comparando MTBF vs MTTR por equipo para identificar a los "peores actores" (bad actors).

## 4. Lógica de Recomendación Automática
El sistema evaluará los KPIs calculados y sugerirá acciones basadas en criterios técnicos:

*   **Condición A (Bajo MTBF, Alto MTTR):** "Alerta Crítica: Alta frecuencia de fallas y reparaciones prolongadas. Recomendación: Realizar Análisis de Causa Raíz (RCA), evaluar rediseño o reemplazo."
*   **Condición B (Bajo MTBF, Bajo MTTR):** "Alerta: Fallas frecuentes pero de rápida solución. Recomendación: Revisar calidad de repuestos, mejorar rutinas de inspección."
*   **Condición C (Alto MTBF, Alto MTTR):** "Alerta: Equipo confiable pero de reparación lenta. Recomendación: Optimizar inventario MRO (repuestos), revisar accesibilidad al equipo y plan de capacitación."
*   **Condición D (Incremento sostenido en Tasa de Fallas):** "Alerta: Posible entrada en zona de desgaste. Recomendación: Programar overhaul (revisión mayor) o reemplazo planificado."

---
**Estado:** Esperando revisión y aprobación para iniciar el desarrollo del código.
