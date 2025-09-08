import sys

from flask import Flask, request, jsonify, Response
import uuid
import requests
import wave
import base64
import hashlib
import time
import os
import importlib
from flask_cors import CORS
from utils.AuthV3Util import addAuthParams

importlib.reload(sys)

# 配置信息（请填写您的应用ID和密钥）
APP_KEY = '08159463405d57c9'
APP_SECRET = '6NyH1FXHpa5InNG0bf6AM1pI4kDoIMV8'

# 有道API的URL
YOUDAO_VOICE_URL = 'https://openapi.youdao.com/iseapi'
YOUDAO_ASR_URL = 'https://openapi.youdao.com/asrapi'
YOUDAO_OCR_URL = 'https://openapi.youdao.com/ocrapi'
YOUDAO_CORRECT_URL = 'https://openapi.youdao.com/correct_writing_image'

app = Flask(__name__)
CORS(app)  # 允许所有来源的请求

#全局变量
translateText = ""
# 通用方法：生成签名
def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()

def do_request(url, data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(url, data=data, headers=headers)

# 语音翻译API调用
@app.route('/evaluate', methods=['POST'])
def evaluate():
    global translateText

    # 检查请求中是否包含音频文件
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    # 获取上传的音频文件
    audio_file = request.files['file']
    filename = str(uuid.uuid4()) + '.wav'
    filepath = os.path.join('C:/Users/86159/Desktop', filename)
    audio_file.save(filepath)

    # 获取音频文件信息
    with wave.open(filepath, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        nchannels = wav_file.getnchannels()

    with open(filepath, 'rb') as f:
        q = base64.b64encode(f.read()).decode('utf-8')

    # 1. 调用翻译功能
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data = {
        'appKey': APP_KEY,
        'q': q,
        'salt': salt,
        'sign': sign,
        'signType': 'v2',
        'langType': 'en',  # 根据您的需求设置语言类型
        'rate': sample_rate,
        'format': 'wav',
        'channel': nchannels,
        'type': 1,
        'curtime': curtime
    }

    # 向有道API发送请求进行翻译
    translate_response = do_request(YOUDAO_ASR_URL, data)
    translate_result = translate_response.json()

    # 删除临时音频文件
    os.remove(filepath)

    if translate_result.get('errorCode') != '0':
        # 翻译失败，返回错误信息
        return jsonify({'error': 'Translation failed', 'details': translate_result}), 500

    # 2. 获取翻译文本并设置全局变量 translateText
    translateText = translate_result.get('result', [])[0]
    print('Translation result:', translateText)

    # 3. 进行语音评估
    # 将翻译结果传递给语音评估函数
    audio_file.seek(0)  # 重置文件指针，以便后续的语音评估使用
    voice_eval_result = voice_evaluation(audio_file, 'en')

    # 返回语音评估结果给前端
    return jsonify({
        'translateText': translateText,
        'evaluation': voice_eval_result
    })

# 语音评测API调用
def voice_evaluation(audio_file, lang_type):
    # 获取文件扩展名
    filename = audio_file.filename
    extension = filename[filename.rindex('.') + 1:]

    if extension != 'wav':
        return {'error': '不支持的音频类型'}

    # 读取音频文件内容
    audio_file_content = audio_file.read()

    # 重置文件指针到开始位置
    audio_file.seek(0)

    # 使用 wave 库获取音频文件的相关信息
    wav_info = wave.open(audio_file.stream, 'rb')
    sample_rate = wav_info.getframerate()
    nchannels = wav_info.getnchannels()
    wav_info.close()

    # 将文件内容转换为 base64
    q = base64.b64encode(audio_file_content).decode('utf-8')

    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    print('1:', translateText)
    data = {
        'appKey': APP_KEY,
        'q': q,
        'text': translateText,
        'curtime': curtime,
        'salt': salt,
        'sign': sign,
        'signType': "v2",
        'langType': lang_type,
        'rate': sample_rate,
        'format': 'wav',
        'channel': nchannels,
        'type': 1
    }

    # 向有道 API 发出请求，进行语音评估
    response = do_request(YOUDAO_VOICE_URL, data)

    # 解析响应内容，提取音标及其得分
    evaluation_result = response.json()

    # 提取单词及音标和发音评分
    words_data = evaluation_result.get('words', [])

    processed_words = []
    for word in words_data:
        ipa = word.get('IPA', '')
        pronunciation = word.get('pronunciation', 0)

        # 获取每个音素（phoneme）的详细发音信息
        phonemes = []
        for phoneme in word.get('phonemes', []):
            phonemes.append({
                'phoneme': phoneme.get('phoneme', ''),
                'pronunciation': phoneme.get('pronunciation', 0)
            })

        # 将处理后的数据添加到返回列表
        processed_words.append({
            'word': word.get('word', ''),
            'ipa': ipa,
            'pronunciation': round(pronunciation, 2),
            'phonemes': phonemes
        })

    # 返回处理后的结果给前端
    return {
        'evaluation': processed_words,
        'overall': round(evaluation_result.get('overall', 0), 2),  # 保留两位小数的整体得分
        'speed': round(evaluation_result.get('speed', 0), 2),  # 保留两位小数的语速
        'accuracy': round(evaluation_result.get('pronunciation', 0), 2),  # 保留两位小数的发音准确度
        'fluency': round(evaluation_result.get('fluency', 0), 2),  # 保留两位小数的流利度
        'integrity': round(evaluation_result.get('integrity', 0), 2)  # 保留两位小数的完整度
    }

# 作文纠错API调用
def correct_writing(image_path, grade):
    with open(image_path, 'rb') as file_img:
        q = base64.b64encode(file_img.read()).decode('utf-8')

    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)

    data = {
        'appKey': APP_KEY,
        'q': q,
        'curtime': curtime,
        'salt': salt,
        'sign': sign,
        'signType': "v3",
        'grade': grade
    }

    response = do_request(YOUDAO_CORRECT_URL, data)
    return response.json()

# 图片识别API
def create_request(img_path):
    '''
    创建一个请求发送到有道OCR API。
    参数：
        img_path (str): 图片文件的路径。
    返回：
        有道OCR API的响应对象。
    '''
    # 请求参数
    lang_type = 'en'  # 设置语言类型（例如，'en'表示英文）
    detect_type = '10012'  # 根据文档设置识别类型
    angle = 'false'  # 如果需要360度识别，则设置为'true'
    column = 'false'  # 如果需要多列识别，则设置为'true'
    rotate = 'false'  # 如果需要获得文字旋转角度，则设置为'true'
    doc_type = 'json'
    image_type = '1'

    # 将图片数据编码为base64
    img = read_file_as_base64(img_path)
    data = {'img': img, 'langType': lang_type,
            'detectType': detect_type,
            'docType': doc_type, 'imageType': image_type}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = do_call('https://openapi.youdao.com/ocrapi', header, data, 'post')
    return res

def do_call(url, header, params, method):
    if method == 'get':
        return requests.get(url, params=params, headers=header)
    elif method == 'post':
        return requests.post(url, data=params, headers=header)

def read_file_as_base64(path):
    with open(path, 'rb') as f:
        data = f.read()
    return str(base64.b64encode(data), 'utf-8')

# 定义一个API端点用于处理文件上传
@app.route('/ocr_recognition', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # 将上传的文件保存到临时路径
        temp_path = os.path.join('temp', file.filename)
        os.makedirs('temp', exist_ok=True)
        file.save(temp_path)

        # 使用保存的图片调用OCR API
        response = create_request(temp_path)

        # 处理完成后删除临时文件
        os.remove(temp_path)

        # 返回OCR API的响应
        return jsonify(response.json()), response.status_code

    return jsonify({'error': 'Failed to process the image'}), 500

@app.route('/correct_writing', methods=['POST'])
def api_correct_writing():
    image_file = request.files['image_file']
    grade = request.form['grade']
    result = correct_writing(image_file, grade)
    return jsonify(result)


# 在 OcrDemo.py 中新增 TTS 接口
@app.route('/tts', methods=['POST'])
def tts():
    # 从请求中提取文本
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': '缺少文本参数'}), 400
    text = data['text']

    # 设置 TTS 请求参数（这里使用默认的发音人，可根据需求修改）
    params = {
        'q': text,
        'voiceName': 'youxiaomei',  # 默认发音人（例如：xiaoyan、xiaomei等）
        'format': 'mp3'
    }

    # 添加鉴权参数（使用 OcrDemo.py 中已定义的 APP_KEY 和 APP_SECRET）
    addAuthParams(APP_KEY, APP_SECRET, params)

    # 设置请求头
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # 请求有道 TTS 接口
    tts_response = requests.post('https://openapi.youdao.com/ttsapi', data=params, headers=headers)

    # 如果返回音频数据，则直接返回二进制内容
    if 'audio' in tts_response.headers.get('Content-Type', ''):
        return Response(tts_response.content, mimetype=tts_response.headers.get('Content-Type', 'audio/mp3'))
    else:
        return jsonify({'error': 'TTS 合成失败', 'details': tts_response.text}), 500


if __name__ == '__main__':
    app.run(port=5010)