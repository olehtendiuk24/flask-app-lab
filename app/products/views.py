import os
import uuid
from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort, request
from werkzeug.utils import secure_filename
from tinydb import TinyDB, Query
from . import products_bp
from .forms import ProductForm

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = TinyDB(os.path.join(DATA_DIR, 'products.json'), indent=4, ensure_ascii=False)
products_table = db.table('products')
ProductQuery = Query()

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 МБ


def save_product_image(file_storage):

    if not file_storage or not file_storage.filename:
        return None

    file_storage.seek(0, os.SEEK_END)
    file_length = file_storage.tell()
    file_storage.seek(0)
    if file_length > MAX_FILE_SIZE:
        raise ValueError("Розмір файлу перевищує максимально дозволені 2 МБ.")

    original_name = secure_filename(file_storage.filename)
    ext = os.path.splitext(original_name)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file_storage.save(file_path)

    return f"uploads/{unique_filename}"


@products_bp.route('/')
def list_products():
    all_products = products_table.all()
    return render_template('products/products.html', products=all_products, title='Каталог товарів')


@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        try:
            image_rel_path = save_product_image(form.image.data)
        except ValueError as e:
            flash(str(e), "danger")
            return render_template('products/product_form.html', form=form, title='Додати товар', is_edit=False)

        all_items = products_table.all()
        new_id = max([item.get('id', 0) for item in all_items], default=0) + 1

        new_product = {
            "id": new_id,
            "name": form.name.data,
            "content": form.content.data,
            "price": round(float(form.price.data), 2),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_rel_path,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        products_table.insert(new_product)
        flash(f"Товар '{new_product['name']}' успішно додано!", "success")
        return redirect(url_for('products.list_products'))

    return render_template('products/product_form.html', form=form, title='Додати товар', is_edit=False)


@products_bp.route('/<int:id>')
def detail_product(id):
    product = products_table.get(ProductQuery.id == id)
    if not product:
        abort(404)
    return render_template('products/detail_product.html', product=product, title=product['name'])


@products_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    product = products_table.get(ProductQuery.id == id)
    if not product:
        abort(404)

    form = ProductForm()

    if form.validate_on_submit():
        image_rel_path = product.get('image')
        if form.image.data and form.image.data.filename:
            try:
                new_img = save_product_image(form.image.data)
                if new_img:

                    if image_rel_path:
                        old_path = os.path.join(BASE_DIR, 'static', image_rel_path)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    image_rel_path = new_img
            except ValueError as e:
                flash(str(e), "danger")
                return render_template('products/product_form.html', form=form, product=product, title='Редагувати товар', is_edit=True)

        updated_data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": round(float(form.price.data), 2),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_rel_path
        }

        products_table.update(updated_data, ProductQuery.id == id)
        flash(f"Товар '{form.name.data}' успішно оновлено!", "success")
        return redirect(url_for('products.detail_product', id=id))

    elif request.method == 'GET':
        form.name.data = product['name']
        form.content.data = product['content']
        form.price.data = product['price']
        form.category.data = product['category']
        form.quantity.data = product['quantity']

    return render_template('products/product_form.html', form=form, product=product, title='Редагувати товар', is_edit=True)


@products_bp.route('/<int:id>/delete', methods=['POST'])
def delete_product(id):
    product = products_table.get(ProductQuery.id == id)
    if not product:
        abort(404)

    if product.get('image'):
        img_path = os.path.join(BASE_DIR, 'static', product['image'])
        if os.path.exists(img_path):
            os.remove(img_path)

    products_table.remove(ProductQuery.id == id)
    flash(f"Товар '{product['name']}' було видалено.", "info")
    return redirect(url_for('products.list_products'))