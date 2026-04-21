import streamlit as st 
import pandas as pd 

st.set_page_config(page_title="Modelador AWS para IA - v2", layout="wide") 

# --- CASO BASE ---
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

# --- LÓGICA DE NEGOCIO (REGLAS DE DECISIÓN) ---

def recomendar_inferencia(preferencia_estrategica, pii): 
    # CAMBIO: La seguridad ahora prima sobre la preferencia estratégica.
    # Si hay PII, SageMaker es más robusto para aislamiento, o Bedrock requiere VPC Endpoints.
    if pii and preferencia_estrategica == "Control fino":
        return "Amazon SageMaker (Aislamiento total y control de VPC)"
    if preferencia_estrategica == "Gestionado": 
        return "Amazon Bedrock (Serverless - Mayor agilidad)" 
    return "Amazon SageMaker" 

def recomendar_seguridad(pii): 
    if pii: 
        return ( 
            "Capa de anonimización (Lambda), encriptación KMS y " 
            "aislamiento mediante AWS PrivateLink." 
        ) 
    return "Controles estándar de IAM y Service Control Policies." 

def recomendar_observabilidad(variabilidad_demanda): 
    # CAMBIO: Se enfoca en métricas específicas de IA (tokens y latencia).
    if variabilidad_demanda == "Alta": 
        return "Amazon CloudWatch con métricas personalizadas de tokens y alertas FinOps en tiempo real." 
    return "Monitoreo estándar de infraestructura y costes mensuales." 

def generar_tradeoff(preferencia_estrategica, pii): 
    if pii and preferencia_estrategica == "Gestionado":
        return "EQUILIBRIO CRÍTICO: Se busca rapidez (Bedrock) pero con alta carga en gobierno de datos y privacidad."
    if preferencia_estrategica == "Gestionado": 
        return "Simplicidad operativa y Time-to-Market optimizado." 
    return "Control total sobre el modelo y la infraestructura a costa de mayor complejidad técnica." 

def generar_capas(datos): 
    # CAMBIO: Se introduce el concepto de RAG y base de datos vectorial.
    capas = { 
        "Datos": ( 
            "S3 (Documentos) + Amazon Kendra o OpenSearch (Base Vectorial para RAG)." 
        ), 
        "Integración/Orquestación": ( 
            "LangChain o AWS Step Functions para flujo de consulta y limpieza de PII."
             ), 
        "Inferencia/Modelo": recomendar_inferencia( 
            datos["preferencia_estrategica"], datos["pii"]
        ), 
        "Aplicación": "Frontend en Streamlit/CloudFront para gestores de siniestros.", 
        "Seguridad": recomendar_seguridad(datos["pii"]), 
        "FinOps": recomendar_observabilidad(datos["variabilidad_demanda"]), 
    } 
    return capas 

def generar_riesgos(datos): 
    # CAMBIO: Se añaden riesgos reales de IA (Alucinaciones) y su mitigación (RAG).
    riesgos = [ 
        { 
            "Riesgo": "Alucinaciones en borradores", 
            "Alternativa/Mitigación": "Arquitectura RAG y validación 'Human-in-the-loop'", 
            "Gobernanza": "Product Owner / Negocio", 
            "Acción": "Implementar umbrales de confianza en el modelo", 
        }, 
        { 
            "Riesgo": "Exposición de PII", 
            "Alternativa/Mitigación": "Detección con Amazon Macie y filtrado previo", 
            "Gobernanza": "CISO / Compliance", 
            "Acción": "Auditoría de logs antes de producción", 
        }, 
        { 
            "Riesgo": "Latencia en concurrencia", 
            "Alternativa/Mitigación": "Provisioned Throughput (Bedrock) / Autoscaling", 
            "Gobernanza": "Arquitecto Cloud", 
            "Acción": "Pruebas de carga con 220 usuarios", 
        }, 
    ] 
    return pd.DataFrame(riesgos) 

def generar_slos(datos): 
    slos = [ 
        { 
            "Indicador": "Latencia máxima", 
            "Valor propuesto": f"<={datos['latencia_max_seg']} s (p99)", 
        }, 
        { 
            "Indicador": "Exactitud de respuesta", 
            "Valor propuesto": ">95% (Validación contra Base de Conocimiento)", 
        }, 
        { 
            "Indicador": "Disponibilidad", 
            "Valor propuesto": datos["disponibilidad_objetivo"], 
        }, 
    ] 
    return pd.DataFrame(slos) 

# --- INTERFAZ (INPUTS) ---

st.sidebar.header("Configuración del Sistema") 

sector = st.sidebar.text_input("Sector", CASO_BASE["sector"]) 
documentos_diarios = st.sidebar.number_input( 
    "Documentos diarios", min_value=0, value=CASO_BASE["documentos_diarios"] 
) 
usuarios_simultaneos = st.sidebar.number_input( 
 "Usuarios simultáneos", min_value=0, value=CASO_BASE["usuarios_simultaneos"] 
) 
latencia_max_seg = st.sidebar.number_input( 
    "Latencia objetivo (seg)", min_value=1, value=CASO_BASE["latencia_max_seg"] 
) 
pii = st.sidebar.checkbox( 
    "¿Contiene PII?", value=CASO_BASE["pii"] 
) 
presupuesto = st.sidebar.selectbox( 
    "Presupuesto", ["Bajo", "Medio", "Alto"], index=1 
) 
variabilidad_demanda = st.sidebar.selectbox( 
    "Variabilidad", ["Baja", "Media", "Alta"], index=1 
) 
preferencia_estrategica = st.sidebar.selectbox( 
    "Estrategia", ["Gestionado", "Control fino"], index=0 
) 
disponibilidad_objetivo = st.sidebar.selectbox( 
    "Disponibilidad", ["Media", "Alta", "Muy alta"], index=1 
) 

datos = { 
    "sector": sector, "documentos_diarios": documentos_diarios, 
    "usuarios_simultaneos": usuarios_simultaneos, "latencia_max_seg": latencia_max_seg, 
    "pii": pii, "presupuesto": presupuesto, "variabilidad_demanda": variabilidad_demanda, 
    "preferencia_estrategica": preferencia_estrategica, "disponibilidad_objetivo": disponibilidad_objetivo, 
} 

# --- CONSTRUCCIÓN DEL MEMO (OUTPUTS) ---

st.title("Reporte de Arquitectura IA: Asistente de Siniestros") 

# Alerta de coherencia (Mejora didáctica)
if datos["documentos_diarios"] > 15000 and datos["presupuesto"] == "Bajo":
    st.warning("**Aviso de diseño**: El volumen de documentos es alto para un presupuesto bajo. Considere optimizar el índice vectorial.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Propuesta por Capas") 
    capas = generar_capas(datos) 
    for capa, descripcion in capas.items(): 
        st.markdown(f"**{capa}:** {descripcion}") 

with col2:
    st.subheader("2. Trade-off Estratégico") 
    st.info(generar_tradeoff(datos["preferencia_estrategica"], datos["pii"])) 

st.subheader("3. Matriz de Riesgos y Mitigación") 
st.table(generar_riesgos(datos)) # Uso de table para mejor lectura de riesgos

st.subheader("4. Definición de SLOs") 
st.dataframe(generar_slos(datos), use_container_width=True) 

st.subheader("5. Reflexión Final") 
st.info("Justificad vuestra elección final: ¿Cómo equilibra esta arquitectura la latencia con la seguridad de los datos PII?")