import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 动态获取根目录的 .env 文件
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(root_dir, '.env')
load_dotenv(env_path)

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("❌ 没有读取到 API Key，请检查根目录下的 .env 文件！")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def generate_test_cases(api_doc_path):
    with open(api_doc_path, 'r', encoding='utf-8') as f:
        api_doc = f.read()

    prompt = f"""
    你是一个资深电商测试专家。请根据以下接口文档和双十一业务规则，生成 15 条测试用例。

    【极其严格的约束】
    1. 正常和边界场景，期望状态码填 200；所有异常场景（缺字段、类型错、金额<=0），期望状态码填 400。
    2. 必须测试边界值（如 299.99, 300, 300.01）。
    3. 必须测试组合场景（如 VIP+满减+优惠券）。
    4. 传参时必须严格遵守 request_body 里的类型要求。

    接口文档：{api_doc}

    请严格输出如下格式的 JSON 数组，不要任何多余的解释，不要带 ```json 标记：
    [
        {{
            "case_name": "用例名称",
            "api_path": "/cart/checkout",
            "data": {{"total_amount": 300.0, "user_level": "VIP", "has_coupon": true}},
            "expected_status": 200
        }}
    ]
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    result_text = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(result_text)
    except json.JSONDecodeError as e:
        print(f"❌ AI 返回的数据不是标准的 JSON 格式:\n{result_text}")
        raise e