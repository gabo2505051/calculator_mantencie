import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ==========================================
# CONFIGURACIÓN Y CARGA DE DATOS
# ==========================================
def cargar_datos(filepath):
    """Carga y preprocesa el historial de fallas."""
    df = pd.read_csv(filepath)
    df['Fecha_Falla'] = pd.to_datetime(df['Fecha_Falla'])
    df['Fecha_Reparacion'] = pd.to_datetime(df['Fecha_Reparacion'])
    
    # Calcular Tiempo de Reparación (TTR) en horas
    df['TTR'] = (df['Fecha_Reparacion'] - df['Fecha_Falla']).dt.total_seconds() / 3600
    return df

# ==========================================
# LÓGICA DE CÁLCULO DE KPIs
# ==========================================
def calcular_kpis(df):
    """Calcula MTBF, MTTR y Disponibilidad por equipo."""
    # Agrupar por equipo
    resumen = df.groupby('ID_Equipo').agg({
        'Fecha_Falla': 'count',
        'TTR': 'sum',
        'Horas_Operacion': 'sum'
    }).rename(columns={'Fecha_Falla': 'Num_Fallas'})
    
    # Fórmulas de Confiabilidad
    resumen['MTTR'] = resumen['TTR'] / resumen['Num_Fallas']
    resumen['MTBF'] = resumen['Horas_Operacion'] / resumen['Num_Fallas']
    resumen['Disponibilidad'] = (resumen['MTBF'] / (resumen['MTBF'] + resumen['MTTR'])) * 100
    resumen['Tasa_Fallas'] = 1 / resumen['MTBF']
    
    return resumen

# ==========================================
# MOTOR DE RECOMENDACIONES
# ==========================================
def generar_recomendaciones(row):
    """Aplica lógica experta para sugerir intervenciones."""
    # Umbrales arbitrarios para fines demostrativos
    MTBF_UMBRAL_BAJO = 150
    MTTR_UMBRAL_ALTO = 10
    
    if row['MTBF'] < MTBF_UMBRAL_BAJO and row['MTTR'] > MTTR_UMBRAL_ALTO:
        return "CRÍTICO: Alta frecuencia de falla y difícil reparación. Realizar RCA y evaluar reemplazo."
    elif row['MTBF'] < MTBF_UMBRAL_BAJO:
        return "ALERTA: Fallas frecuentes. Revisar calidad de componentes y mantenimiento preventivo."
    elif row['MTTR'] > MTTR_UMBRAL_ALTO:
        return "MEJORA: Reparaciones lentas. Optimizar stock de repuestos y capacitación técnica."
    else:
        return "OPTIMO: Equipo operando dentro de parámetros normales."

# ==========================================
# SIMULACIÓN CURVA DE LA BAÑERA
# ==========================================
def simular_curva_banera():
    """Simula la tasa de fallas para mostrar la Curva de la Bañera."""
    t = np.linspace(0, 100, 100)
    # Mortalidad infantil (exponencial decreciente)
    mortalidad_infantil = 5 * np.exp(-0.1 * t)
    # Vida útil (tasa constante)
    vida_util = np.full_like(t, 0.5)
    # Desgaste (exponencial creciente)
    desgaste = 0.02 * np.exp(0.06 * t)
    
    tasa_total = mortalidad_infantil + vida_util + desgaste
    return t, tasa_total

# ==========================================
# VISUALIZACIÓN
# ==========================================
def visualizar_resultados(resumen):
    """Genera gráficos detallados de KPIs y la Curva de la Bañera."""
    fig = plt.figure(figsize=(16, 10))
    
    # 1. MTBF vs MTTR
    ax1 = plt.subplot(2, 2, 1)
    resumen[['MTBF', 'MTTR']].plot(kind='bar', ax=ax1, color=['#2E86C1', '#CB4335'], alpha=0.8)
    ax1.set_title('Análisis de Confiabilidad: MTBF vs MTTR', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Horas')
    ax1.legend(["MTBF (Confiabilidad)", "MTTR (Mantenibilidad)"])
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    
    # 2. Disponibilidad
    ax2 = plt.subplot(2, 2, 2)
    colors = ['#28B463' if x > 90 else '#F1C40F' if x > 80 else '#E74C3C' for x in resumen['Disponibilidad']]
    resumen['Disponibilidad'].plot(kind='bar', ax=ax2, color=colors, alpha=0.8)
    ax2.set_title('Disponibilidad Operacional (%)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Disponibilidad (%)')
    ax2.set_ylim(0, 110)
    ax2.axhline(90, color='black', linestyle='--', alpha=0.5, label='Target 90%')
    ax2.grid(axis='y', linestyle='--', alpha=0.3)

    # 3. Curva de la Bañera (Simulación)
    ax3 = plt.subplot(2, 1, 2)
    t, tasa = simular_curva_banera()
    ax3.plot(t, tasa, color='#8E44AD', linewidth=3, label='Tasa de Fallas λ(t)')
    ax3.fill_between(t, tasa, color='#8E44AD', alpha=0.1)
    
    # Anotaciones en la curva
    ax3.annotate('Mortalidad Infantil', xy=(5, 4), xytext=(15, 5),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1))
    ax3.annotate('Vida Útil (Fallas Aleatorias)', xy=(50, 0.5), xytext=(40, 2),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1))
    ax3.annotate('Zona de Desgaste (Wear-out)', xy=(90, 6), xytext=(70, 8),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1))
    
    ax3.set_title('Concepto: Curva de la Bañera (Bathtub Curve)', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Tiempo de Vida del Activo')
    ax3.set_ylabel('Tasa de Fallas λ')
    ax3.grid(True, linestyle=':', alpha=0.6)
    ax3.legend()

    plt.tight_layout()
    plt.savefig('analisis_confiabilidad_completo.png')
    print("\n[INFO] Dashboard 'analisis_confiabilidad_completo.png' generado.")

# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    # Asegurar codificación UTF-8 para consola si es posible
    import sys
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("="*50)
    print("      SISTEMA DE ANÁLISIS DE CONFIABILIDAD IIoT")
    print("="*50)
    
    try:
        data = cargar_datos('historial_fallas.csv')
        kpis = calcular_kpis(data)
        kpis['Recomendacion'] = kpis.apply(generar_recomendaciones, axis=1)
        
        print("\n--- MÉTRICAS POR ACTIVO ---")
        print(kpis[['Num_Fallas', 'MTBF', 'MTTR', 'Disponibilidad']].round(2))
        
        print("\n--- PLAN DE ACCIÓN RECOMENDADO ---")
        for equipo, rec in kpis['Recomendacion'].items():
            print(f"▶ {equipo}: {rec}")
            
        visualizar_resultados(kpis)
        print("\n" + "="*50)
        print("Análisis finalizado exitosamente.")
        
    except Exception as e:
        print(f"[ERROR] {e}")
