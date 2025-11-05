import json
from typing import List
from openai import OpenAI
from config import config
from models.message import Message


client = OpenAI(api_key=config.deepseek_api_key, base_url="https://api.deepseek.com")


def read_file_content(file_name):
    """读取文件内容"""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"文件 {file_name} 未找到。")
        return ""


def generate_system_prompt(repository_type: List[str]):
    """根据 repository_type 枚举值，读取对应的文件内容并合并"""
    system_prompt = """
    您是一位乐于助人的助手。

    请使用以下上下文作为您已掌握的知识，并将其放入 `<context></context>` XML 标签内。

    <context>
    """

    for member in repository_type:
        file_name = f"llm/prompt/{member}.md"  # 构造文件名
        content = read_file_content(file_name)
        system_prompt += content + "\n"
    file_name = f"llm/prompt/HotelOverviewAndCoreIdentity.md"
    content = read_file_content(file_name)
    system_prompt += content + "\n"
    system_prompt += """
    </context>

    回答用户问题时：

    - 如果您不知道，请直接说明您不知道。

    - 如果您不确定，请请求用户进一步解释。

    避免提及您是从上下文中获取的信息。

    并根据用户问题的语言进行回答。
    """
    return system_prompt.strip()


def get_result(messages: List[Message], repository_types: List[str]):
    content = [{"role": "system", "content": generate_system_prompt(repository_types)}]
    for message in messages:
        content.append(
            {
                "role": "assistant" if message.position == "left" else "user",
                "content": message.content,
            }
        )
    response = client.chat.completions.create(model="deepseek-chat", messages=content)
    return response.choices[0].message.content
