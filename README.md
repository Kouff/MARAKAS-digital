Web framework: Flask.

The repository has branches:
* master (without docker and postgres, using sqlite3)
* with_docker_and_postgresql (this code but with docker and postgres)

Clone a project and move to it:

    $ git clone https://github.com/Kouff/MARAKAS-digital.git
    $ cd MARAKAS-digital
Create a [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html#via-pip) and [activate](https://virtualenv.pypa.io/en/latest/user_guide.html#activators) it or skip this point.

Install the requirements:
    
    $ pip install -r requirements.txt
Run server:

    $ python main.py
    
Urls: where **id** is "id" from products.
* GET http://127.0.0.1:8000/products/ - get all the products
* GET http://127.0.0.1:8000/products/{id}/ - get a product
* PUT http://127.0.0.1:8000/products/{id}/ - create a new review for a product (fields: "title" and "review")
