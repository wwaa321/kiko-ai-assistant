import SparkApi
import xml.etree.ElementTree as ET
from openai import OpenAI

tree=ET.parse('configuration.xml')
root=tree.getroot()

system_prompt=root.find('llm_setting/system_prompt').text
temperature=float(root.find('llm_setting/temperature').text)

#ollama会话配置-------------------------------------start
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
            messages=message,
            temperature=temperature,
        )
        answer = response.choices[0].message.content
    except Exception as e:
        # 在这里，你可以根据需要记录异常信息，例如：print(e)
        answer = "很抱歉，目前无法处理您的请求，请稍后再试。"

    message.append({"role": "assistant", "content": "{}".format(answer)})
    return answer

#ollama会话配置-------------------------------------end


#阿里云dashscope-------------------------------------start


def conversation_qwen(content):
    qwen_api_key_info=root.find('qwen_api/api_key').text
    qwen_model_info=root.find('qwen_api/model').text
    message.append({"role": "user", "content": "{}".format(content)})
    client = OpenAI(
    api_key=f"{qwen_api_key_info}",  # 替换成真实DashScope的API_KEY
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务endpoint
)

    try:
        response=client.chat.completions.create(
            model=qwen_model_info,
            messages=message,
            temperature=temperature,
        )
        answer=response.choices[0].message.content
    except Exception as e:
        answer= "很抱歉，目前无法处理您的请求，请稍后再试。"
    message.append({"role": "assistant", "content": "{}".format(answer)})
    return answer


#阿里云dashscope------------------------------------end

#月之暗面Kimi---------------------------------start
def conversation_kimi(content):
    kimi_api_key_info=root.find('kimi_api/api_key').text
    kimi_model_info=root.find('kimi_api/model').text
    message.append({"role": "user", "content": "{}".format(content)})
    client = OpenAI(
    api_key=f"{kimi_api_key_info}",  
    base_url="https://api.moonshot.cn/v1", 
    )
    try:
        response=client.chat.completions.create(
            model=kimi_model_info,
            messages=message,
            temperature=temperature,
        )
        answer=response.choices[0].message.content
    except Exception as e:
        answer= "很抱歉，目前无法处理您的请求，请稍后再试。"
    message.append({"role": "assistant", "content": "{}".format(answer)})
    return answer
    


#讯飞星火-------------------------------------start
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
    
