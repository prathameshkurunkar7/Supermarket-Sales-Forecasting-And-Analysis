from flask import Flask,render_template,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

import io
from base64 import encodebytes
from PIL import Image


import qrcode
import visuals as vs
import models as mo

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)

class Order(db.Model):
    oid = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime)
    products = db.relationship('Product',backref='order',lazy=True)

    def __init__(self,date):
        self.date = date
        # self.products = products
    
class Product(db.Model):
    pid = db.Column(db.Integer,primary_key=True)#auto increment by default
    name = db.Column(db.String(100),unique = True)
    qty = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.oid'),
        nullable=False)

    def __init__(self,name,qty,order):
        self.name = name
        self.qty = qty
        self.order_id = order

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('oid','date','products')

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('pid','name','qty','order_id')

# Init Schema
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/select-category')
def categorySelector():
    obj = vs.SuperMarketSalesAnalysis()
    category = request.args['selected']
    plot = obj.yearlySalesPerCategory(category)

    return plot

@app.route('/select-subcategory')
def subCategorySelector():
    obj = vs.SuperMarketSalesAnalysis()
    subCategory = request.args['selected']
    plot = obj.yearlySalesPerSubCategory(subCategory)

    return plot

@app.route('/select-monthly-subcategory')
def monthlySubCategorySelector():
    obj = vs.SuperMarketSalesAnalysis()
    subCategory = request.args['selected']
    plot = obj.monthlySalesPerSubCategory(subCategory)

    return plot

@app.route('/select-year')
def yearlyProfitSelector():
    obj = vs.SuperMarketSalesAnalysis()
    year = request.args['year']
    plot = obj.profitSalesPerYear(year)

    return plot

@app.route('/forecast')
def forecast():
    obj = mo.Forecasts()
    date = request.args['date']
    category = request.args['category']
    res=obj.predict(category,date)

    return res

@app.route('/subcat-forecast')
def subcatForecast():
    obj = mo.Forecasts()
    date = request.args['date']
    subcategory = request.args['sub-category']
    res=obj.subCatPredict(subcategory,date)

    return res

@app.route('/dashboard/forecast')
def forecastPage():

    return render_template('Forecast.html')

@app.route('/dashboard/regional')
def regionalRoute():
    obj = vs.SuperMarketSalesAnalysis()
    plot1 = obj.regionWiseSales()
    plot2 = obj.regionVsQuantity()
    plot3 = obj.regionVsQuantityYearly()
    
    return render_template('Regional.html',plot1= plot1,plot2=plot2,plot3 = plot3)

@app.route('/dashboard/financial')
def financial():
    obj = vs.SuperMarketSalesAnalysis()
    plot1 = obj.discountVsSalesAndProfit()
    plot2 = obj.yearlyProfit()
    plot3 = obj.yearlySales()
    plot4 = obj.discountVsSales()
    plot5 = obj.discountVsProfit()
    plot6 = obj.profitSalesPerYear('2014')

    return render_template('Financial.html',plot1 = plot1,plot2 = plot2,plot3=plot3,plot4 = plot4,plot5=plot5,plot6 = plot6)

@app.route('/dashboard/categorical')
def categorical():
    obj = vs.SuperMarketSalesAnalysis()
    plot1 = obj.categoricalSales()
    plot2 = obj.yearlySalesPerCategory('Furniture')

    return render_template('Categorical.html',plot1= plot1,plot2=plot2)

@app.route('/dashboard/subcategorical')
def sub_categorical():

    obj = vs.SuperMarketSalesAnalysis()
    plot1 = obj.subcategoricalSales()
    plot2 = obj.yearlySalesPerSubCategory('Bookcases')
    plot3 = obj.monthlySalesPerSubCategory('Bookcases')

    return render_template('Subcategorical.html',plot1=plot1,plot2=plot2,plot3=plot3)

@app.route('/dashboard/other')
def other():

    obj = vs.SuperMarketSalesAnalysis()
    plot1 = obj.temperatureSales()
    plot2 = obj.fuelPriceVsSales()
    plot3 = obj.holidaySales()

    return render_template('Other.html',plot1=plot1,plot2= plot2,plot3=plot3)

@app.route('/dashboard/cart')
def cartPage():

    return render_template('Cart.html')

# Database Routes

@app.route('/addToCart',methods=['POST'])
def addToCart():

    date = request.json['date']
    name = request.json['name']
    qty = request.json['qty']

    date = datetime.strptime(date,'%Y-%m-%d').date()

    new_order = Order(date)
    db.session.add(new_order)
    db.session.commit()

    new_prod = Product(name,int(qty),new_order.oid)

    db.session.add(new_prod)
    db.session.commit()

    return product_schema.jsonify(new_prod)

@app.route('/getCart',methods=['GET'])
def getCart():
    all_prod = Product.query.all()
    res = products_schema.dump(all_prod)

    for item in res:
        order=Order.query.get(item.get('order_id'))
        item['date'] = datetime.strftime(order.date,'%Y-%m-%d')

    return jsonify(res)

@app.route('/removeFromCart',methods=['DELETE'])
def removeFromCart():
    pid = request.json['pid']

    prod = Product.query.get(int(pid))
    order = Order.query.get(prod.order_id)
    db.session.delete(prod)
    db.session.commit()

    db.session.delete(order)
    db.session.commit()

    all_prod = Product.query.all()
    res = products_schema.dump(all_prod)

    return jsonify({"message":'Product removed',"itemsInCart":len(res)})

@app.route('/placeOrder',methods=['PATCH'])
def placeOrder():
    order = request.json
    
    for item in order:
        pid = int(item.get('pid')[-1:])

        prod = Product.query.get(pid)
        qty = item.get('qty')

        prod.qty = qty
        db.session.commit()

    with open('./invoices/{}.txt'.format("Invoice"),"w") as f:
        f.write("Product {}".format(' '*30))
        f.write('Qty\n')

        for item in order:
            name = item.get('name')
            date = item.get('date')
            qty = item.get('qty')

            f.write('{}{}'.format(name,' '*30))
            f.write('{}{}'.format(date,' '*30))
            f.write('{}\n'.format(qty))


    return jsonify({'message':"Product List Received"})

@app.route('/supplier')
def supplier():

    return render_template('Supplier.html')


@app.route('/getOrders',methods=['POST'])
def getOrders():

    all_prod = Product.query.all()
    res = products_schema.dump(all_prod)

    date = request.json['date']

    orderlist=[]
    for item in res:
        order=Order.query.get(item.get('order_id'))
        item['date'] = datetime.strftime(order.date,'%Y-%m-%d')

        if item.get('date') == date:
            orderlist.append(item)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    if len(orderlist)>0:
        qr.add_data('Product {} Date {} Qty\n'.format(' '*20,' '*20))

        for item in orderlist:
            name = item.get('name')
            date = item.get('date')
            qty = item.get('qty')
            qr.add_data('{} {} {} {} {} \n'.format(name,' '*10,date,' '*10,qty))

        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
    
        img.save('Invoice.png')

        image_path = './Invoice.png'
        encoded_img = get_response_image(image_path)
        my_message = 'Scan QR Code to receive order'
        response =  { 'Status' : 'Success', 'message': my_message , 'ImageBytes': encoded_img,'totalProducts':len(orderlist)}

    else:
        response =  { 'Status' : 'Success', 'message': 'No Orders for this month','totalProducts':len(orderlist)}

    return jsonify(response)

if __name__ =='__main__':
    app.run(debug=True)