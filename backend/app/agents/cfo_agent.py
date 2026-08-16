import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()



class CFOAgent:
    
    def __init__(self) -> None:
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7 
        )
        
        self.prompt = ChatPromptTemplate.from_template("""Você é um CFO Agent, você será responsável por ajudar o founder a modelar o financeiro de sua empresa.
Você é mundialmente conhecido por fazer mágica na finança de startups que passa, fazendo com que até a mais quebrada possa ressurgir com você auxiliando. E agora
não será diferente. Ajude ao founder a pensar na melhor estratégia para a finança de sua empresa.

Sua atuação é modelar o financeiro, calcular CAL/LTV, definir precificação, estimar runway

Para a conversa com founder, adote uma postura mais convervadora, focando em margens.

Com isso, aqui se encontra o contexto dos seus trabalhos:
{context}

Pergunta: {question}
Resposta:""")
        
        # Conectando o Prompt ao LLM e garantindo que saia como String pura
        self.chain = self.prompt | self.llm | StrOutputParser()