from flask import Flask, request, jsonify
import base64
from io import BytesIO
import sys
import json
import os

app = Flask(__name__)

# Import the function from the Python script
sys.path.append('<path_to_directory_containing_script>')
from simple_extractor import main

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@app.route('/run_extractor', methods=['POST'])
def run_extractor():
    try:
        # Lấy dữ liệu từ request
        data = request.json

        # Decode base64 image và lưu vào BytesIO object
        image_data = base64.b64decode(data['image'])
        image_buffer = BytesIO(image_data)

        # Lưu ảnh vào một file tạm thời
        temp_image_path = 'temp_image.png'
        with open(temp_image_path, 'wb') as temp_image_file:
            temp_image_file.write(image_buffer.getvalue())

        # Chuẩn bị các đối số cho hàm main
        args = {
            'dataset': data.get('dataset', 'lip'),
            'model-restore': data.get('model_restore', ''),
            'gpu': data.get('gpu', '0'),
            'input-dir': '',
            'output-dir': '',
            'logits': data.get('logits', False)
        }

        # Thực thi hàm main với các đối số
        main(args)

        # Đọc và encode file kết quả thành base64
        output_image_base64 = image_to_base64(temp_image_path)

        # Xóa ảnh tạm sau khi hoàn thành
        os.remove(temp_image_path)

        return jsonify({'image': output_image_base64}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
