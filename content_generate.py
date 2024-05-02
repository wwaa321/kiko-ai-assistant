import SparkApi
import xml.etree.ElementTree as ET
from openai import OpenAI

tree=ET.parse('configuration.xml')
root=tree.getroot()

system_prompt=root.find('llm_setting/system_prompt').text

#ollama-------------------------------------
now_ollama_url=root.find('ollama_api/api_url').text

client = OpenAI(
    base_url = now_ollama_url,
    api_key='ollama', # required, but unused
)

message=[{"role": "system", "content": "{}".format(system_prompt)},
  ]

def conversation_ollama(content):
    llm_model=root.find('ollama_api/model').text

    message.append({"role": "user", "content": "{}".format(content)})
    try:
        response = client.chat.completions.create(
            model=llm_model,
            messages=message
        )
        answer = response.choices[0].message.content
    except Exception as e:
        # 在这里，你可以根据需要记录异常信息，例如：print(e)
        answer = "很抱歉，目前无法处理您的请求，请稍后再试。"

    message.append({"role": "assistant", "content": "{}".format(answer)})
    return answer

#ollama-------------------------------------


#qwen-------------------------------------
import dashscope
from http import HTTPStatus


qwen_api_key_info=root.find('qwen_api/api_key').text
qwen_model_info=root.find('qwen_api/model').text

dashscope.api_key = qwen_api_key_info
def conversation_qwen(content):
    
    resp=dashscope.Generation.call(
        model="{}".format(qwen_model_info),
        prompt=content,
    )

    if resp.status_code == HTTPStatus.OK:
        answer = resp.output['text']

        return answer
    else:

        return "很抱歉，目前无法处理您的请求，请稍后再试。"


#qwen-------------------------------------



#讯飞星火-------------------------------------
#以下密钥信息从控制台获取
appid = root.find('xinghuo_api/appid').text  #填写控制台中获取的 APPID 信息
api_secret = root.find('xinghuo_api/api_secret').text  #填写控制台中获取的 APISecret 信息
api_key = root.find('xinghuo_api/api_key').text 
version = root.find('xinghuo_api/version').text   

if version=="v1.5":

    domain = "general"   # v1.5版本
    Spark_url = "wss://spark-api.xf-yun.com/v1.1/chat"  #v1.5环境的地址

if version=="v2.0":
    domain = "generalv2"
    Spark_url = "wss://spark-api.xf-yun.com/v2.1/chat" 

if version=="v3.0":
    domain = "generalv3"
    Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat" 

if version=="v3.5":
    domain = "generalv3"
    Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat" 

context =[{"role":"system","content":"{}".format(system_prompt)}]

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    context.append(jsoncon)
    return context

def getlength(context):
    length = 0
    for content in context:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(context):
    while (getlength(context) > 8000):
        del context[0]
    return context
    

def conversation(content):
    #context.clear()
    answer = ""  # 定义一个变量用于存储回答

    question=checklen(getText("user",content))
    SparkApi.answer=""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    answer = SparkApi.answer  # 将回答赋值给变量
    getText("assistant", answer)
    if answer=='':
        answer='远程响应错误，请查看API余额或稍后再试。'
    return answer
    
