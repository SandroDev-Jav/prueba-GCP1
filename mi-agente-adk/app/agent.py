import os
from google.cloud import storage
from pypdf import PdfReader
from io import BytesIO
from google.adk.agents import Agent

BUCKET_NAME = os.getenv("informacion-prueba")
PDF_PATH = os.getenv(
    "procesos/3 PROCESO DE ASIGNACIÓN DE EQUIPO DE CÓMPUTO.pdf"
)  # Ejemplo: "documentos/proceso.pdf"


def leer_pdf_gcs() -> str:
    """Lee el archivo PDF almacenado en Google Cloud Storage y extrae su texto."""
    if not BUCKET_NAME or not PDF_PATH:
        return "Error: Las variables de entorno GCS_BUCKET_NAME o PDF_FILE_PATH no están configuradas."

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(PDF_PATH)

        pdf_bytes = blob.download_as_bytes()
        reader = PdfReader(BytesIO(pdf_bytes))

        texto_completo = ""
        for i, page in enumerate(reader.pages):
            texto_completo += f"--- Página {i + 1} ---\n" + page.extract_text() + "\n"

        return texto_completo
    except Exception as e:
        return f"Error al leer el archivo PDF desde GCS: {str(e)}"


def buscar_en_proceso_pdf(query: str) -> str:
    """
    Herramienta que busca información dentro del documento PDF del proceso almacenado en GCS.
    """
    contenido_pdf = leer_pdf_gcs()
    if contenido_pdf.startswith("Error"):
        return contenido_pdf

    # Retorna el texto para que el modelo analice la consulta basándose en el contexto del PDF
    return contenido_pdf


# Configuración del Agente ADK
agente_proceso = Agent(
    name="AgenteConsultorProcesos",
    model="gemini-2.5-flash",
    instruction=(
        "Eres un asistente especializado en responder preguntas sobre el proceso interno "
        "documentado en un archivo PDF alojado en Cloud Storage. Utiliza la herramienta "
        "buscar_en_proceso_pdf para obtener la información necesaria antes de responder."
    ),
    tools=[buscar_en_proceso_pdf],
)
