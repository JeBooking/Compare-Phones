from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
import os
from photo_analyzer import analyze_photo_from_stream
from config import config

app = Flask(__name__)

# 加载配置
config_name = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[config_name])

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # 直接从内存中分析文件，不保存到磁盘
            result = analyze_photo_from_stream(file)
            return jsonify(result)

        except Exception as e:
            return jsonify({'error': f'处理文件时出错: {str(e)}'}), 500
    
    return jsonify({'error': '不支持的文件格式'}), 400

@app.route('/analyze', methods=['POST'])
def analyze():
    """分析照片的API端点"""
    return upload_file()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'],
            host=app.config['HOST'],
            port=app.config['PORT'])


