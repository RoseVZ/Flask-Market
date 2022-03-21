from enum import unique
from multiprocessing import Value
from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    item_name= db.Column(db.String(30), nullable =False, unique=True)
    code = db.Column(db.String(40),nullable=True,unique=True)
    price = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    def buy(self,user):
        self.owner = user.id
        user.budget = user.budget - self.price
        db.session.commit()
    def sell(self, user):
        self.owner = None
        user.budget =user.budget +self.price
        db.session.commit()


    def __repr__(self):
        return f'Item {self.item_name}'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(50),nullable=False,unique=True)
    emailadd=db.Column(db.String(80),nullable=False,unique=True)
    password = db.Column(db.String(60),nullable =False)
    budget = db.Column(db.Integer,nullable=False, default = 1000)
    items = db.relationship('Item',backref='owned_user', lazy =True)


    @property
    def prettier_budget(self):#display budget with commas
        if(len(str(self.budget))) >=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f'{self.budget}'

           
    @property
    def password1(self):
        return self.password1

    @password1.setter
    def password1(self, plain_text_password):#hash the password stored
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    def can_purchase(self, item_ob):
        return self.budget>=item_ob.price

    def can_sell(self, item_ob):
        return item_ob in self.items

    def __repr__(self):
        return f'Item {self.username}'