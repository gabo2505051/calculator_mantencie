"""
Calculadora de Confiabilidad Industrial (IIoT Reliability Engine)
==================================================================
Proyecto 2 - Portafolio IIoT

Calcula MTBF, MTTR, MTTF, Disponibilidad y Tasa de Fallas por equipo
a partir de un historial de fallas. Incluye motor de recomendaciones
con detección de tendencias y simulación de la Curva de la Bañera.

Mejoras v2.0:
- Clase ReliabilityEngine para invocación externa (MantOS-ready)
- Implementación de MTTF para activos no reparables
- Detección de tendencia de degradación (Condición D real)
- Umbrales configurables externamente
- Logging profesional (reemplaza print)
- Type hints en todas las funciones
- Output organizado en carpeta reports/
"""

import os
import logging
from dataclasses import dataclass, field

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI para compatibilidad
import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


# ============================================================================
# CONFIGURACIÓN DE UMBRALES (EXTERNALIZADOS)
# ============================================================================
@dataclass
class UmbralesConfiabilidad:
    """Umbrales configurables para el motor de recomendaciones.

    Permite adaptar los criterios de decisión al contexto industrial
    sin modificar el código fuente.
    """
    mtbf_umbral_bajo: float = 150.0    # Horas — debajo de esto: fallas frecuentes
    mttr_umbral_alto: float = 10.0     # Horas — encima de esto: reparaciones lentas
    disponibilidad_target: float = 90.0  # % — objetivo corporativo
    tendencia_meses: int = 3           # Meses para análisis de tendencia
    tendencia_factor: float = 1.5      # Factor de incremento para alertar degradación


# ============================================================================
# MOTOR DE CONFIABILIDAD (CLASE PRINCIPAL)
# ============================================================================
class ReliabilityEngine:
    """Motor de análisis de confiabilidad industrial.

    Encapsula la lógica de carga, cálculo de KPIs y recomendaciones
    en una clase reutilizable para integración con MantOS.

    Ejemplo de uso:
        >>> engine = ReliabilityEngine('historial_fallas.csv')
        >>> kpis = engine.calcular_kpis()
        >>> recomendaciones = engine.generar_recomendaciones()
    """

    def __init__(self, filepath: str | None = None,
                 umbrales: UmbralesConfiabilidad | None = None) -> None:
        """Inicializa el motor con la ruta al dataset y umbrales opcionales.

        Args:
            filepath: Ruta al CSV con historial de fallas.
            umbrales: Umbrales personalizados para el motor de recomendaciones.
        """
        self.umbrales = umbrales or UmbralesConfiabilidad()
        self._df: pd.DataFrame | None = None
        self._kpis: pd.DataFrame | None = None

        if filepath:
            self.cargar_datos(filepath)

    # ----------------------------------------------------------------
    # FASE 1: INGESTA DE DATOS
    # ----------------------------------------------------------------
    def cargar_datos(self, filepath: str) -> pd.DataFrame:
        """Carga y preprocesa el historial de fallas.

        Args:
            filepath: Ruta al archivo CSV.

        Returns:
            DataFrame con columnas originales + TTR calculado.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si faltan columnas requeridas.
        """
        logger.info(f"Cargando datos desde: {os.path.basename(filepath)}")

        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"El archivo '{filepath}' no fue encontrado."
            )

        self._df = pd.read_csv(filepath)

        # Validar columnas requeridas
        requeridas = ['ID_Equipo', 'Fecha_Falla', 'Fecha_Reparacion',
                       'Horas_Operacion']
        faltantes = [c for c in requeridas if c not in self._df.columns]
        if faltantes:
            raise ValueError(
                f"Columnas faltantes: {faltantes}. "
                f"Encontradas: {list(self._df.columns)}"
            )

        self._df['Fecha_Falla'] = pd.to_datetime(self._df['Fecha_Falla'])
        self._df['Fecha_Reparacion'] = pd.to_datetime(
            self._df['Fecha_Reparacion']
        )

        # Calcular Tiempo de Reparación (TTR) en horas
        self._df['TTR'] = (
            (self._df['Fecha_Reparacion'] - self._df['Fecha_Falla'])
            .dt.total_seconds() / 3600
        )

        logger.info(
            f"Datos cargados: {self._df.shape[0]} registros, "
            f"{self._df['ID_Equipo'].nunique()} equipos"
        )
        return self._df

    # ----------------------------------------------------------------
    # FASE 2: CÁLCULO DE KPIs
    # ----------------------------------------------------------------
    def calcular_kpis(self) -> pd.DataFrame:
        """Calcula MTBF, MTTR, MTTF, Disponibilidad y Tasa de Fallas.

        Returns:
            DataFrame con KPIs por equipo.

        Raises:
            RuntimeError: Si no se han cargado datos previamente.
        """
        if self._df is None:
            raise RuntimeError("No hay datos cargados. Use cargar_datos().")

        logger.info("Calculando KPIs de confiabilidad...")

        resumen = self._df.groupby('ID_Equipo').agg({
            'Fecha_Falla': 'count',
            'TTR': 'sum',
            'Horas_Operacion': 'sum'
        }).rename(columns={'Fecha_Falla': 'Num_Fallas'})

        # Fórmulas de Confiabilidad
        resumen['MTTR'] = resumen['TTR'] / resumen['Num_Fallas']
        resumen['MTBF'] = (
            resumen['Horas_Operacion'] / resumen['Num_Fallas']
        )
        resumen['Disponibilidad'] = (
            (resumen['MTBF'] / (resumen['MTBF'] + resumen['MTTR'])) * 100
        )
        resumen['Tasa_Fallas'] = 1 / resumen['MTBF']

        # MTTF: Tiempo Medio Hasta la Falla (primera falla por equipo)
        primera_falla = self._df.sort_values('Fecha_Falla').groupby(
            'ID_Equipo'
        ).first()
        resumen['MTTF'] = primera_falla['Horas_Operacion']

        self._kpis = resumen
        logger.info(f"KPIs calculados para {len(resumen)} equipos")
        return resumen

    # ----------------------------------------------------------------
    # FASE 3: MOTOR DE RECOMENDACIONES
    # ----------------------------------------------------------------
    def _detectar_tendencia(self, equipo_id: str) -> bool:
        """Detecta si la tasa de fallas ha aumentado significativamente
        en los últimos N meses respecto al periodo anterior.

        Implementa la Condición D real del plan: detección de
        incremento sostenido en la tasa de fallas (indicador de desgaste).

        Args:
            equipo_id: Identificador del equipo a analizar.

        Returns:
            True si se detecta tendencia creciente de degradación.
        """
        if self._df is None:
            return False

        df_equipo = self._df[self._df['ID_Equipo'] == equipo_id].copy()
        if len(df_equipo) < 4:  # Necesitamos al menos 4 registros
            return False

        df_equipo['Mes'] = df_equipo['Fecha_Falla'].dt.to_period('M')
        fallas_por_mes = df_equipo.groupby('Mes').size()

        if len(fallas_por_mes) < 2 * self.umbrales.tendencia_meses:
            return False

        n = self.umbrales.tendencia_meses
        tasa_reciente = fallas_por_mes.iloc[-n:].mean()
        tasa_anterior = fallas_por_mes.iloc[-2*n:-n].mean()

        if tasa_anterior == 0:
            return False

        return tasa_reciente > tasa_anterior * self.umbrales.tendencia_factor

    def generar_recomendaciones(self) -> pd.DataFrame:
        """Aplica lógica experta para generar recomendaciones por equipo.

        Evalúa 5 condiciones basadas en MTBF, MTTR y tendencia temporal:
        - A: Crítico (bajo MTBF + alto MTTR)
        - B: Alerta (bajo MTBF, MTTR aceptable)
        - C: Mejora (MTBF ok, MTTR alto)
        - D: Degradación (tendencia creciente de fallas)
        - E: Óptimo (todos los indicadores normales)

        Returns:
            DataFrame con KPIs y columna de Recomendación.

        Raises:
            RuntimeError: Si no se han calculado KPIs.
        """
        if self._kpis is None:
            self.calcular_kpis()

        logger.info("Generando recomendaciones...")

        recomendaciones = []
        for equipo_id, row in self._kpis.iterrows():
            rec = self._evaluar_equipo(equipo_id, row)
            recomendaciones.append(rec)

        self._kpis['Recomendacion'] = recomendaciones
        return self._kpis

    def _evaluar_equipo(self, equipo_id: str,
                        row: pd.Series) -> str:
        """Evalúa un equipo individual contra los umbrales configurados.

        Args:
            equipo_id: Identificador del equipo.
            row: Serie con los KPIs del equipo.

        Returns:
            Texto de recomendación técnica.
        """
        u = self.umbrales

        # Condición A: CRÍTICO
        if row['MTBF'] < u.mtbf_umbral_bajo and row['MTTR'] > u.mttr_umbral_alto:
            return (
                "CRITICO: Alta frecuencia de falla y dificil reparacion. "
                "Realizar RCA y evaluar reemplazo."
            )

        # Condición B: ALERTA
        if row['MTBF'] < u.mtbf_umbral_bajo:
            return (
                "ALERTA: Fallas frecuentes. Revisar calidad de componentes "
                "y mantenimiento preventivo."
            )

        # Condición C: MEJORA
        if row['MTTR'] > u.mttr_umbral_alto:
            return (
                "MEJORA: Reparaciones lentas. Optimizar stock de repuestos "
                "y capacitacion tecnica."
            )

        # Condición D: DEGRADACIÓN (Tendencia creciente - NUEVA)
        if self._detectar_tendencia(equipo_id):
            return (
                "DEGRADACION: Incremento sostenido en tasa de fallas detectado. "
                "Programar inspeccion predictiva y evaluar desgaste."
            )

        # Condición E: ÓPTIMO
        return "OPTIMO: Equipo operando dentro de parametros normales."

    # ----------------------------------------------------------------
    # FASE 4: VISUALIZACIÓN
    # ----------------------------------------------------------------
    def visualizar_resultados(self, output_dir: str = 'reports') -> str:
        """Genera dashboard visual con KPIs y Curva de la Bañera.

        Los gráficos se guardan en una carpeta dedicada para mantener
        la raíz del proyecto limpia.

        Args:
            output_dir: Directorio para guardar los gráficos.

        Returns:
            Ruta al archivo PNG generado.

        Raises:
            RuntimeError: Si no se han calculado KPIs.
        """
        if self._kpis is None:
            raise RuntimeError("No hay KPIs calculados. Use calcular_kpis().")

        # Crear directorio de salida
        os.makedirs(output_dir, exist_ok=True)
        ruta_salida = os.path.join(output_dir,
                                   'analisis_confiabilidad_completo.png')

        logger.info("Generando dashboard de confiabilidad...")

        fig = plt.figure(figsize=(16, 12))

        # 1. MTBF vs MTTR
        ax1 = plt.subplot(2, 2, 1)
        self._kpis[['MTBF', 'MTTR']].plot(
            kind='bar', ax=ax1, color=['#2E86C1', '#CB4335'], alpha=0.8
        )
        ax1.set_title('Confiabilidad: MTBF vs MTTR',
                       fontsize=12, fontweight='bold')
        ax1.set_ylabel('Horas')
        ax1.legend(["MTBF (Confiabilidad)", "MTTR (Mantenibilidad)"])
        ax1.grid(axis='y', linestyle='--', alpha=0.3)

        # 2. Disponibilidad
        ax2 = plt.subplot(2, 2, 2)
        target = self.umbrales.disponibilidad_target
        colors = [
            '#28B463' if x > target else '#F1C40F' if x > target - 10
            else '#E74C3C'
            for x in self._kpis['Disponibilidad']
        ]
        self._kpis['Disponibilidad'].plot(
            kind='bar', ax=ax2, color=colors, alpha=0.8
        )
        ax2.set_title('Disponibilidad Operacional (%)',
                       fontsize=12, fontweight='bold')
        ax2.set_ylabel('Disponibilidad (%)')
        ax2.set_ylim(0, 110)
        ax2.axhline(target, color='black', linestyle='--', alpha=0.5,
                     label=f'Target {target:.0f}%')
        ax2.legend()
        ax2.grid(axis='y', linestyle='--', alpha=0.3)

        # 3. MTTF por equipo (NUEVO)
        ax3 = plt.subplot(2, 2, 3)
        self._kpis['MTTF'].plot(
            kind='bar', ax=ax3, color='#8E44AD', alpha=0.8
        )
        ax3.set_title('MTTF: Tiempo Hasta Primera Falla',
                       fontsize=12, fontweight='bold')
        ax3.set_ylabel('Horas')
        ax3.grid(axis='y', linestyle='--', alpha=0.3)

        # 4. Curva de la Bañera (Simulación)
        ax4 = plt.subplot(2, 2, 4)
        t, tasa = self._simular_curva_banera()
        ax4.plot(t, tasa, color='#8E44AD', linewidth=3,
                 label='Tasa de Fallas lambda(t)')
        ax4.fill_between(t, tasa, color='#8E44AD', alpha=0.1)

        ax4.annotate('Mortalidad Infantil', xy=(5, 4), xytext=(15, 5),
                     arrowprops=dict(facecolor='black', shrink=0.05, width=1))
        ax4.annotate('Vida Util (Fallas Aleatorias)',
                     xy=(50, 0.5), xytext=(40, 2),
                     arrowprops=dict(facecolor='black', shrink=0.05, width=1))
        ax4.annotate('Zona de Desgaste (Wear-out)',
                     xy=(90, 6), xytext=(70, 8),
                     arrowprops=dict(facecolor='black', shrink=0.05, width=1))

        ax4.set_title('Curva de la Banera (Bathtub Curve)',
                       fontsize=12, fontweight='bold')
        ax4.set_xlabel('Tiempo de Vida del Activo')
        ax4.set_ylabel('Tasa de Fallas lambda')
        ax4.grid(True, linestyle=':', alpha=0.6)
        ax4.legend()

        fig.suptitle('Dashboard de Confiabilidad Industrial v2.0',
                     fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        fig.savefig(ruta_salida, dpi=300, bbox_inches='tight')
        plt.close(fig)

        logger.info(f"Dashboard guardado: {ruta_salida}")
        return ruta_salida

    @staticmethod
    def _simular_curva_banera() -> tuple[np.ndarray, np.ndarray]:
        """Simula la tasa de fallas para la Curva de la Bañera.

        Returns:
            Tupla (tiempo, tasa_total) con 100 puntos simulados.
        """
        t = np.linspace(0, 100, 100)
        mortalidad_infantil = 5 * np.exp(-0.1 * t)
        vida_util = np.full_like(t, 0.5)
        desgaste = 0.02 * np.exp(0.06 * t)
        tasa_total = mortalidad_infantil + vida_util + desgaste
        return t, tasa_total

    # ----------------------------------------------------------------
    # PROPIEDADES DE ACCESO
    # ----------------------------------------------------------------
    @property
    def datos(self) -> pd.DataFrame | None:
        """DataFrame con los datos crudos cargados."""
        return self._df

    @property
    def kpis(self) -> pd.DataFrame | None:
        """DataFrame con los KPIs calculados."""
        return self._kpis


# ============================================================================
# PUNTO DE ENTRADA CLI
# ============================================================================
def main(filepath: str = 'historial_fallas.csv',
         output_dir: str = 'reports') -> None:
    """Ejecuta el análisis completo de confiabilidad.

    Args:
        filepath: Ruta al CSV con historial de fallas.
        output_dir: Directorio para guardar los gráficos.
    """
    logger.info("=" * 50)
    logger.info("  SISTEMA DE ANALISIS DE CONFIABILIDAD IIoT v2.0")
    logger.info("=" * 50)

    engine = ReliabilityEngine(filepath)
    kpis = engine.calcular_kpis()
    engine.generar_recomendaciones()

    # Mostrar resultados en consola
    print("\n--- METRICAS POR ACTIVO ---")
    print(kpis[['Num_Fallas', 'MTBF', 'MTTR', 'MTTF',
                'Disponibilidad']].round(2))

    print("\n--- PLAN DE ACCION RECOMENDADO ---")
    for equipo, rec in kpis['Recomendacion'].items():
        print(f"  > {equipo}: {rec}")

    engine.visualizar_resultados(output_dir)

    logger.info("Analisis finalizado exitosamente.")


if __name__ == '__main__':
    main()
