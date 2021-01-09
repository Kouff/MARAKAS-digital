Clone a project and move to it:

    $ git clone https://github.com/Kouff/MARAKAS-digital.git
    $ cd MARAKAS-digital
    $ git checkout with_docker_and_postgresql
Build and run docker container:

    $ docker-compose up -d --build
    
Urls: where **id** is "id" from products.
* GET http://127.0.0.1:8000/products/ - get all the products
* GET http://127.0.0.1:8000/products/{id}/ - get a product
* PUT http://127.0.0.1:8000/products/{id}/ - create a new review for a product (fields: "title" and "review")

Stop docker container:

    $ docker-compose down
