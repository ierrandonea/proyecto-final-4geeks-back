import json
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

# to consult database schema: https://dbdesigner.page.link/xvnBfzE4JMMCnLmx5

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(120), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    presentation = db.Column(db.String(120), nullable=False)
    attributes = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)    
    product_ratings = db.relationship("product_ratings", backref="product")

    def serialize(self):
        return{
            "id": self.id,
            "sku": self.sku
            "price": self.price
            "brand": self.brand
            "name": self.name
            "category": self.category,
            "presentation": self.presentation,
            "attributes": self.attributes,
            "description": self.description,
            "image": self.image,
            "thumbnail": self.thumbnail,
            "stock": self.stock
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    cover = db.Column(db.String(255), nullable=False)
    images = db.Column(db.String(255), nullable=False)
    resume = db.Column(db.String(280), nullable=False)
    body = db.Column(db.Text, nullable=False)
    # please organize large text areas as:
    # {
        # "paragraph_1": "lorem ipsum...",
        # "paragraph_2": "lorem ipsum...",
        # ...
    # }   
    content_ratings = db.relationship("content_ratings", backref="contents")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "cover": self.cover,
            "images": self.images,
            "resume": self.resume,
            "body": self.body
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Product_Ratings(db.Model):
    __tablename__ = 'product_ratings'
    id = db.Column(db.Integer, primary_key=True)
    product_id =  db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(280), nullable=True)
    date = db.Column(db.Date, nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "username": self.user.full_name,
            "start": self.stars,
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

class Content_Ratings(db.Model):
    __tablename__ = 'content_ratings'
    id = db.Column(db.Integer, primary_key=True)
    content_id =  db.Column(db.Integer, db.ForeignKey('contents.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(280), nullable=True)
    date = db.Column(db.Date, nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "username": self.user.full_name,
            "likes": self.likes,
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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)    
    product_ratings = db.relationship("product_ratings", backref="user")    
    content_ratings = db.relationship("content_ratings", backref="user")
    orders = db.relationship("orders", backref="user")  

    def serialize(self):
        return{
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "category": self.category,
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

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ammount = db.Column(db.String(120), nullable=False)
    shipping_address = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    order_email = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Varchar(255), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    order_detail = db.relationship("order_details", backref="orders")  

    def serialize(self):
        return{
            "id": self.id,
            "ammount": self.ammount,
            "shipping_address": self.shipping_address,
            "full_name": self.full_name,
            "order_email": self.order_email,
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

class Order_Details(db.Model):
    __tablename__ = 'order_details'
    id = db.Column(db.Integer, primary_key=True)    
    product_id =  db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    event_id =  db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    order_id =  db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.String(120), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "price": self.price,
            "sku": self.sku,
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

class Product_Category(db.Model):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer, primary_key=True)
    product_id =  db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

class Event_Category(db.Model):
    __tablename__ = 'event_categories'
    id = db.Column(db.Integer, primary_key=True)
    event_id =  db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    cover = db.Column(db.String(255), nullable=False)
    images = db.Column(db.String(255), nullable=False)
    resume = db.Column(db.String(280), nullable=False)
    body = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(120), nullable=False)
    order_detail = db.relationship("oerder_details", backref="event")

    def serialize(self):
        return{
            "id": self.id,
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
     