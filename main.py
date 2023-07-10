from flask import *
from werkzeug.utils import secure_filename
import os
from colorthief import ColorThief
from random import randrange

top_colors = None

hex_list = []
filename = ""
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/images/"
app.secret_key = "secret key"

# def rgb_to_hex(rgb):
#     return '%02x%02x%02x' % rgb
# def give_colors(file_path):
#     hex_list.clear()
#     my_image = Image.open(file_path).convert('RGB')
#     image_array = np.array(my_image)
#     unique_colors = {}  # (r, g, b): count
#     for column in image_array:
#         for rgb in column:
#             t_rgb = tuple(rgb)
#             if t_rgb not in unique_colors:
#                 unique_colors[t_rgb] = 0
#             if t_rgb in unique_colors:
#                 unique_colors[t_rgb] += 1
#             print(unique_colors)
#     sorted_unique_colors = sorted(
#         unique_colors.items(), key=lambda x: x[1],
#         reverse=True)
#     converted_dict = dict(sorted_unique_colors)
#     values = list(converted_dict.keys())
#     top_10 = values[0:10]
#
#     for key in top_10:
#         hex = rgb_to_hex(key)
#         hex_list.append(f"#{hex}")

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
        full_path = f"static/images/{filename}"
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