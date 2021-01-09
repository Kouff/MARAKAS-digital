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
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


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
    with open(csv_path, "r") as f_obj:
        reader = csv.DictReader(f_obj)
        for row in reader:
            product = Product(asin=row['Asin'], title=row['Title'])
            db.session.add(product)
    csv_path = "Reviews.csv"
    products = Product.query.all()
    with open(csv_path, "r") as f_obj:
        reader = csv.DictReader(f_obj)
        for row in reader:
            review = Review(review=row['Review'], title=row['Title'], product=find_product(products, row['Asin']))
            db.session.add(review)
    db.session.commit()


class ProductView(views.MethodView):

    def get(self, id):
        return str(id)

    def put(self, id):
        return str(id)


app.add_url_rule('/<int:id>/', view_func=ProductView.as_view('products'))

if __name__ == "__main__":
    engine = db.get_engine()
    if not os.path.exists(db_name):
        db.create_all()
        init_db()
    elif not engine.dialect.has_table(engine, 'Product'):
        init_db()
    app.run(debug=True)
