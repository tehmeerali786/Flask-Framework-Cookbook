import os
from decimal import Decimal
import redis
import json 
from functools import wraps
from werkzeug.utils import secure_filename
from flask import request, jsonify, Blueprint, render_template, flash, redirect, url_for, abort
from flask.views import MethodView
from flask_restful import Resource, reqparse
from my_app import db, app, api, ALLOWED_EXTENSIONS
from my_app.catalog.models import Product, Category, ProductForm, CategoryForm
# from my_app import redis
from sqlalchemy.orm import join

catalog = Blueprint('catalog', __name__)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('price', type=float)
parser.add_argument('category', type=dict)
parser.add_argument('image_path', type=str)


def template_or_json(template=None):
    '''Return a dict from your view and this will either
        pass it to a template or render json. Use like:
        
        @template_or_json('template.html')
    '''
    def decorated(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ctx = f(*args, **kwargs)
            if request.headers.get("X-Requested-Width") == "XMLHttpRequest" or not template:
                return jsonify(ctx)
            else:
                return render_template(template, **ctx)
        
        return decorated_function
    return decorated

def allowed_file(filename):
    return '.' in filename and filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@catalog.route('/')
@catalog.route('/home')
@template_or_json('home.html')
def home():
    
    products = Product.query.all()
    
    # if request.headers.get("X-Requested-With") ==\
    #     "XMLHttpRequest":
    #         products = Product.query.all()
    #         return jsonify({
    #             'count': len(products)
    #         })
    
    return {'count': len(products)}

@catalog.route('/product/<id>')
def product(id):
    # product = Product.objects.get_or_404(key=key)
    product = Product.query.get_or_404(id)
    # product_key = 'product-%s' % product.id
    # redis.set(product_key, product.name)
    # redis.expire(product_key, 600)
    return render_template('product.html', product=product)

@catalog.route('/products')
@catalog.route('/products/<int:page>')
def products(page=1):
    products = Product.query.paginate(page=page, per_page=10)
    # res = {}
    # for product in products:
    #     res [product.id] ={
    #         'name' : product.name,
    #         'price' :str(product.price),
    #         'category': product.category.name,
    #     }
    # return jsonify(res)
    return render_template('products.html', products=products)


@catalog.route('/product-create', methods=['GET', 'POST'])
def create_product():
    
    form = ProductForm()
    # categories =[(c.id, c.name) for c in Category.query.all()]
    # form.category.choices = categories
    if form.validate_on_submit():
        
        name = form.name.data
        price = form.price.data
        category = Category.query.get_or_404( form.category.data )
        image = form.image.data
        if allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        
        product = Product(name, price, category, filename)
        # product.save()
        db.session.add(product)
        db.session.commit()
        flash('This product %s has been created' % name, 'success')
        return redirect(url_for('catalog.product', id=product.id))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('product-create.html', form=form)

@catalog.route('/product-search')
@catalog.route('/product-search/<int:page>')
def product_search(page=1):
    name = request.args.get('name')
    price = request.args.get('price')
    category = request.args.get('category')
    products = Product.query
    if name:
        products = products.filter(Product.name.like('%' + name + '%'))
    if price:
        products = products.filter(Product.price == price)
    if category:
        products = products.select_from(join(Product, Category)).filter(
            Category.name.like('%' + category + '%')
        )
        
    return render_template(
        
        'products.html', products=products.paginate(page=page, per_page=10)
                           
                           )


@catalog.route('/create-category', methods=['GET', 'POST'])
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name)
        db.session.add(category)
        db.session.commit()
        flash(
            'The category %s has been created successfully.' % name, 'success'
        )
        return redirect( url_for('catelog.category', id=category.id) )
    
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('category-create.html', category=category)

@catalog.route('/category/<id>')
def category(id):
    category = Category.query.get_or_404(id)
    return render_template('category.html', category=category)
@catalog.route('/categories')
def categories():
    categories = Category.query.all()
    # res = {}
    # for category in categories:
    #     res[category.id] = {
    #         'name' : category.name
    #     }
    #     for product in category.products:
    #         res[category.id]['products'] = {
                
    #             'id' : product.id,
    #             'name' : product.name, 
    #             'price' : product.price
    #         }
            
    # return jsonify(res)
    return render_template('categories.html', categories=categories)

@catalog.route('/recent-products')
def recent_products():
    keys_live = redis.keys('product-*')
    products = [redis.get(k).decode('utf-8') for k in keys_live]
    return jsonify({ 'products': products})


# class ProductView(MethodView):
#     def get(self, id=None, page=1):
#         if not id:
#             products = Product.query.paginate(page, 10).items 
#             res = {}
#             for product in products:
#                 res[product.id] = {
#                     'name': product.name,
#                     'price': product.price,
#                     'category': product.category.name
#                 }
                
#         else:
#             product = Product.query.filter_by(id=id).first()
#             if not product:
#                 abort(404)
#                 res = json.dumps({
#                     'name': product.name,
#                     'price': product.price,
#                     'category': product.category.name
#                 })
                
#         return res
    
#     def post(self):
#         # Create a new product.
#         # Return the ID/object of the newly created product.
#         pass
        
#     def put(self, id):
#         # Update the product corresponding provided id
#         # Return the JSON corresponding updated product.
#         pass 
    
#     def delete(self, id):
#         # Delete the product corresponding provided id
#         # Return success or error message.
#         pass 
    
# product_view = ProductView.as_view('product_view')
# app.add_url_rule('/products/', view_func=product_view, methods=['GET', 'POST'])
# app.add_url_rule('/products/<int:id>', view_func=product_view, methods=['GET', 'PUT', 'DELETE'])

class ProductApi(Resource):
    def get(self, id=None, page=1):
        if not id:
            products = Product.query.paginate(page=page, per_page=10).items
        else:
            products = [Product.query.get(id)]
        if not products:
            abort(404)
        res = {}
        for product in products:
            res[product.id] = {
                'name' : product.name,
                'price' : product.price,
                'category' : product.category.name
            }
        return json.dumps(res)
    
    def post(self):
        args = parser.parse_args()
        name = args['name']
        price = args['price']
        categ_name = args['category']['name']
        category = Category.query.filter_by(name=categ_name).first()
        if not category:
            category = Category(categ_name)
        image_path = args['image_path']
        product = Product(name, price, category, image_path)
        db.session.add(product)
        db.session.commit()
        res = {}
        res[product.id] = {
            'name' : product.name,
            'price' : product.price,
            'category' : product.category.name,
            'image_path': product.image_path
        }
        return json.dumps(res)
    
    def put(self, id):
        args = parser.parse_args()
        name = args['name']
        price = args['price']
        categ_name = args['category']['name']
        category = Category.query.filter_by(name=categ_name).first()
        Product.query.filter_by(id=id).update({
            'name' : name,
            'price' : price,
            'category' : category.id,
        })
        db.session.commit()
        product = Product.query.get_or_404(id)
        res = {}
        res[product.id] = {
            'name' : product.name,
            'price' : product.price,
            'category' : product.category.name,
            'image_path': product.image_path
        }
        return json.dumps(res)
    
    def delete(self, id):
        product = Product.query.filter_by(id=id)
        product.delete()
        db.session.commit()
        return json.dumps({'response' : 'success'})
    
api.add_resource(
    ProductApi,
    '/api/product',
    '/api/product/<int:id>',
    '/api/product/<int:id>/<int:page>'
)

