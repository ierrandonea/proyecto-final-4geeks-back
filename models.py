import json
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_image = db.Column(db.String(120), nullable=False)

    product_name = db.Column(db.String(120), nullable=False)
    product_price = db.Column(db.String(120), nullable=False)

    product_attributes = db.Column(db.String(255), nullable=False)
    product_description = db.Column(db.Text, nullable=False)

    product_format = db.Column(db.String(120), nullable=False)
    product_stock = db.Column(db.Integer, nullable=False)
    
    product_ratings = db.relationship("Product_ratings", backref="product")

    def serialize(self):
        return{
            "id": self.id,
            "product_image": self.title,
            "product_name": self.content,
            "product_price": self.user_id,
            "product_attributes": self.product_attributes,
            "product_description": self.product_description,
            "product_format": self.product_format,
            "product_stock": self.product_stock
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
            "content_ratings": self.content_ratings
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
     