from flask import Flask, request, jsonify, send_file, render_template
from pydub import AudioSegment
import os
import uuid
import logging
import subprocess
import tempfile
import shutil
from werkzeug.utils import secure_filename
from config import Config
from flask import Flask, render_template

# 初始化Flask应用
app = Flask(__name__)
app.config.from_object(Config)
counter_file = 'visit_count.txt' # 初始化计数器

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 检查FFmpeg是否安装
try:
    subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except (subprocess.CalledProcessError, FileNotFoundError) as e:
    logger.error("FFmpeg未安装或未添加到系统PATH！")
    raise RuntimeError(
        "系统必须安装FFmpeg。安装方法：\n"
        "Ubuntu/Debian: sudo apt install ffmpeg\n"
        "CentOS: sudo yum install epel-release && sudo yum install ffmpeg ffmpeg-devel\n"
        "Windows: 从 https://ffmpeg.org/download.html 下载并配置环境变量"
    )

# 确保目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def get_counter():
    if not os.path.exists(counter_file):
        with open(counter_file, 'w') as f:
            f.write('0')
        return 0
    with open(counter_file, 'r') as f:
        return int(f.read())
def increment_counter():
    count = get_counter() + 1
    with open(counter_file, 'w') as f:
        f.write(str(count))
    return count
@app.route('/')
def index():
    return render_template('index.html', visitor_count=increment_counter())
    
    # 最后返回渲染结果
    return render_template('index.html', visitor_count=visitor_count)


@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('static', filename)
    
    
@app.route('/convert', methods=['POST'])
def convert_audio():
    upload_path = None
    try:
        # 验证文件上传
        if 'file' not in request.files:
            return jsonify({'error': '未选择文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '空文件名'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式'}), 400

        # 生成唯一ID和安全文件名
        file_id = str(uuid.uuid4())
        orig_ext = secure_filename(file.filename).rsplit('.', 1)[-1]
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.{orig_ext}")
        file.save(upload_path)

        # 获取转换参数
        target_format = request.form.get('format', 'mp3').lower()
        speed = float(request.form.get('speed', 1.0))

        # 加载音频文件
        audio = AudioSegment.from_file(upload_path, format=orig_ext)

        # 处理播放速度调整
        if speed != 1.0:
            new_frame_rate = int(audio.frame_rate * speed)
            audio = audio._spawn(audio.raw_data, overrides={
                'frame_rate': new_frame_rate
            })
            audio = audio.set_frame_rate(audio.frame_rate)

        # 定义编解码器参数
        codec_config = {
            'mp3': {'format': 'mp3', 'codec': 'libmp3lame', 'bitrate': '192k'},
            'wav': {'format': 'wav', 'codec': 'pcm_s16le'},
            'flac': {'format': 'flac', 'codec': 'flac'},
            'ogg': {'format': 'ogg', 'codec': 'libvorbis'}
        }

        if target_format not in codec_config:
            return jsonify({'error': '不支持的目标格式'}), 400

        # 导出转换后的文件
        output_filename = f"{file_id}.{target_format}"
        output_path = os.path.join(app.config['CONVERTED_FOLDER'], output_filename)
        audio.export(output_path, **codec_config[target_format])

        return jsonify({
            'download_url': f'/download/{output_filename}'
        })

    except Exception as e:
        logger.error(f"转换失败: {str(e)}", exc_info=True)
        return jsonify({'error': '音频处理失败，请检查文件格式是否符合要求'}), 500
    finally:
        # 清理临时文件
        if upload_path and os.path.exists(upload_path):
            os.remove(upload_path)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['CONVERTED_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except FileNotFoundError:
        return jsonify({'error': '文件不存在或已过期'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
