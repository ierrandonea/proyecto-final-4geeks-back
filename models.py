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
    product_ratings = db.relationship("Product_ratings", backref="product")

    def serialize(self):
        return{
            "id": self.id,
            "sku": self.sku
            "price": self.sku
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
    __tablename__ = 'content'
    id = db.Column(db.Integer, primary_key=True)
    content_cover = db.Column(db.String(120), nullable=False)
    content_images = db.Column(db.String(255), nullable=False)
    
    content_name = db.Column(db.String(120), nullable=False)    
    content_resume = db.Column(db.String(255), nullable=False)    
    content_description = db.Column(db.Text, nullable=False)
    
    content_ratings = db.relationship("Content_ratings", backref="content")

    def serialize(self):
        return{
            "id": self.id,
            "content_cover": self.content_cover,
            "content_images": self.content_images,
            "content_name": self.content_name,
            "content_resume": self.content_resume,
            "content_description": self.content_description,
            "content_ratings": self.content_ratings,
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Product_ratings(db.Model):
    __tablename__ = 'product_ratings'
    id = db.Column(db.Integer, primary_key=True)
    product_id =  db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    p_rating_stars = db.Column(db.Integer, nullable=False)
    p_rating_comment = db.Column(db.String(280), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "product_id": self.product_id,
            "p_rating_stars": self.p_rating_stars,
            "p_rating_comment": self.p_rating_comment
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Content_ratings(db.Model):
    __tablename__ = 'product_ratings'
    id = db.Column(db.Integer, primary_key=True)
    content_id =  db.Column(db.Integer, db.ForeignKey('contents.id'), nullable=False)
    p_rating_likes = db.Column(db.Integer, nullable=False)
    p_rating_comment = db.Column(db.String(280), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "content_id": self.content_id,
            "p_rating_likes": self.p_rating_likes,
            "p_rating_comment": self.p_rating_comment
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
     