# Calculadora de Confiabilidad Industrial (IIoT Reliability Calc) - v2.0

![Status](https://img.shields.io/badge/Status-v2.0_Profesional-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?logo=pandas)
![Tests](https://img.shields.io/badge/Tests-22_Passing-brightgreen)

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
2. **KPIs de Clase Mundial:** Calcula de forma automática el **MTBF** (Confiabilidad), **MTTR** (Mantenibilidad) y **MTTF** (Tiempo Hasta Primera Falla).
3. **Análisis de Disponibilidad:** Identifica la disponibilidad porcentual de cada activo comparándolo contra objetivos corporativos.
4. **Inteligencia de Mantenimiento:** Un motor de reglas traduce los KPIs en recomendaciones técnicas concretas, permitiendo pasar de un mantenimiento correctivo a uno preventivo y predictivo.

## 🚀 Novedades de la Versión 2.0 (Mejoras 5 Estrellas)

- **Clase `ReliabilityEngine`:** Arquitectura orientada a objetos lista para integración con agentes IA (MantOS).
- **MTTF Implementado:** Cálculo de Tiempo Medio Hasta Primera Falla para activos no reparables.
- **Detección de Tendencias:** Condición D real — identifica automáticamente incrementos sostenidos en la tasa de fallas (indicador de desgaste).
- **Umbrales Configurables:** Clase `UmbralesConfiabilidad` con `dataclass` para adaptar criterios sin modificar código.
- **Logging Profesional:** Sistema de registro con timestamps reemplazando todos los `print()`.
- **Type Hints:** Anotaciones de tipo en todas las funciones y métodos.
- **Suite de Pruebas:** 22 tests unitarios con `pytest` validando fórmulas, recomendaciones y visualización.
- **Output Organizado:** Gráficos en carpeta `reports/` en lugar de la raíz del proyecto.

## 🛠️ Características Principales

- **Cálculo Automatizado de KPIs:** Obtención precisa de MTBF, MTTR, MTTF y Disponibilidad Operacional.
- **Motor de Recomendaciones:** Sistema experto con 5 condiciones (Crítico, Alerta, Mejora, Degradación, Óptimo).
- **Generador de Datos Sintéticos:** Capacidad para simular escenarios industriales complejos (mortalidad infantil, desgaste, activos críticos).
- **Dashboard Visual:** 4 paneles incluyendo MTBF vs MTTR, Disponibilidad, MTTF y la **Curva de la Bañera**.

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **Pandas:** Procesamiento de series temporales y limpieza de datos.
- **Matplotlib:** Generación de dashboards y visualizaciones técnicas.
- **Numpy:** Cálculos estadísticos y simulaciones de curvas de falla.
- **Pytest:** Automatización de pruebas unitarias.

## 📁 Estructura del Proyecto

```text
cal_mant/
├── reliability_calculator.py  # Motor principal (Clase ReliabilityEngine)
├── generate_dataset.py        # Generador de datos industriales sintéticos
├── tests/                     # Suite de pruebas unitarias
│   └── test_reliability.py    # 22 tests automatizados
├── reports/                   # Dashboard generado (creado automáticamente)
├── requirements.txt           # Dependencias del proyecto
├── PROYECTO_2_PLAN.md         # Documentación del plan de desarrollo
└── README.md
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

## 🧪 Pruebas Unitarias

Para verificar la integridad de las fórmulas y el motor de recomendaciones:
```bash
pytest tests/ -v
```

## 📊 Visualización de Resultados

El script genera automáticamente un dashboard en `reports/analisis_confiabilidad_completo.png` que incluye:
1. Comparativa de Confiabilidad (MTBF) vs Mantenibilidad (MTTR).
2. Nivel de Disponibilidad por equipo con alertas de color.
3. MTTF: Tiempo Hasta Primera Falla por equipo.
4. Representación de la Curva de la Bañera para identificar etapas del ciclo de vida.

---
**Autor:** Gabriel Castro - Especialista en Automatización e IIoT.
