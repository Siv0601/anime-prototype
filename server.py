from flask import Flask, request, send_file, send_from_directory, jsonify
from PIL import Image
import os
import base64
import io

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_GIF = "output.gif"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 't1.html')

@app.route('/save', methods=['POST'])
def save_gif():
    data = request.get_json()
    images_data = data.get('images', [])

    if not images_data:
        return jsonify({"error": "No images received"}), 400

    image_list = []

    for index, img_data in enumerate(images_data):
        try:
            # Convert base64 string to image
            img_data = img_data.split(",")[1]  # Remove data URL prefix
            img_bytes = base64.b64decode(img_data)
            img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")

            image_list.append(img)
        except Exception as e:
            return jsonify({"error": f"Failed to process image {index}: {str(e)}"}), 400

    if not image_list:
        return jsonify({"error": "No valid images to create GIF"}), 400

    # Save images as GIF
    output_path = os.path.join(UPLOAD_FOLDER, OUTPUT_GIF)
    image_list[0].save(output_path, save_all=True, append_images=image_list[1:], duration=100, loop=0)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
