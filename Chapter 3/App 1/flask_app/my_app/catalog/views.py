from decimal import Decimal
from flask import request, jsonify, Blueprint
from my_app import db 
# from my_app import redis
from my_app.catalog.models import Product
# ,Category 
catalog = Blueprint('catalog', __name__)

@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome to the Catalog Home."

@catalog.route('/product/<key>')

def product(key):
    product = Product.objects.get_or_404(key=key)
    # product = Product.query.get_or_404(id)
    # product_key = 'product-%s' % product.id
    # redis.set(product_key, product.name)
    # redis.expire(product_key, 600)
    return 'Product - %s, %s' % (product.name, product.price)

@catalog.route('/products')
def products():
    products = Product.objects.all()
    res = {}
    for product in products:
        res [product.key] ={
            'name' : product.name,
            'price' :str(product.price),
            # 'category': product.category.name,
        }
    return jsonify(res)


@catalog.route('/product-create', methods=['POST',])
def create_product():
    name = request.form.get('name')
    key = request.form.get('key')
    price = request.form.get('price')
    # categ_name = request.form.get('category')
    # category = Category.query.filter_by(name=categ_name).first()
    # if not category:
    #     category = Category(categ_name)
    product = Product(
        name=name,
        key=key,
        price=Decimal(price)
        )
    product.save()
    # db.session.add(product)
    # db.session.commit()
    return 'Product Created.'

# @catalog.route('/create-category', methods=['POST',])
# def create_category():
#     name = request.form.get('name')
#     category = Category(name)
#     db.session.add(category)
#     db.session.commit()
#     return 'Category created.'

# @catalog.route('/categories')
# def categories():
#     categories = Category.query.all()
#     res = {}
#     for category in categories:
#         res[category.id] = {
#             'name' : category.name
#         }
#         for product in category.products:
#             res[category.id]['products'] = {
                
#                 'id' : product.id,
#                 'name' : product.name, 
#                 'price' : product.price
#             }
            
#     return jsonify(res)

# @catalog.route('/recent-products')
# def recent_products():
#     keys_live = redis.keys('product-*')
#     products = [redis.get(k).decode('utf-8') for k in keys_live]
#     return jsonify({ 'products': products})