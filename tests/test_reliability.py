"""
Tests Unitarios - Calculadora de Confiabilidad Industrial
==========================================================
Proyecto 2 - Portafolio IIoT

Valida las fórmulas de MTBF, MTTR, MTTF, Disponibilidad y el motor
de recomendaciones usando datasets controlados.
"""

import os
import sys

import matplotlib
matplotlib.use('Agg')

import pandas as pd
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reliability_calculator import (
    ReliabilityEngine, UmbralesConfiabilidad
)


# ============================================================================
# FIXTURES
# ============================================================================
@pytest.fixture
def csv_basico(tmp_path) -> str:
    """Dataset mínimo con 2 equipos y fallas controladas."""
    data = {
        'ID_Equipo': ['EQ-001', 'EQ-001', 'EQ-002'],
        'Fecha_Falla': [
            '2024-01-10 08:00', '2024-02-15 10:00', '2024-01-20 14:00'
        ],
        'Fecha_Reparacion': [
            '2024-01-10 12:00', '2024-02-15 15:00', '2024-01-21 02:00'
        ],
        'Horas_Operacion': [200, 300, 500]
    }
    df = pd.DataFrame(data)
    ruta = tmp_path / "test_fallas.csv"
    df.to_csv(ruta, index=False)
    return str(ruta)


@pytest.fixture
def csv_tendencia(tmp_path) -> str:
    """Dataset con fallas crecientes para probar detección de tendencia."""
    records = []
    # Primeros 6 meses: 1 falla por mes
    for month in range(1, 7):
        records.append({
            'ID_Equipo': 'EQ-TREND',
            'Fecha_Falla': f'2024-{month:02d}-15 10:00',
            'Fecha_Reparacion': f'2024-{month:02d}-15 14:00',
            'Horas_Operacion': 200
        })
    # Últimos 3 meses: 4 fallas por mes (tendencia creciente)
    for month in range(7, 10):
        for day in [5, 10, 15, 20]:
            records.append({
                'ID_Equipo': 'EQ-TREND',
                'Fecha_Falla': f'2024-{month:02d}-{day:02d} 10:00',
                'Fecha_Reparacion': f'2024-{month:02d}-{day:02d} 14:00',
                'Horas_Operacion': 200
            })
    df = pd.DataFrame(records)
    ruta = tmp_path / "test_tendencia.csv"
    df.to_csv(ruta, index=False)
    return str(ruta)


@pytest.fixture
def engine_basico(csv_basico: str) -> ReliabilityEngine:
    """Engine inicializado con dataset básico."""
    return ReliabilityEngine(csv_basico)


# ============================================================================
# TESTS: CARGA DE DATOS
# ============================================================================
class TestCargarDatos:
    """Tests para la carga y validación de datos."""

    def test_carga_exitosa(self, csv_basico: str) -> None:
        """Verifica carga exitosa de CSV válido."""
        engine = ReliabilityEngine(csv_basico)
        assert engine.datos is not None
        assert len(engine.datos) == 3

    def test_calculo_ttr(self, engine_basico: ReliabilityEngine) -> None:
        """Verifica que el TTR se calcula correctamente."""
        df = engine_basico.datos
        assert 'TTR' in df.columns
        # EQ-001 primera falla: 4 horas de reparación
        ttr_eq001 = df[df['ID_Equipo'] == 'EQ-001'].iloc[0]['TTR']
        assert ttr_eq001 == 4.0

    def test_archivo_no_encontrado(self) -> None:
        """Verifica error con archivo inexistente."""
        with pytest.raises(FileNotFoundError):
            ReliabilityEngine("/ruta/inexistente.csv")

    def test_columnas_faltantes(self, tmp_path) -> None:
        """Verifica error con columnas incorrectas."""
        ruta = tmp_path / "datos_malos.csv"
        pd.DataFrame({'Col_A': [1]}).to_csv(ruta, index=False)
        with pytest.raises(ValueError, match="Columnas faltantes"):
            ReliabilityEngine(str(ruta))


# ============================================================================
# TESTS: CÁLCULO DE KPIs
# ============================================================================
class TestCalcularKPIs:
    """Tests para las fórmulas de confiabilidad."""

    def test_mtbf(self, engine_basico: ReliabilityEngine) -> None:
        """MTBF = Horas_Operacion_Total / Num_Fallas."""
        kpis = engine_basico.calcular_kpis()
        # EQ-001: (200+300)/2 = 250
        assert kpis.loc['EQ-001', 'MTBF'] == 250.0

    def test_mttr(self, engine_basico: ReliabilityEngine) -> None:
        """MTTR = TTR_Total / Num_Fallas."""
        kpis = engine_basico.calcular_kpis()
        # EQ-001: (4+5)/2 = 4.5
        ttr_esperado = (4.0 + 5.0) / 2  # 4h + 5h
        assert kpis.loc['EQ-001', 'MTTR'] == ttr_esperado

    def test_disponibilidad(self, engine_basico: ReliabilityEngine) -> None:
        """Disponibilidad = MTBF / (MTBF + MTTR) * 100."""
        kpis = engine_basico.calcular_kpis()
        mtbf = kpis.loc['EQ-001', 'MTBF']
        mttr = kpis.loc['EQ-001', 'MTTR']
        esperada = (mtbf / (mtbf + mttr)) * 100
        assert abs(kpis.loc['EQ-001', 'Disponibilidad'] - esperada) < 0.01

    def test_tasa_fallas(self, engine_basico: ReliabilityEngine) -> None:
        """Tasa de Fallas = 1 / MTBF."""
        kpis = engine_basico.calcular_kpis()
        assert abs(kpis.loc['EQ-001', 'Tasa_Fallas'] - 1/250.0) < 0.0001

    def test_mttf(self, engine_basico: ReliabilityEngine) -> None:
        """MTTF = Horas de operación hasta primera falla."""
        kpis = engine_basico.calcular_kpis()
        assert 'MTTF' in kpis.columns
        # EQ-001 primera falla: 200 horas
        assert kpis.loc['EQ-001', 'MTTF'] == 200.0

    def test_num_fallas(self, engine_basico: ReliabilityEngine) -> None:
        """Verifica conteo correcto de fallas."""
        kpis = engine_basico.calcular_kpis()
        assert kpis.loc['EQ-001', 'Num_Fallas'] == 2
        assert kpis.loc['EQ-002', 'Num_Fallas'] == 1

    def test_error_sin_datos(self) -> None:
        """Verifica error si no hay datos cargados."""
        engine = ReliabilityEngine()
        with pytest.raises(RuntimeError, match="No hay datos"):
            engine.calcular_kpis()


# ============================================================================
# TESTS: MOTOR DE RECOMENDACIONES
# ============================================================================
class TestRecomendaciones:
    """Tests para el motor de recomendaciones con umbrales."""

    def test_condicion_a_critico(self) -> None:
        """MTBF bajo + MTTR alto → CRÍTICO."""
        umbrales = UmbralesConfiabilidad(
            mtbf_umbral_bajo=200, mttr_umbral_alto=5
        )
        engine = ReliabilityEngine(umbrales=umbrales)
        row = pd.Series({'MTBF': 100, 'MTTR': 15, 'Disponibilidad': 50})
        resultado = engine._evaluar_equipo('TEST', row)
        assert 'CRITICO' in resultado

    def test_condicion_b_alerta(self) -> None:
        """MTBF bajo + MTTR ok → ALERTA."""
        umbrales = UmbralesConfiabilidad(
            mtbf_umbral_bajo=200, mttr_umbral_alto=20
        )
        engine = ReliabilityEngine(umbrales=umbrales)
        row = pd.Series({'MTBF': 100, 'MTTR': 5, 'Disponibilidad': 80})
        resultado = engine._evaluar_equipo('TEST', row)
        assert 'ALERTA' in resultado

    def test_condicion_c_mejora(self) -> None:
        """MTBF ok + MTTR alto → MEJORA."""
        umbrales = UmbralesConfiabilidad(
            mtbf_umbral_bajo=100, mttr_umbral_alto=5
        )
        engine = ReliabilityEngine(umbrales=umbrales)
        row = pd.Series({'MTBF': 500, 'MTTR': 15, 'Disponibilidad': 90})
        resultado = engine._evaluar_equipo('TEST', row)
        assert 'MEJORA' in resultado

    def test_condicion_e_optimo(self) -> None:
        """Todos los indicadores ok → ÓPTIMO."""
        umbrales = UmbralesConfiabilidad(
            mtbf_umbral_bajo=100, mttr_umbral_alto=20
        )
        engine = ReliabilityEngine(umbrales=umbrales)
        row = pd.Series({'MTBF': 500, 'MTTR': 5, 'Disponibilidad': 99})
        resultado = engine._evaluar_equipo('TEST', row)
        assert 'OPTIMO' in resultado

    def test_umbrales_personalizados(self) -> None:
        """Verifica que los umbrales personalizados funcionan."""
        umbrales = UmbralesConfiabilidad(
            mtbf_umbral_bajo=500, mttr_umbral_alto=2
        )
        engine = ReliabilityEngine(umbrales=umbrales)
        # Con umbrales estrictos, un equipo "normal" puede ser ALERTA
        row = pd.Series({'MTBF': 300, 'MTTR': 1, 'Disponibilidad': 90})
        resultado = engine._evaluar_equipo('TEST', row)
        assert 'ALERTA' in resultado


# ============================================================================
# TESTS: DETECCIÓN DE TENDENCIA
# ============================================================================
class TestDeteccionTendencia:
    """Tests para la detección de tendencia de degradación."""

    def test_detecta_degradacion(self, csv_tendencia: str) -> None:
        """Verifica detección de tendencia creciente en fallas."""
        engine = ReliabilityEngine(csv_tendencia)
        engine.calcular_kpis()
        # La tendencia debe detectarse: 4 fallas/mes vs 1 falla/mes
        assert engine._detectar_tendencia('EQ-TREND') == True

    def test_sin_degradacion(self, csv_basico: str) -> None:
        """Verifica que no se detecta tendencia con pocos datos."""
        engine = ReliabilityEngine(csv_basico)
        assert engine._detectar_tendencia('EQ-001') is False


# ============================================================================
# TESTS: VISUALIZACIÓN
# ============================================================================
class TestVisualizacion:
    """Tests para la generación de gráficos."""

    def test_genera_dashboard(self, engine_basico: ReliabilityEngine,
                               tmp_path) -> None:
        """Verifica que el dashboard se genera correctamente."""
        engine_basico.calcular_kpis()
        output_dir = str(tmp_path / "reports")
        ruta = engine_basico.visualizar_resultados(output_dir)
        assert os.path.exists(ruta)
        assert os.path.getsize(ruta) > 0

    def test_crea_directorio(self, engine_basico: ReliabilityEngine,
                              tmp_path) -> None:
        """Verifica que se crea la carpeta de reports automáticamente."""
        engine_basico.calcular_kpis()
        output_dir = str(tmp_path / "nuevo_dir")
        engine_basico.visualizar_resultados(output_dir)
        assert os.path.isdir(output_dir)


# ============================================================================
# TESTS: FLUJO COMPLETO
# ============================================================================
class TestFlujoCompleto:
    """Tests de integración del flujo main()."""

    def test_flujo_completo(self, csv_basico: str, tmp_path) -> None:
        """Verifica el flujo completo: carga → KPIs → recomendaciones → gráficos."""
        engine = ReliabilityEngine(csv_basico)
        kpis = engine.calcular_kpis()
        engine.generar_recomendaciones()

        assert 'Recomendacion' in kpis.columns
        assert len(kpis) == 2

        output_dir = str(tmp_path / "reports")
        ruta = engine.visualizar_resultados(output_dir)
        assert os.path.exists(ruta)
