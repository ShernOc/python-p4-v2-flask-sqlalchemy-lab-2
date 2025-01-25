from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin # type: ignore


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    #add serialization
    serialize_only = ('id','name')
    serialize_rules = ('-review.customer',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    #relationship
    
    reviews = db.relationship("Review", back_populates = "customer", cascade = "all, delete-orphan")
    
   #  association_proxy
    items = association_proxy('reviews','item', creator = lambda item_obj:Review(item=item_obj))
    
    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'item'
    serialize_only= ('id','name','price')
    serialize_rules = ('-reviews.item',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    
    reviews = db.relationship("Review", back_populates = "item", )

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    
    
class Review(db.Model, SerializerMixin):
    ___tablename__ = "reviews"
    serialize_only = ('id', 'comment, customer_id', 'item_id')
    serialize_rules = ('-item.reviews', '-customer.reviews',)
    
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"))

    #relationship 
    customer = db.relationship("Customer", back_populates = "reviews")
    item = db.relationship("Item", back_populates = "reviews")
    
    

