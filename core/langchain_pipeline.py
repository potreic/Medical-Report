# core/langchain_pipeline.py
from config.settings import OPENROUTER_API_KEY
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def generate_medical_report(transcribed_text: str) -> str:
    """
    Takes doctor–patient consultation text and generates
    a structured medical report using DeepSeek via OpenRouter API.
    """
    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3.1:free",
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.2,
    )

    prompt_template = ChatPromptTemplate.from_template("""
    You are a professional medical scribe.
    Convert the following doctor-patient consultation into a structured medical report.

    The report must contain these sections in Markdown:
    - **Patient Information**
    - **Symptoms**
    - **Diagnosis**
    - **Prescription / Treatment Plan**
    - **Doctor's Notes**

    Be objective, concise, and avoid adding unverified information.

    Transcript:
    {transcript}
    """)

    messages = prompt_template.format_messages(transcript=transcribed_text)
    parser = StrOutputParser()
    response = llm.invoke(messages)

    return parser.parse(response.content)
