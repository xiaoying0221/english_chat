import requests
from flask_cors import CORS
from flask import Flask, request, jsonify
from utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = '08159463405d57c9'
APP_SECRET = '6NyH1FXHpa5InNG0bf6AM1pI4kDoIMV8'

app = Flask(__name__)
CORS(app)  # 允许所有来源的请求

def create_request(q, grade, title, model_content, is_need_synonyms, correct_version, is_need_essay_report):
    '''
    创建一个请求发送到有道英文作文批改API。
    参数说明请参考文档: https://ai.youdao.com/DOCSIRMA/html/learn/api/yyzwpgwbsr/index.html
    '''
    # 请求参数
    data = {
        'q': q,  # 正文内容，必填
        'grade': grade,  # 作文等级，必填
        'title': title,  # 作文标题，可选
        'modelContent': model_content,  # 作文参考范文，可选
        'isNeedSynonyms': is_need_synonyms,  # 是否需要查询同义词，"true" 或 "false"
        'correctVersion': correct_version,  # 作文批改版本：基础 或 高级，必填
        'isNeedEssayReport': is_need_essay_report  # 是否返回写作报告，"true" 或 "false"
    }

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = do_call('https://openapi.youdao.com/v2/correct_writing_text', header, data, 'post')
    return res.json()

def do_call(url, header, params, method):
    if method == 'get':
        return requests.get(url, params=params, headers=header)
    elif method == 'post':
        return requests.post(url, data=params, headers=header)

# 创建Flask API端点
@app.route('/correct_writing', methods=['POST'])
def correct_writing():
    req_data = request.get_json()
    q = req_data.get('q')
    grade = req_data.get('grade')
    title = req_data.get('title', '')
    model_content = req_data.get('modelContent', '')
    is_need_synonyms = req_data.get('isNeedSynonyms', 'false')
    correct_version = req_data.get('correctVersion', 'basic')
    is_need_essay_report = req_data.get('isNeedEssayReport', 'false')

    if not q or not grade or not correct_version:
        return jsonify({'error': 'Missing required parameters: q, grade, correctVersion'}), 400

    # 调用有道接口
    result = create_request(q, grade, title, model_content, is_need_synonyms, correct_version, is_need_essay_report)

    # 假设返回的结果中包含以下字段（根据实际接口返回调整）：
    #  - totalScore, fullScore
    #  - majorScore 对象（包含 grammarScore, structureScore, emphasis, grammarAdvice, structureAdvice ）
    #  - essayAdvice
    #  - essayFeedback（sentsFeedback 数组，每项包含 rawSent 和 sentFeedback）
    #  - rawEssay （原文）
    #  - allFeatureScore（各项详细分数，可选）
    # 此处我们对返回结果做一次格式化，保证统一结构
    formatted_result = {
        "totalScore": result.get("Result", {}).get("totalScore", 0),
        "fullScore": result.get("Result", {}).get("fullScore", 100),
        "majorScore": result.get("Result", {}).get("majorScore", {}),
        "essayAdvice": result.get("Result", {}).get("essayAdvice", ""),
        "essayFeedback": result.get("Result", {}).get("essayFeedback", {"sentsFeedback": []}),
        "rawEssay": result.get("Result", {}).get("rawEssay", ""),
        "allFeatureScore": result.get("Result", {}).get("allFeatureScore", {})
    }

    return jsonify(formatted_result)

if __name__ == '__main__':
    app.run(port=5000, debug=True)