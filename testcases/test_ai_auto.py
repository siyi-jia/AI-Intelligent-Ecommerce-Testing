import sys
import os
import pytest
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.ai_generator import generate_test_cases

# 调用 AI 生成用例
print("⌛ 正在请求 AI 生成测试用例...")
ai_cases = generate_test_cases("api_docs/user_api.json")


# 获取干净的用例名，防止乱码
case_ids = [str(c.get("case_name", "Unnamed")).encode('utf-8').decode('utf-8') for c in ai_cases]

@pytest.mark.parametrize("case", ai_cases, ids=case_ids)
def test_ai_generated_api(case):
    url = f"http://127.0.0.1:8080{case['api_path']}"

    # 发送请求
    response = requests.post(url, json=case["data"])

    # 断言并打印详细报错信息
    assert response.status_code == case["expected_status"], (
        f"\n❌ 用例失败: {case['case_name']}"
        f"\n📦 传入参数: {case['data']}"
        f"\n🎯 期望状态码: {case['expected_status']}"
        f"\n📉 实际状态码: {response.status_code}"
        f"\n📄 服务器返回: {response.text}"
    )