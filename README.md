# Calculadora de Confiabilidad Industrial (IIoT Reliability Calc)

![Status](https://img.shields.io/badge/Status-Desarrollo_Finalizado-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?logo=pandas)

Este proyecto forma parte de mi **Portafolio IIoT** y consiste en una herramienta avanzada de Ingeniería de Confiabilidad diseñada para optimizar la toma de decisiones en entornos industriales. La aplicación automatiza el cálculo de indicadores clave (KPIs) y proporciona recomendaciones estratégicas basadas en el comportamiento histórico de los activos.

## 📌 Problemática

En muchas plantas industriales, la gestión del mantenimiento sigue siendo reactiva debido a:
- **Falta de visibilidad:** Los datos de fallas suelen estar dispersos en hojas de cálculo no estructuradas o bitácoras manuales.
- **Subjetividad:** La toma de decisiones depende de la intuición del personal en lugar de métricas de ingeniería precisas.
- **"Malos Actores":** Dificultad para identificar rápidamente qué equipos consumen más recursos o fallan con mayor frecuencia.
- **Costos Ocultos:** Tiempo de inactividad (downtime) prolongado por falta de análisis de mantenibilidad (MTTR).

## 💡 Solución

Esta calculadora resuelve estos desafíos mediante:
1. **Normalización de Datos:** Transforma registros históricos en una estructura de datos limpia y lista para análisis.
2. **KPIs de Clase Mundial:** Calcula de forma automática el **MTBF** (Confiabilidad) y el **MTTR** (Mantenibilidad).
3. **Análisis de Disponibilidad:** Identifica la disponibilidad porcentual de cada activo comparándolo contra objetivos corporativos.
4. **Inteligencia de Mantenimiento:** Un motor de reglas traduce los KPIs en recomendaciones técnicas concretas, permitiendo pasar de un mantenimiento correctivo a uno preventivo y predictivo.

## 🚀 Características Principales

- **Cálculo Automatizado de KPIs:** Obtención precisa de MTBF (Mean Time Between Failures), MTTR (Mean Time To Repair) y Disponibilidad Operacional.
- **Motor de Recomendaciones:** Sistema experto que sugiere intervenciones técnicas (RCA, capacitación, gestión de repuestos) según el perfil de falla del equipo.
- **Generador de Datos Sintéticos:** Capacidad para simular escenarios industriales complejos (mortalidad infantil, desgaste, activos críticos).
- **Dashboard Visual:** Generación de gráficos comparativos y visualización teórica de la **Curva de la Bañera (Bathtub Curve)**.

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **Pandas:** Procesamiento de series temporales y limpieza de datos.
- **Matplotlib:** Generación de dashboards y visualizaciones técnicas.
- **Numpy:** Cálculos estadísticos y simulaciones de curvas de falla.

## 📁 Estructura del Proyecto

```text
├── reliability_calculator.py  # Script principal de análisis y KPIs
├── generate_dataset.py        # Generador de datos industriales sintéticos
├── historial_fallas.csv       # Dataset con registros de fallas (generado)
├── requirements.txt           # Dependencias del proyecto
└── PROYECTO_2_PLAN.md         # Documentación de la fase de planificación
```

## ⚙️ Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/iiot-reliability-calc.git
   cd iiot-reliability-calc
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generar el dataset de prueba (Opcional):**
   ```bash
   python generate_dataset.py
   ```

4. **Ejecutar la calculadora:**
   ```bash
   python reliability_calculator.py
   ```

## 📊 Visualización de Resultados

El script genera automáticamente un archivo `analisis_confiabilidad_completo.png` que incluye:
1. Comparativa de Confiabilidad (MTBF) vs Mantenibilidad (MTTR).
2. Nivel de Disponibilidad por equipo con alertas de color.
3. Representación de la Curva de la Bañera para identificar etapas del ciclo de vida.

---
**Autor:** [Tu Nombre] - Especialista en Automatización e IIoT.
