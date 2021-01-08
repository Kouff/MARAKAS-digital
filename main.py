from flask import Flask, request, views
from flask_sqlalchemy import SQLAlchemy

db_name = 'db.sqlite3'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(50))
    title = db.Column(db.String(250))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    review = db.Column(db.String(250))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship(Product, backref=db.backref('reviews', lazy=True))


class ProductView(views.MethodView):

    def get(self, id):
        return str(id)

    def put(self, id):
        return str(id)


app.add_url_rule('/<int:id>/', view_func=ProductView.as_view('products'))


if __name__ == "__main__":
    app.run(debug=True)
