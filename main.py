from flask import *
from werkzeug.utils import secure_filename
import os
from colorthief import ColorThief
from random import randrange

top_colors = None

hex_list = []
filename = ""
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/"


@app.route('/')
def home():
    global top_colors
    return render_template('index.html', colors=hex_list, path=filename)


@app.route('/upload', methods=['POST', 'GET'])
def upload():

    global top_colors, hex_list

    def rgb_to_hex(rgb):
        return '%02x%02x%02x' % rgb

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        full_path = f"static/{filename}"
        colors = ColorThief(full_path)
        top_colors = colors.get_palette(color_count=10)
        hex_list = []
        for i in top_colors:

            hex_list.append('#'+rgb_to_hex(i))

        return redirect(url_for('home'))


@app.route('/random', methods=['GET', 'POST'])
def random():
    global hex_list

    def rgb_to_hex(rgb):
        return '%02x%02x%02x' % rgb

    hex_list=[]
    for i in range(10):
        R = randrange(0, 256)
        G = randrange(0, 256)
        B = randrange(0, 256)
        color = (R, G, B)
        hex_list.append('#'+rgb_to_hex(color))
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)