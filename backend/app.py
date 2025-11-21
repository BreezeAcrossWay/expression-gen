import os
import base64
import uuid
import io
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import requests
from PIL import Image
import zipfile

app = Flask(__name__)
CORS(app)

# 配置
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Stability AI API配置 (使用环境变量或默认值)
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY', 'your-api-key-here')
STABILITY_API_HOST = 'https://api.stability.ai'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_with_stability(prompt, init_image=None):
    """使用Stability AI生成图像"""
    try:
        # 这里使用本地图像生成模拟，实际项目中需要接入真实的AI API
        # 你可以使用Stability AI, Replicate, 或本地的Stable Diffusion
        
        # 创建一个简单的卡通风格图像（示例）
        img = Image.new('RGB', (512, 512), color=(255, 255, 255))
        return img
    except Exception as e:
        print(f"生成图像错误: {e}")
        return None

def generate_cartoon_variants(image_path):
    """基于上传的照片生成多个卡通形象"""
    variants = []
    
    # 加载原始图片
    original_img = Image.open(image_path)
    
    # 生成4个不同风格的卡通形象
    styles = [
        "可爱卡通风格",
        "Q版动漫风格", 
        "像素艺术风格",
        "简约线条风格"
    ]
    
    for i, style in enumerate(styles):
        variant_id = str(uuid.uuid4())
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'variant_{variant_id}.png')
        
        # 这里应该调用AI模型生成卡通形象
        # 目前使用缩放和处理作为演示
        img = original_img.copy()
        img = img.resize((400, 400), Image.Resampling.LANCZOS)
        img.save(output_path)
        
        variants.append({
            'id': variant_id,
            'style': style,
            'path': output_path,
            'url': f'/api/image/{variant_id}'
        })
    
    return variants

def generate_expression(base_image_path, expression, custom_prompt=None):
    """基于选定的卡通形象生成表情包"""
    expression_id = str(uuid.uuid4())
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'expr_{expression_id}.png')
    
    # 加载基础图像
    base_img = Image.open(base_image_path)
    
    # 这里应该调用AI模型生成表情
    # 目前使用原图作为演示
    result_img = base_img.copy()
    result_img.save(output_path)
    
    return {
        'id': expression_id,
        'expression': expression,
        'custom_prompt': custom_prompt,
        'path': output_path,
        'url': f'/api/image/{expression_id}'
    }

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'ok', 'message': '服务运行正常'})

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """上传明星照片"""
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # 生成卡通形象变体
        variants = generate_cartoon_variants(filepath)
        
        return jsonify({
            'success': True,
            'message': '上传成功',
            'original_image': unique_filename,
            'variants': variants
        })
    
    return jsonify({'error': '不支持的文件格式'}), 400

@app.route('/api/generate-expressions', methods=['POST'])
def generate_expressions():
    """基于选定的卡通形象生成表情包"""
    data = request.json
    variant_id = data.get('variant_id')
    expressions = data.get('expressions', ['开心', '难过', '思考'])
    
    variant_path = os.path.join(app.config['OUTPUT_FOLDER'], f'variant_{variant_id}.png')
    
    if not os.path.exists(variant_path):
        return jsonify({'error': '卡通形象不存在'}), 404
    
    results = []
    for expr in expressions:
        result = generate_expression(variant_path, expr)
        results.append(result)
    
    return jsonify({
        'success': True,
        'expressions': results
    })

@app.route('/api/generate-custom', methods=['POST'])
def generate_custom_expression():
    """根据自定义prompt生成表情包"""
    data = request.json
    variant_id = data.get('variant_id')
    custom_prompt = data.get('prompt', '')
    
    variant_path = os.path.join(app.config['OUTPUT_FOLDER'], f'variant_{variant_id}.png')
    
    if not os.path.exists(variant_path):
        return jsonify({'error': '卡通形象不存在'}), 404
    
    result = generate_expression(variant_path, 'custom', custom_prompt)
    
    return jsonify({
        'success': True,
        'expression': result
    })

@app.route('/api/image/<image_id>', methods=['GET'])
def get_image(image_id):
    """获取生成的图像"""
    # 尝试在不同路径查找图片
    paths = [
        os.path.join(app.config['OUTPUT_FOLDER'], f'variant_{image_id}.png'),
        os.path.join(app.config['OUTPUT_FOLDER'], f'expr_{image_id}.png'),
    ]
    
    for path in paths:
        if os.path.exists(path):
            return send_file(path, mimetype='image/png')
    
    return jsonify({'error': '图像不存在'}), 404

@app.route('/api/export-single/<expression_id>', methods=['GET'])
def export_single(expression_id):
    """导出单个表情包"""
    expr_path = os.path.join(app.config['OUTPUT_FOLDER'], f'expr_{expression_id}.png')
    
    if not os.path.exists(expr_path):
        return jsonify({'error': '表情包不存在'}), 404
    
    return send_file(expr_path, 
                     mimetype='image/png',
                     as_attachment=True,
                     download_name=f'expression_{expression_id}.png')

@app.route('/api/export-all', methods=['POST'])
def export_all():
    """一键导出所有表情包"""
    data = request.json
    expression_ids = data.get('expression_ids', [])
    
    if not expression_ids:
        return jsonify({'error': '没有要导出的表情包'}), 400
    
    # 创建ZIP文件
    zip_filename = f'expressions_{uuid.uuid4()}.zip'
    zip_path = os.path.join(app.config['OUTPUT_FOLDER'], zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for i, expr_id in enumerate(expression_ids):
            expr_path = os.path.join(app.config['OUTPUT_FOLDER'], f'expr_{expr_id}.png')
            if os.path.exists(expr_path):
                zipf.write(expr_path, f'expression_{i+1}.png')
    
    return send_file(zip_path,
                     mimetype='application/zip',
                     as_attachment=True,
                     download_name='all_expressions.zip')

@app.route('/api/delete-expression/<expression_id>', methods=['DELETE'])
def delete_expression(expression_id):
    """删除表情包"""
    expr_path = os.path.join(app.config['OUTPUT_FOLDER'], f'expr_{expression_id}.png')
    
    if os.path.exists(expr_path):
        os.remove(expr_path)
        return jsonify({'success': True, 'message': '删除成功'})
    
    return jsonify({'error': '表情包不存在'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
