import streamlit as st 
import pandas as pd 
 
st.set_page_config(page_title="Modelador AWS para IA", layout="wide") 
 
CASO_BASE = { 
    "sector": "Asegurador", 
    "documentos_diarios": 18000, 
    "usuarios_simultaneos": 220, 
    "latencia_max_seg": 4, 
    "pii": True, 
    "presupuesto": "Medio", 
    "variabilidad_demanda": "Media", 
    "preferencia_estrategica": "Gestionado", 
    "disponibilidad_objetivo": "Alta", 
} 
 
 
def recomendar_inferencia(preferencia_estrategica): 
    if preferencia_estrategica == "Gestionado": 
        return "Amazon Bedrock" 
    return "SageMaker" 
 
 
def recomendar_seguridad(pii): 
    if pii: 
        return ( 
            "Controles reforzados: minimización de datos, revisión " 
            "humana, cumplimiento y segmentación." 
        ) 
    return "Controles estándar de acceso y gobierno." 
 
 
def recomendar_observabilidad(variabilidad_demanda): 
    if variabilidad_demanda == "Alta": 
        return ( 
            "Alertas automáticas de coste y monitoreo reforzado de " 
            "inferencia." 
        ) 
    if variabilidad_demanda == "Media": 
        return "Monitoreo continuo con revisión periódica de consumo." 
    return "Observabilidad básica y revisión mensual." 
 
 
def generar_tradeoff(preferencia_estrategica): 
    if preferencia_estrategica == "Gestionado": 
        return ( 
            "Se prioriza velocidad de lanzamiento y simplicidad " 
            "operativa frente a control fino." 
        ) 
    return ( 
        "Se prioriza control fino y personalización frente a rapidez " 
        "de despliegue." 
    ) 
 
 
def generar_capas(datos): 
    capas = { 
        "Datos": ( 
            "Repositorio documental y fuentes internas del área de " 
            "siniestros." 
        ), 
        "Integración": ( 
            "Flujos de entrada/salida y orquestación entre documentos, " 
            "consultas y motor de recomendación."
             ), 
        "Inferencia/Modelo": recomendar_inferencia( 
            datos["preferencia_estrategica"] 
        ), 
        "Aplicación": "Interfaz interna para gestores y analistas.", 
        "Seguridad y Gobierno": recomendar_seguridad(datos["pii"]), 
        "Observabilidad y FinOps": recomendar_observabilidad( 
            datos["variabilidad_demanda"] 
        ), 
    } 
    return capas 
 
 
def generar_riesgos(datos): 
    riesgos = [ 
        { 
            "Riesgo": "Exposición de datos personales sensibles", 
            "Alternativa/Mitigación": ( 
                "Minimización de datos, revisión humana y control de acceso" 
            ), 
            "Gobernanza": "Compliance + Responsable de Seguridad", 
            "Acción": "Validar tratamiento de PII antes del despliegue", 
        }, 
        { 
            "Riesgo": "Latencia superior al objetivo", 
            "Alternativa/Mitigación": ( 
                "Optimizar flujo y monitorear tiempos de respuesta" 
            ), 
            "Gobernanza": "Arquitecto SI/TI", 
            "Acción": "Definir pruebas de rendimiento", 
        }, 
        { 
            "Riesgo": "Sobrecoste de inferencia", 
            "Alternativa/Mitigación": ( 
                "Alertas de consumo y revisión de uso" 
            ), 
            "Gobernanza": "FinOps / Responsable de Operación", 
            "Acción": "Revisar consumo periódicamente", 
        }, 
    ] 
    return pd.DataFrame(riesgos) 
 
 
def generar_slos(datos): 
    slos = [ 
        { 
            "Indicador": "Latencia máxima objetivo", 
            "Valor propuesto": f"<={datos['latencia_max_seg']} s", 
        }, 
        { 
            "Indicador": "Disponibilidad objetivo", 
            "Valor propuesto": datos["disponibilidad_objetivo"], 
        }, 
        { 
            "Indicador": "Tasa de escalado a humano", 
            "Valor propuesto": ( 
                "Definir umbral para casos ambiguos o sensibles" 
            ), 
        }, 
    ] 
    return pd.DataFrame(slos) 
 
 
st.sidebar.header("Parámetros de entrada") 
 
sector = st.sidebar.text_input("Sector", CASO_BASE["sector"]) 
documentos_diarios = st.sidebar.number_input( 
    "Documentos diarios", min_value=0, value=CASO_BASE["documentos_diarios"] 
) 
usuarios_simultaneos = st.sidebar.number_input( 
 "Usuarios simultáneos", min_value=0, 
    value=CASO_BASE["usuarios_simultaneos"] 
) 
latencia_max_seg = st.sidebar.number_input( 
    "Latencia máxima tolerada (segundos)", min_value=1, 
    value=CASO_BASE["latencia_max_seg"] 
) 
pii = st.sidebar.checkbox( 
    "¿Hay datos personales sensibles (PII)?", value=CASO_BASE["pii"] 
) 
presupuesto = st.sidebar.selectbox( 
    "Presupuesto", ["Bajo", "Medio", "Alto"], index=1 
) 
variabilidad_demanda = st.sidebar.selectbox( 
    "Variabilidad de la demanda", ["Baja", "Media", "Alta"], index=1 
) 
preferencia_estrategica = st.sidebar.selectbox( 
    "Preferencia estratégica", ["Gestionado", "Control fino"], index=0 
) 
disponibilidad_objetivo = st.sidebar.selectbox( 
    "Disponibilidad objetivo", ["Media", "Alta", "Muy alta"], index=1 
) 
 
datos = { 
    "sector": sector, 
    "documentos_diarios": documentos_diarios, 
    "usuarios_simultaneos": usuarios_simultaneos, 
    "latencia_max_seg": latencia_max_seg, 
    "pii": pii, 
    "presupuesto": presupuesto, 
    "variabilidad_demanda": variabilidad_demanda, 
    "preferencia_estrategica": preferencia_estrategica, 
    "disponibilidad_objetivo": disponibilidad_objetivo, 
} 
 
st.title("Modelador de Arquitecturas AWS para IA") 
st.write("Propuesta inicial de arquitectura lógica basada en reglas simples.") 
 
st.subheader("1. Resumen ejecutivo") 
st.write( 
    f"Para el sector {datos['sector']}, la arquitectura propuesta prioriza " 
    f"{'simplicidad y rapidez' if datos['preferencia_estrategica'] == 'Gestionado' else 
'control y personalización'} " 
    f"teniendo en cuenta latencia, sensibilidad del dato y operación." 
) 
 
st.subheader("2. Arquitectura propuesta por capas") 
capas = generar_capas(datos) 
for capa, descripcion in capas.items(): 
    st.markdown(f"**{capa}:** {descripcion}") 
 
st.subheader("3. Trade-off principal") 
st.write(generar_tradeoff(datos["preferencia_estrategica"])) 
 
st.subheader("4. Matriz RAGA") 
st.dataframe(generar_riesgos(datos), use_container_width=True) 
 
st.subheader("5. SLO/SLA propuestos") 
st.dataframe(generar_slos(datos), use_container_width=True) 
 
st.subheader("6. Reflexión del equipo") 
st.info( 
    "Añadid aquí vuestra justificación final: " 
    "¿qué decisión tomáis vosotros y por qué?" 
) 