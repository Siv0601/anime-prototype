from flask import Flask, request, send_file
from PIL import Image
import base64
import io

app = Flask(__name__)

@app.route('/generate_gif', methods=['POST'])
def generate_gif():
    data = request.json.get('frames', [])
    if not data:
        return "No frames received", 400

    images = []
    for frame in data:
        img_data = base64.b64decode(frame.split(',')[1])  # Remove data URL prefix
        image = Image.open(io.BytesIO(img_data))
        images.append(image)

    gif_path = "animation.gif"
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=500, loop=0)

    return send_file(gif_path, mimetype='image/gif', as_attachment=True, download_name='animation.gif')

if __name__ == '__main__':
    app.run(debug=True,port=5001)
