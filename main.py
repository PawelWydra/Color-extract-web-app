from flask import Flask, render_template, send_from_directory, url_for
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField



app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfdsdsfdsf'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
Bootstrap(app)


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only photos are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField("Upload")


@app.route("/uploads/<filename>")
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route("/", methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
        from chart import exact_color
        exact_color(filename)
    else:
        file_url = None
    return render_template("index.html", form=form, file_url=file_url)


# @app.route('/plot.png')
# def plot_png():
#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')
#
#
# def create_figure():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     xs = range(100)
#     ys = [random.randint(1, 50) for x in xs]
#     axis.plot(xs, ys)
#     return fig



if __name__ == '__main__':
    app.run(debug=True)