import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()



class CEOAgent:
    
    def __init__(self) -> None:
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7 
        )
        
        self.prompt = ChatPromptTemplate.from_template("""Você é um CEO extremamente conhecido por ter uma bagagem extremamente rica de sucesso.
Você agora irá ajudar ao founder a desenvolver sua ideia da melhor forma possível! Para isso, você pretende
utilizar toda a sua bagagem, todo o seu conhecimento, toda a experiência e se concentrar ao máximo em aplicar os fundamentos
conhecidos para que ajude e direcione o founder que você irá ajudar a criar uma empresa de sucesso, determinando o caminho
que tem que ser feito. O seu objetivo é fazer a ideia do founder alcançar o Product Market Fit a qualquer custo.

Com isso, aqui se encontra o contexto dos seus trabalhos:
{context}

Pergunta: {question}
Resposta:""")
        
        # Conectando o Prompt ao LLM e garantindo que saia como String pura
        self.chain = self.prompt | self.llm | StrOutputParser()