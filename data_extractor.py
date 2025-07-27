from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
)

def extract(article_text):
    # In a real scenario, this function would use NLP to extract data.
    # For this example, it returns a fixed JSON object.
    prompt = '''
From the below news article, extract revenue and eps in JSON format containing following keys: 
'revenue_actual', 'revenue_actual', 'revenue_expected', 'eps_actual', 'eps_expected'

Each value should have unit million or billion as part of value string

Only return the valid JSON. No Premble.
Article
=========
{article}
'''
    pt = PromptTemplate.from_template(prompt)

    chain = pt | llm
    response = chain.invoke({"article" : article_text})
    response.content

    parser = JsonOutputParser()
    output_json = parser.parse(response.content)

    return output_json