import os

from langchain.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "AIzaSyBjU1vE37ip2Z5Dx1C_itWsVpf56JlOUo8"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


queries = ["Suggest a recipe for building muscle that also suitable for heart health", "I'm too fatty, I need a diet plan", "What to eat to loose weight and maintain good muscle", "Suggest a food item to gain muscle"]

entities = [{"entity_name" : "build muscle", "entity_type" : "fitness_goal"}, {"entity_name" : "heart health", "entity_type" : "fitness_goal"}, {"entity_name" : "recipe", "entity_type" : "recipe"}]

intent = "Skinny"

# cypher_query = "MATCH (n:Recipe) WHERE n.Skinny = "Yes" AND n.Cardiovascular = "Yes" 

def pmp(query):
    prompt = """You take queries from users and extract entities in a specified format. Also, Please match highly co-related intents from these "muscle gain","weight loss","cardio","muscle maintainance" with the query. 
    Don't make up your own entities, extract from the provided query. Don't Explain anything and dont deviate from the provided format.
    format: {"intent": "", "entities": [{"entity_name": "", "entity_type":"", "score": 0}]}
    query: """ + query + """ 
    answer: """
    return prompt

for q in queries:
    print(q)
    response = llm.invoke(pmp(q))
    print(response.content)
    print(type(response.content))
