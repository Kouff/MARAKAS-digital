import os
import csv
from flask import Flask, request, views, jsonify
from flask_sqlalchemy import SQLAlchemy

from exceptions import InvalidData

db_name = 'db.sqlite3'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.errorhandler(InvalidData)
def handle_invalid_data(error):
    """handler for invalid data"""
    return jsonify(error.to_dict()), error.status_code  # send the response with an error message


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(50))
    title = db.Column(db.String(250))

    def json(self, reviews=False):
        data = {
            'id': self.id,
            'asin': self.asin,
            'title': self.title
        }
        if reviews:
            data['reviews'] = [review.json() for review in self.reviews]
        return data


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    review = db.Column(db.String(250))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship(Product, backref=db.backref('reviews', lazy=True))

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'review': self.review,
        }


def init_db():
    def find_product(query, asin: str):
        for obj in query:
            if obj.asin == asin:
                return obj

    csv_path = "Products.csv"
    with open(csv_path, "r") as f_obj:  # open a file
        reader = csv.DictReader(f_obj)  # get data from the file
        for row in reader:
            product = Product(asin=row['Asin'], title=row['Title'])  # create a new product
            db.session.add(product)
    csv_path = "Reviews.csv"
    products = Product.query.all()  # get all the products
    with open(csv_path, "r") as f_obj:  # open a file
        reader = csv.DictReader(f_obj)  # get data from the file
        for row in reader:
            # create a new review
            review = Review(review=row['Review'], title=row['Title'], product=find_product(products, row['Asin']))
            db.session.add(review)
    db.session.commit()


class ProductListView(views.MethodView):
    """Retrieving all products"""

    def get(self):
        products = Product.query.all()  # get all the products
        return jsonify([product.json() for product in products])  # send the response with the products data


class ProductDetailView(views.MethodView):
    """Retrieving or updating a product"""

    def validate_data(self):
        data = request.form or request.json  # get data
        title = data.get('title')
        review = data.get('review')
        error_messages = {}
        if not title:  # if the title field is empty
            error_messages['title'] = 'This field may not be blank.'  # add an error message
        if not review:  # if the review field is empty
            error_messages['review'] = 'This field may not be blank.'  # add an error message
        if error_messages:  # if the error message is not empty
            raise InvalidData(error_messages)  # raise the exception if the error message is not empty
        return data  # return validated data

    def get(self, id):
        product = Product.query.get_or_404(id)  # get a product by id
        return jsonify(product.json(reviews=True))  # send the response with the product data

    def put(self, id):
        data = self.validate_data()  # get validated data
        product = Product.query.get_or_404(id)  # get a product by id
        # create a new review for the product
        review = Review(review=data['review'], title=data['title'], product=product)
        db.session.add(review)
        db.session.commit()
        return jsonify(product.json(reviews=True)), 201  # send the response with the product data


app.add_url_rule('/products/', view_func=ProductListView.as_view('products_list'))
app.add_url_rule('/products/<int:id>/', view_func=ProductDetailView.as_view('products_detail'))

if __name__ == "__main__":
    engine = db.get_engine()
    if not os.path.exists(db_name):  # if the db doesn`t exist
        db.create_all()  # create the db
        init_db()  # add data from .csv files to the db
    elif not engine.dialect.has_table(engine, 'Product'):  # if the db is empty
        init_db()  # add data from .csv files to the db
    app.run()  # run server
