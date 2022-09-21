import os
import urllib.parse
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=sn-asset.database.windows.net;DATABASE=db-asset;UID=adminrdc;PWD=Welcome123")

app = Flask(__name__)
cors = CORS(app, resources={r'/assets/*': {'origins': '*'}})

app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.description}"


# @app.route('/')
# def index():
#     return 'Hello!'

@app.route('/assets')
def get_assets():
    assets = Asset.query.all()

    output = []
    for asset in assets:
        asset_data = {'id': asset.id, 'name': asset.name, 'category': asset.category, 'quantity': asset.quantity, 'price': asset.price, 'total_price': asset.total_price, 'description': asset.description}

        output.append(asset_data)
    return output

#view
@app.route('/assets/<id>')
def get_asset(id):
    asset = Asset.query.get_or_404(id)
    return {"id": asset.id, "name": asset.name, "category": asset.category, "quantity": asset.quantity, "price": asset.price, "total_price": asset.total_price, "description": asset.description}

#add
@app.route('/assets', methods=['POST'])
def add_asset():
    asset = Asset(name=request.json['name'], category=request.json['category'], quantity=request.json['quantity'], price=request.json['price'], total_price=request.json['total_price'], description=request.json['description'])
    db.session.add(asset)
    db.session.commit()
    return {'id': asset.id}

#update
@app.route('/assets/<id>', methods=['PUT'])
def update_asset(id):
    asset = Asset.query.filter_by(id=id).first()
   
    asset.name = request.json['name']
    asset.category = request.json['category']
    asset.quantity = request.json['quantity']
    asset.price = request.json['price']
    asset.total_price = request.json['total_price']
    asset.description = request.json['description']

    db.session.commit()

    return {'id': asset.id}

#delete
@app.route('/assets/<id>', methods=['DELETE'])
def delete_asset(id):
    asset = Asset.query.get(id)
    if asset is None:
        return {"error": "Not Found"}
    db.session.delete(asset)
    db.session.commit()
    return {"message": "Deleted Successfully!"}


    
if __name__ == '__main__':
   app.run()