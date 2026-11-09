from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/cart/checkout', methods=['POST'])
def checkout():
    data = request.json

    # 1. 防御：请求体必须是 JSON 字典
    if not isinstance(data, dict):
        return jsonify({"msg": "请求体格式错误"}), 400

    # 2. 防御：检查必填字段
    if 'total_amount' not in data or 'user_level' not in data or 'has_coupon' not in data:
        return jsonify({"msg": "缺少必填字段"}), 400

    # 3. 防御：检查金额类型，防止传字符串导致崩溃
    try:
        total_amount = float(data['total_amount'])
    except (ValueError, TypeError):
        return jsonify({"msg": "金额必须是数字"}), 400

    user_level = data['user_level']
    has_coupon = data['has_coupon']

    # 4. 防御：检查布尔值和枚举值
    if not isinstance(has_coupon, bool):
        return jsonify({"msg": "has_coupon必须是布尔值"}), 400
    if user_level not in ['NORMAL', 'VIP']:
        return jsonify({"msg": "用户等级非法"}), 400

    # 5. 防御：金额必须大于 0
    if total_amount <= 0:
        return jsonify({"msg": "总价必须大于0"}), 400

    # 6. 核心业务逻辑计算
    final_price = total_amount
    if total_amount >= 300:
        final_price -= 50
    if user_level == 'VIP':
        final_price = final_price * 0.9
    if has_coupon:
        final_price -= 20

    if final_price < 0:
        final_price = 0

    return jsonify({
        "msg": "结算成功",
        "final_price": round(final_price, 2)
    }), 200


if __name__ == '__main__':
    app.run(port=8080, threaded=True)