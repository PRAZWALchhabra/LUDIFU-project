import json,os,stripe
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from Gallery import *

# Folder Path
Gallery_Folder = "static/photos/"

STRIPE_PUBLISHABLE_KEY = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'  
STRIPE_SECRET_KEY = 'sk_test_BQokikJOvBiI2HlWgH4olfQ2'

stripe.api_key = STRIPE_SECRET_KEY

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

photos_obj = Photos()

# ----------------------------------------------
@app.route('/payment/<amount>', methods=['POST','GET'])
def payment_proceed(amount):  
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        amount=amount,
        currency='usd',
        customer=customer.id,
        description='A payment for the Hello World project'
    )

    return render_template('charge.html',amount=amount)

# ------------ Family Tree Route ----------------
@app.route('/tree')
def tree():
	return render_template("tree.html")
# -----------------------------------------------

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('galleries'))

# -------------- Gallery Routes ----------------
@app.route('/galleries')
def galleries():
	gallery_obj = Gallery()
	galleries = gallery_obj.get_all_gallery()
	return render_template("gallery.html", galleries=galleries)

@app.route('/galleries/add', methods=['POST'])
def add_galleries():
	if request.method == "POST":
		gallery_name = request.form['galleryName']
		gallery_obj = Gallery()
		result = gallery_obj.add_gallery(gallery_name)
		response = {'success':result}
		return json.dumps(response)

@app.route('/galleries/edit', methods=['POST'])
def edit_galleries():
    if request.method == "POST":
        new_name = request.form['newName']
        gallery_name = request.form['galleryName']
        gallery_obj = Gallery()
        result = gallery_obj.edit_gallery_name(gallery_name, new_name)
        response = {'success': result}
        return json.dumps(response)


@app.route('/galleries/delete', methods=['POST'])
def delete_galleries():
    if request.method == "POST":
        gallery_name = request.form['galleryName']
        gallery_obj = Gallery()
        result = gallery_obj.delete_gallery(gallery_name)
        response = {'success': result}
        return json.dumps(response)

# -------------- Gallery Routes ----------------


# -------------- Gallery Photos Routes ----------------
@app.route('/galleries/album/<gallery_name>', methods=['GET'])
def gallery(gallery_name):
	photos_obj = Photos()
	photos = photos_obj.get_all_gallery_photos(gallery_name)
	return render_template("photos.html", photos=photos, gallery_folder=Gallery_Folder,gallery_name=gallery_name)

@app.route('/galleries/album/photos/delete', methods=['POST'])
def delete_gallery_photo():
    if request.method == "POST":
        gallery_name = request.form['galleryName']
        photo_name = request.form['photoName']
        result = photos_obj.delete_gallery_photos(gallery_name, photo_name)
        response = {'success': result}
        return json.dumps(response)


@app.route('/galleries/album/<gallery_name>/upload', methods=['GET','POST'])
def upload_gallery_photo(gallery_name):
    app.config['UPLOAD_FOLDER'] = Gallery_Folder+gallery_name
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(url_for('gallery', gallery_name=gallery_name))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('gallery', gallery_name=gallery_name))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# -------------- Gallery Photos Routes ----------------


if __name__  == "__main__":
    app.run(debug=True)
