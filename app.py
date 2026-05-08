"""
Interfaz Gráfica - Calculadora de Confiabilidad Industrial
==========================================================
Proyecto 2 - Portafolio IIoT

Dashboard interactivo en Streamlit para el motor de confiabilidad.
Permite cargar datos, ajustar umbrales en tiempo real y visualizar
los resultados y recomendaciones.
"""

# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import os
import tempfile
from reliability_calculator import ReliabilityEngine, UmbralesConfiabilidad

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="IIoT Reliability Calc",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados (Glassmorphism & Industrial)
st.markdown("""
<style>
    .metric-card {
        background-color: rgba(41, 128, 185, 0.15);
        border-radius: 8px;
        padding: 20px;
        border-left: 5px solid #3498db;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #ecf0f1;
    }
    .metric-label {
        font-size: 13px;
        color: #bdc3c7;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .recommendation-alert {
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 12px;
        font-size: 15px;
        border: 1px solid rgba(255,255,255,0.05);
        color: #ecf0f1;
    }
    .rec-critico { background-color: rgba(231, 76, 60, 0.15); border-left: 5px solid #e74c3c; }
    .rec-alerta { background-color: rgba(243, 156, 18, 0.15); border-left: 5px solid #f39c12; }
    .rec-mejora { background-color: rgba(52, 152, 219, 0.15); border-left: 5px solid #3498db; }
    .rec-optimo { background-color: rgba(46, 204, 113, 0.15); border-left: 5px solid #2ecc71; }
    .rec-degradacion { background-color: rgba(155, 89, 182, 0.15); border-left: 5px solid #9b59b6; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# ENCABEZADO
# ==========================================
st.title("⚙️ Calculadora de Confiabilidad Industrial")
st.markdown("Plataforma interactiva para análisis de **MTBF, MTTR, MTTF** y generación de recomendaciones mediante inteligencia de mantenimiento.")

# ==========================================
# SIDEBAR: CONTROLES
# ==========================================
st.sidebar.header("🎛️ Panel de Control")

uploaded_file = st.sidebar.file_uploader("1. Cargar Historial de Fallas (CSV)", type=['csv'])

archivo_ruta = 'historial_fallas.csv' # Dataset por defecto
archivo_temporal = False

if uploaded_file:
    # Guardar archivo cargado temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
        tmp.write(uploaded_file.getvalue())
        archivo_ruta = tmp.name
        archivo_temporal = True
else:
    st.sidebar.info("👆 Carga un archivo CSV propio o usa el dataset simulado por defecto.")

st.sidebar.markdown("---")
st.sidebar.subheader("2. Ajuste de Umbrales")
st.sidebar.markdown("Ajusta los criterios de decisión en tiempo real:")

umbral_mtbf = st.sidebar.slider("Umbral Bajo MTBF (Horas)", min_value=50, max_value=500, value=150, step=10)
umbral_mttr = st.sidebar.slider("Umbral Alto MTTR (Horas)", min_value=2, max_value=48, value=10, step=1)
target_disp = st.sidebar.slider("Target Disponibilidad (%)", min_value=70, max_value=99, value=90, step=1)
tendencia_f = st.sidebar.slider("Sensibilidad Degradación (Factor)", min_value=1.1, max_value=3.0, value=1.5, step=0.1)

# ==========================================
# PROCESAMIENTO Y RENDERIZADO
# ==========================================
if os.path.exists(archivo_ruta):
    try:
        # 1. Configurar engine con umbrales de la interfaz interactiva
        umbrales = UmbralesConfiabilidad(
            mtbf_umbral_bajo=umbral_mtbf,
            mttr_umbral_alto=umbral_mttr,
            disponibilidad_target=target_disp,
            tendencia_factor=tendencia_f
        )
        engine = ReliabilityEngine(archivo_ruta, umbrales=umbrales)
        
        # 2. Calcular todo
        kpis = engine.calcular_kpis()
        engine.generar_recomendaciones()

        # 3. KPIs Globales de Planta
        st.subheader("📊 Resumen Global de Planta")
        col1, col2, col3, col4 = st.columns(4)
        
        avg_mtbf = kpis['MTBF'].mean()
        avg_mttr = kpis['MTTR'].mean()
        avg_disp = kpis['Disponibilidad'].mean()
        total_fallas = kpis['Num_Fallas'].sum()

        col1.markdown(f'<div class="metric-card"><div class="metric-label">MTBF Promedio</div><div class="metric-value">{avg_mtbf:.1f} hrs</div></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="metric-card"><div class="metric-label">MTTR Promedio</div><div class="metric-value">{avg_mttr:.1f} hrs</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="metric-card"><div class="metric-label">Disponibilidad Media</div><div class="metric-value">{avg_disp:.1f}%</div></div>', unsafe_allow_html=True)
        col4.markdown(f'<div class="metric-card"><div class="metric-label">Fallas Totales</div><div class="metric-value">{int(total_fallas)}</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        
        # 4. Pestañas de Navegación
        tab1, tab2 = st.tabs(["📈 Visualización de Datos", "🛠️ Plan de Acción (Recomendaciones)"])

        with tab1:
            st.subheader("Dashboard Analítico")
            with st.spinner("Generando motores gráficos..."):
                ruta_grafico = engine.visualizar_resultados()
                st.image(ruta_grafico, use_container_width=True)
                
            st.subheader("Datos Estructurados por Activo")
            # Mostrar tabla formateada
            df_mostrar = kpis[['Num_Fallas', 'MTBF', 'MTTR', 'MTTF', 'Disponibilidad']].copy()
            st.dataframe(df_mostrar.style.format("{:.2f}").background_gradient(cmap='Blues', subset=['MTBF']).background_gradient(cmap='Reds', subset=['MTTR']), use_container_width=True)

        with tab2:
            st.subheader("Motor de Recomendaciones Inteligentes")
            st.markdown("Las siguientes recomendaciones se actualizan dinámicamente según los umbrales configurados en el panel lateral.")
            
            for equipo, rec in kpis['Recomendacion'].items():
                # Asignar clase CSS según la condición
                clase_css = ""
                if "CRITICO" in rec: clase_css = "rec-critico"
                elif "ALERTA" in rec: clase_css = "rec-alerta"
                elif "MEJORA" in rec: clase_css = "rec-mejora"
                elif "DEGRADACION" in rec: clase_css = "rec-degradacion"
                else: clase_css = "rec-optimo"
                
                st.markdown(f'<div class="recommendation-alert {clase_css}"><strong>[{equipo}]</strong> - {rec}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error al procesar los datos: {str(e)}")
    finally:
        # Limpieza de archivo temporal si se subió uno
        if archivo_temporal and os.path.exists(archivo_ruta):
            os.remove(archivo_ruta)

else:
    st.warning("⚠️ No se encontró el archivo 'historial_fallas.csv'. Por favor, ejecuta 'python generate_dataset.py' primero o sube tu propio archivo CSV.")
