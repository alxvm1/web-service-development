import os
from flask import Flask, render_template, request
from PIL import Image, ImageDraw
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

def create_color_histogram(image, filename):
    arr = np.array(image)
    plt.figure(figsize=(6, 4))
    plt.hist(arr[..., 0].ravel(), bins=256, color='red', alpha=0.5, label='Red')
    plt.hist(arr[..., 1].ravel(), bins=256, color='green', alpha=0.5, label='Green')
    plt.hist(arr[..., 2].ravel(), bins=256, color='blue', alpha=0.5, label='Blue')
    plt.legend()
    plt.title('Color Distribution Histogram')
    plt.xlabel('Intensity')
    plt.ylabel('Pixel Count')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    cell_percent = int(request.form['cell_size'])
    filename = os.path.join(UPLOAD_FOLDER, 'original.png')
    file.save(filename)

    img = Image.open(filename).convert('RGB')
    width, height = img.size
    cell_px = int(width * cell_percent / 100)

    img_chess = img.copy()
    draw = ImageDraw.Draw(img_chess)
    for y in range(0, height, cell_px):
        for x in range(0, width, cell_px):
            if ((x // cell_px) + (y // cell_px)) % 2 == 0:
                draw.rectangle(
                    [x, y, min(x + cell_px, width), min(y + cell_px, height)],
                    fill=(200, 200, 200),
                    outline=None
                )
    chess_filename = os.path.join(UPLOAD_FOLDER, 'chess.png')
    img_chess.save(chess_filename)

    # Color histogram
    hist_orig = os.path.join(UPLOAD_FOLDER, 'hist_original.png')
    create_color_histogram(img, hist_orig)
    hist_chess = os.path.join(UPLOAD_FOLDER, 'hist_chess.png')
    create_color_histogram(img_chess, hist_chess)

    return render_template('results.html',
        orig_img='/static/original.png',
        hist_orig='/static/hist_original.png',
        chess_img='/static/chess.png',
        hist_chess='/static/hist_chess.png'
    )

if __name__ == '__main__':
    app.run(debug=True)
