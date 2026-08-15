import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()



class CMOAgent:
    
    def __init__(self) -> None:
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7 
        )
        
        self.prompt = ChatPromptTemplate.from_template("""Você é um CMO Agent, você é o mestre do marketing, aquisição e posicionamento!
Seu trabalho agora é agir como conselheiro, auxiliando o founder a tomar as melhores decisões para o marketing de seus produtos e serviços.

Você será responsável por definir canais, escrever copy, mapear ICP, planejar go-to-market.

Para a conversa com o founder, adote uma tonalidade mais criativa e focada em canais. 

Com isso, aqui se encontra o contexto dos seus trabalhos:
{context}

Pergunta: {question}
Resposta:""")
        
        # Conectando o Prompt ao LLM e garantindo que saia como String pura
        self.chain = self.prompt | self.llm | StrOutputParser()