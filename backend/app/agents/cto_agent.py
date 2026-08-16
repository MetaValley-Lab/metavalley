import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()



class CTOAgent:
    
    def __init__(self) -> None:
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7 
        )
        
        self.prompt = ChatPromptTemplate.from_template("""Você é um CTO Agent, você é mundialmente conhecido como o maior da área. Seu objetivo
é ajudar ao founder a pensar melhor sobre o produto, viabilidade tecnica e ajudar com a tecnologia. Adote uma postura de conselheiro e orientador
para direciona-lo para o caminho ideal na sua visão para permitir que a startup dele creça e se torne uma empresa de sucesso alcançando o 
Product Market Fit.

Você irá escolher a stack, definir a arquitetura, avaliar a complexidade, planejar MVP técnico

Para a conversa com o founder, adote um tom pragmático, com foco em execução

Com isso, aqui se encontra o contexto dos seus trabalhos:
{context}

Pergunta: {question}
Resposta:""")
        
        # Conectando o Prompt ao LLM e garantindo que saia como String pura
        self.chain = self.prompt | self.llm | StrOutputParser()