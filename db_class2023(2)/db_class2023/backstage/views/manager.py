from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app
import cx_Oracle
import io
from PIL import Image
import base64
import binascii
from io import BytesIO

UPLOAD_FOLDER = 'static/product'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.productManager'))

@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        pid = request.values.get('delete')
        data = Record.delete_check(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = Product.get_product(pid)
            Product.delete_product(pid)
    
    elif 'edit' in request.values:
        pid = request.values.get('edit')
        return redirect(url_for('manager.edit', pid=pid))

    book_data = book()    
    return render_template('productManager.html', book_data = book_data, user=current_user.name)    

@login_required   
def book():
    mid = current_user.id
    book_row = Product.get_all_product(mid)
    book_data = []
    for i in book_row:
        if i[7] is not None:
            # 假設 hex_data 是 'LOB' 對象
            hex_data = i[7]

            # 讀取 'LOB' 對象的二進制數據
            binary_data = hex_data.read()

            # 將二進制數據轉換為圖片
            image = Image.open(io.BytesIO(binary_data))

            # 將圖片轉換為 base64 字符串
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode("utf-8")
        else:
            img_str = None
        book = {
          '商品編號': i[0],
          '商品名稱': i[1],
          '商品售價': i[2],
          '商品類別': i[3],
          '商品數量': i[5],
          '商品圖片': img_str
        }
        
        book_data.append(book)
    return book_data


#############################################################################################################################################################
@manager.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        newsname = request.values.get('delete')
        data = News.delete_check(newsname)
        
      #  if(data != None):
     #       flash('failed')
     #   else:
        data = News.get_news_data(newsname)
        News.delete_news(newsname)
    
    elif 'edit' in request.values:
        title = request.values.get('edit')
        return redirect(url_for('manager.editNews', title=title))

    news_data = news()    
    return render_template('publish.html', news_data = news_data, user=current_user.name)

@login_required   
def news():
    mid = current_user.id
    news_row = News.get_all_news(mid)
    news_data = []
    for i in news_row:
        news = {
          '消息標題': i[0],
          '發布內文': i[1],
          '發布時間': i[2]
        }
        
        news_data.append(news)
    return news_data

@manager.route('/addnews', methods=['GET', 'POST'])
@login_required
def addnews():
    if request.method == 'POST':

        title = request.values.get('title')
        content = request.values.get('content')
        releasetime = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

        News.add_news(
                {'title' : title,
                'content' : content,
                'releasetime' : releasetime,
                'sellerid':current_user.id,
                }
        )

        return redirect(url_for('manager.publish'))

    return render_template('publish.html')

@manager.route('/editNews', methods=['GET', 'POST'])
@login_required
def editNews():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':
        News.update_news(
            {
            'title' : request.values.get('title'),
            'content' : request.values.get('content'),
            'sellerid': current_user.id ,
            'releasetime': request.values.get('releasetime')      
            }
        )
        
        return redirect(url_for('manager.publish'))

    else:
        news = show_new_info()
        return render_template('editNews.html', data=news)


def show_new_info():
    title = request.args['title']
    mid = current_user.id
    data = News.get_news_data(title)
    #title = data[0]
    content= data[1]
    release = data[2]
    
    news = {
        '消息標題': title,
        '發布內文': content,
        '發布時間': release
    }
    return news
################################################################################################################################
#新增商品
@manager.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            pid = en + number
            data = Product.get_product(pid)

        name = request.values.get('name')
        price = request.values.get('price')
        category = request.values.get('category')
        description = request.values.get('description')
        num = request.values.get('num')
        image  = request.files['image']
        image.save(image.filename)
        file_upload = convert_into_binary(image.filename)
        #secure_file = secure_filename(file_upload)
        if (len(name) < 1 or len(price) < 1):
            return redirect(url_for('manager.productManager'))
        existProduct = Product.get_all_name()
        productList =[]
        for i in existProduct:
            productList.append(i[0])
        if(name in productList):
            flash('Falied!')  
            return redirect(url_for('manager.productManager'))
            
        else:  
            Product.add_product(
                {'pid' : pid,
                'name' : name,
                'price' : price,
                'category' : category,
                'description':description,
                'num':num,
                'id': current_user.id,
                'image':file_upload 
                }

            )

        return redirect(url_for('manager.productManager'))

    return render_template('productManager.html')

def convert_into_binary(file_path):
  with open(file_path, 'rb') as file:
    binary = file.read()
  return binary

@manager.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':

        editimage  = request.files['editimage']
        #editimage.seek(0, os.SEEK_END)
       
        
        if editimage.filename != "" :
            editimage.save(editimage.filename)
            edit_file_upload = convert_into_binary(editimage.filename)
            
            Product.update_product_withImage(
                {
                'name' : request.values.get('name'),
                'price' : request.values.get('price'),
                'category' : request.values.get('category'), 
                'description' : request.values.get('description'),
                'num' : request.values.get('num'),
                'pid' : request.values.get('pid'),
                'editimage':edit_file_upload
                }
            )
        else:
            Product.update_product(
                {
                'name' : request.values.get('name'),
                'price' : request.values.get('price'),
                'category' : request.values.get('category'), 
                'description' : request.values.get('description'),
                'num' : request.values.get('num'),
                'pid' : request.values.get('pid')
                }
            )
        return redirect(url_for('manager.productManager'))

    else:
        product = show_info()
        return render_template('edit.html', data=product)


def show_info():
    pid = request.args['pid']
    data = Product.get_product(pid)
    pname = data[1]
    price = data[2]
    category = data[3]
    description = data[4]
    num = data[5]
   # image = data[6]
    if data[7] is not None:
        # 假設 hex_data 是 'LOB' 對象
        hex_data = data[7]

        # 讀取 'LOB' 對象的二進制數據
        binary_data = hex_data.read()

        # 將二進制數據轉換為圖片
        image = Image.open(io.BytesIO(binary_data))

        # 將圖片轉換為 base64 字符串
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode("utf-8")
    else:
        img_str = None

    product = {
        '商品編號': pid,
        #'商品圖片': image,
        '商品名稱': pname,
        '單價': price,
        '類別': category,
        '商品敘述': description,
        '數量': num,
        '商品圖片': img_str,
    }
    return product

###########################################################################################################################################
@manager.route('/orderManager', methods=['GET', 'POST'])
@login_required
def orderManager():
    if request.method == 'POST':
        pass
    else:
        sno = current_user.id
        order_row = Order_List.get_order(sno)
        order_data = []
        for i in order_row:
            order = {
                '訂單編號': i[0],
                '訂購人': i[1],
                '訂單總價': i[2],
                '訂單時間': i[3]
            }
            order_data.append(order)
            
        orderdetail_row = Order_List.get_orderdetail()
        order_detail = []

        for j in orderdetail_row:
            orderdetail = {
                '訂單編號': j[0],
                '商品名稱': j[1],
                '商品單價': j[2],
                '訂購數量': j[3],
                '領貨方式': j[4],
                '付款方式': j[5],
            }
            order_detail.append(orderdetail)

    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)


#########################################################################################

  
