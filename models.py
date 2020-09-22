import json
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

# to consult database schema: https://dbdesigner.page.link/xvnBfzE4JMMCnLmx5

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)       
    phone = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    user_ratings = db.relationship("ProductRating", backref="user", lazy=True)
    orders = db.relationship("Order", backref="user", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,                                    
            "phone": self.phone,
            "address": self.address
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit() 

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    presentation = db.Column(db.String(500), nullable=False)
    attributes = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(255), default="base_placeholder-Cecilia-Lorenzo-Inaki.jpg")
    ratings = db.relationship("ProductRating", backref="product", lazy=True)
    categories = db.relationship('Category', secondary="product_categories", lazy=True)
    orders = db.relationship('OrderDetail', backref="product", lazy=True)

    def serialize(self):        
        return{
            "id": self.id,
            "sku": self.sku,
            "brand": self.brand,
            "name": self.name,
            "presentation": json.loads(self.presentation),
            "attributes": json.loads(self.attributes),
            "description": self.description,
            "image": self.image
        }
    
    def serialize_w_categories(self):
        categories = list(map(lambda category: category.serialize(), self.categories))        
        return{
            "id": self.id,
            "sku": self.sku,
            "brand": self.brand,
            "name": self.name,
            "categories": categories,
            "presentation": json.loads(self.presentation),
            "attributes": json.loads(self.attributes),
            "description": self.description,
            "image": self.image
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# please register products sending info this way:
# {
#     "attributes": {
#       "acidity": "6",
#       "origin": "Colombia",
#       "roasting": "95 AGS",
#       "species": "Arabica",
#       "type": "Molido"
#     },
#     "brand": "4Geeks Coffee",
#     "description": "Lorem ipsum dolor sit amen.",
#     "image": "base_placeholder-Cecilia-Lorenzo-Inaki.jpg",
#     "name": "Console.log(Coffee)",
#     "presentation": [
#       {
#         "format": "100gr",
#         "stock": 22,
#         "price": "3590"
#       },
#       {
#         "format": "210gr",
#         "stock": 10,
#         "price": "6500"
#       },
#       {
#         "format": "370gr",
#         "stock": 19,
#         "price": "12000"
#       }
#     ],
#     "sku": "4gB-FP-4Geeks-ftVII",
#     "categories": [1,3]
#   }

# class Content(db.Model):
#     __tablename__ = 'contents'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     cover = db.Column(db.String(255), nullable=False)
#     images = db.Column(db.String(255), nullable=False)
#     resume = db.Column(db.String(280), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     # please organize large text areas as:
#     # {
#         # "paragraph_1": "lorem ipsum...",
#         # "paragraph_2": "lorem ipsum...",
#         # ...
#     # }   
#     # content_ratings = db.relationship("content_ratings", backref="contents")

#     def serialize(self):
#         return{
#             "id": self.id,
#             "name": self.name,
#             "cover": self.cover,
#             "images": self.images,
#             "resume": self.resume,
#             "body": self.body
#         }
    
#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

class ProductRating(db.Model):
    __tablename__ = 'product_ratings'
    id = db.Column(db.Integer, primary_key=True)     
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(280), nullable=True)
    date = db.Column(db.Date, nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "stars": self.stars,
            "comment": self.comment,
            "date": self.date
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# class ContentRating(db.Model):
#     __tablename__ = 'content_ratings'
#     id = db.Column(db.Integer, primary_key=True)
#     # content_id =  db.Column(db.Integer, db.ForeignKey('contents.id'), nullable=False)
#     # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     likes = db.Column(db.Integer, nullable=False)
#     comment = db.Column(db.String(280), nullable=True)
#     date = db.Column(db.Date, nullable=False)

#     def serialize(self):
#         return{
#             "id": self.id,
#             "username": self.user.full_name,
#             "likes": self.likes,
#             "comment": self.comment,
#             "date": self.date
#         }
    
#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit() 

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)     
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    shipping_address = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    order_detail = db.relationship("OrderDetail",  backref="order", lazy=True)  

    def serialize(self):
        return{
            "id": self.id,
            "shipping_address": self.shipping_address,
            "full_name": self.full_name,
            "status": self.status,
            "purchase_date": self.purchase_date
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    event_id =  db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    order_id =  db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    total_price = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.String(120), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "total_price": self.price,
            "quantity": self.quantity
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()  


class ProductCategory(db.Model):
    __tablename__ = "product_categories"
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    products = db.relationship('Product', secondary="product_categories", lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    cover = db.Column(db.String(255), nullable=False)
    images = db.Column(db.String(255), nullable=False)
    resume = db.Column(db.String(280), nullable=False)
    body = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('OrderDetail',  backref="event", lazy=True)

    def serialize(self):
        return{
            "id": self.id,
            "event_type": self.event_type,
            "date": self.date,
            "name": self.name,
            "category": self.category,
            "cover": self.cover,
            "images": self.images,
            "resume": self.resume,
            "body": self.resume,
            "price": self.price,
            "sku": self.sku
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



# such database. much model. wow

#          ▄              ▄    
#         ▌▒█           ▄▀▒▌   
#         ▌▒▒█        ▄▀▒▒▒▐   
#        ▐▄█▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐   
#      ▄▄▀▒▒▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐   
#    ▄▀▒▒▒░░░▒▒▒░░░▒▒▒▀██▀▒▌   
#   ▐▒▒▒▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄▒▌  
#   ▌░░▌█▀▒▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐  
#  ▐░░░▒▒▒▒▒▒▒▒▌██▀▒▒░░░▒▒▒▀▄▌ 
#  ▌░▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒▌ 
# ▌▒▒▒▄██▄▒▒▒▒▒▒▒▒░░░░░░░░▒▒▒▐ 
# ▐▒▒▐▄█▄█▌▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▒▒▒▌
# ▐▒▒▐▀▐▀▒▒▒▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▒▐ 
#  ▌▒▒▀▄▄▄▄▄▄▀▒▒▒▒▒▒▒░▒░▒░▒▒▒▌ 
#  ▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒░▒▒▄▒▒▐  
#   ▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒░▒░▒▄▒▒▒▒▌  
#     ▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀   
#       ▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀     
#          ▀▀▀▀▀▀▀▀▀▀▀▀        
     