from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from PIL import Image
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import HumanMessage
import os
import json
import base64
import httpx
from io import BytesIO

image_path = "shreeji-sample-bill.png"

OPENAI_API_KEY = "Your OpenAI key here"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
api_key = os.environ.get("OPENAI_API_KEY")
model = ChatOpenAI(model="gpt-4o")

parser = JsonOutputParser()

image = Image.open(image_path)
buffer = BytesIO()
image.save(buffer, format="PNG")  
image_bytes = buffer.getvalue()
image_data = base64.b64encode(image_bytes).decode("utf-8")

message = HumanMessage(
    content=[
        {"type": "text", "text": "describe the content in this image"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{image_data}"},
        },
    ],
)
response = model.invoke([message])
image_details = response.content

prompt = PromptTemplate(
    template="""You are provided with some details of a bill image. Your task is to fetch the important information for calculating the spending behaviour
  You have to provide the data in Json format. 
  The bill content is as follows:
  {image_details} 
""",
    input_variables=["image_details"]
    
)

chain = prompt | model | parser

print(chain.invoke({"image_details": image_details}))