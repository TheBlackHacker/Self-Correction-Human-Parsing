from flask import Flask, request, jsonify
import base64
from io import BytesIO
import sys
import json
import os
import shutil
import uuid

app = Flask(__name__)

# Import the function from the Python script
#sys.path.append('<path_to_directory_containing_script>')
from simple_extractor import main

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@app.route('/run_extractor', methods=['POST'])
def run_extractor():
    try:
        data = request.json

        image_data = base64.b64decode(data['image'])
        image_buffer = BytesIO(image_data)

        temp_dir = 'temp/'+str(uuid.uuid4())[:12]
        os.makedirs(temp_dir)

        temp_image_path = os.path.join(temp_dir, 'temp_image.png')
        with open(temp_image_path, 'wb') as temp_image_file:
            temp_image_file.write(image_buffer.getvalue())

        args = {
            'dataset': data.get('dataset', 'lip'),
            'model_restore': data.get('model_restore', 'checkpoints/final.pth'),
            'gpu': data.get('gpu', '0'),
            'input_dir': temp_dir,
            'output_dir': temp_dir,
            'logits': data.get('logits', False)
        }

        main(args)

        output_image_base64 = image_to_base64(temp_image_path)

        shutil.rmtree(temp_dir)

        return jsonify({'image': output_image_base64}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
