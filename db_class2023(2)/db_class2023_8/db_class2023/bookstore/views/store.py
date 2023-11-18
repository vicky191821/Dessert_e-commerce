import re
from typing_extensions import Self
from flask import Flask, request, template_rendered, Blueprint
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from datetime import datetime
from numpy import identity, product
import random, string
from sqlalchemy import null
from link import *
import math
from base64 import b64encode
from api.sql import Member, Order_List, Product, Record, Cart, News
import cx_Oracle
import io
from PIL import Image
import base64
import binascii
from io import BytesIO

store = Blueprint("bookstore", __name__, template_folder="../templates")


@store.route("/", methods=["GET", "POST"])
@login_required
def bookstore():
    result = Product.count()
    count = math.ceil(result[0] / 10)
    flag = 0

    if request.method == "GET":
        if current_user.role == "manager":
            flash("No permission")
            return redirect(url_for("manager.home"))

    if "keyword" in request.args and "page" in request.args:
        total = 0
        single = 1
        page = int(request.args["page"])
        start = (page - 1) * 10
        end = page * 10
        search = request.values.get("keyword")
        keyword = search

        cursor.prepare("SELECT * FROM PRODUCT WHERE PNAME LIKE :search")
        cursor.execute(None, {"search": "%" + keyword + "%"})
        book_row = cursor.fetchall()
        book_data = []
        final_data = []

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
                img_str = "data:image/jpeg;base64," + base64.b64encode(
                    buffered.getvalue()
                ).decode("utf-8")
            else:
                img_str = None

            book = {
                "商品編號": i[0],
                "商品名稱": i[1],
                "商品價格": i[2],
                "商品種類": i[3],
                "商品數量": i[5],
                "商品圖片": img_str,
            }
            book_data.append(book)
            total = total + 1

        if len(book_data) < end:
            end = len(book_data)
            flag = 1

        for j in range(start, end):
            final_data.append(book_data[j])

        count = math.ceil(total / 10)

        return render_template(
            "bookstore.html",
            single=single,
            keyword=search,
            book_data=book_data,
            user=current_user.name,
            page=1,
            flag=flag,
            count=count,
        )

    elif "pid" in request.args:
        pid = request.args["pid"]
        data = Product.get_product(pid)

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
            img_str = "data:image/jpeg;base64," + base64.b64encode(
                buffered.getvalue()
            ).decode("utf-8")
        else:
            img_str = None

        pname = data[1]
        price = data[2]
        category = data[3]
        description = data[4]
        image = "sdg.jpg"

        product = {
            "商品編號": pid,
            "商品名稱": pname,
            "單價": price,
            "類別": category,
            "商品敘述": description,
            "商品圖片": img_str,
        }

        return render_template("product.html", data=product, user=current_user.name)

    elif "page" in request.args:
        page = int(request.args["page"])
        start = (page - 1) * 10
        end = page * 10

        book_row = Product.get_all()
        book_data = []
        final_data = []

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
                img_str = "data:image/jpeg;base64," + base64.b64encode(
                    buffered.getvalue()
                ).decode("utf-8")
            else:
                img_str = None

            book = {
                "商品編號": i[0],
                "商品名稱": i[1],
                "商品價格": i[2],
                "商品種類": i[3],
                "商品數量": i[5],
                "商品圖片": img_str,
            }
            book_data.append(book)

        if len(book_data) < end:
            end = len(book_data)
            flag = 1

        for j in range(start, end):
            final_data.append(book_data[j])

        return render_template(
            "bookstore.html",
            book_data=final_data,
            user=current_user.name,
            page=page,
            flag=flag,
            count=count,
        )

    elif "keyword" in request.args:
        single = 1
        search = request.values.get("keyword")
        keyword = search
        cursor.prepare("SELECT * FROM PRODUCT WHERE PNAME LIKE :search")
        cursor.execute(None, {"search": "%" + keyword + "%"})
        book_row = cursor.fetchall()
        book_data = []
        total = 0

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
                img_str = "data:image/jpeg;base64," + base64.b64encode(
                    buffered.getvalue()
                ).decode("utf-8")
            else:
                img_str = None

            book = {
                "商品編號": i[0],
                "商品名稱": i[1],
                "商品價格": i[2],
                "商品種類": i[3],
                "商品數量": i[5],
                "商品圖片": img_str,
            }

            book_data.append(book)
            total = total + 1

        if len(book_data) < 10:
            flag = 1

        count = math.ceil(total / 10)

        return render_template(
            "bookstore.html",
            keyword=search,
            single=single,
            book_data=book_data,
            user=current_user.name,
            page=1,
            flag=flag,
            count=count,
        )
    elif "categorymain" in request.args:
        total = 0
        single = 2

        dessert_type = request.args.get("categorymain")

        cursor.prepare("SELECT * FROM PRODUCT WHERE CATEGORY =:dessert_type")
        cursor.execute(None, {"dessert_type": dessert_type})
        book_row = cursor.fetchall()
        book_data = []
        total = 0

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
                img_str = "data:image/jpeg;base64," + base64.b64encode(
                    buffered.getvalue()
                ).decode("utf-8")
            else:
                img_str = None

            book = {
                "商品編號": i[0],
                "商品名稱": i[1],
                "商品價格": i[2],
                "商品種類": i[3],
                "商品數量": i[5],
                "商品圖片": img_str,
            }

            book_data.append(book)
            total = total + 1

        if len(book_data) < 10:
            flag = 1

        count = math.ceil(total / 10)

        return render_template(
            "bookstore.html",
            single=single,
            categorymain=dessert_type,
            book_data=book_data,
            user=current_user.name,
            page=1,
            flag=flag,
            count=count,
        )
    else:
        book_row = Product.get_all()
        book_data = []
        temp = 0
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
                img_str = "data:image/jpeg;base64," + base64.b64encode(
                    buffered.getvalue()
                ).decode("utf-8")
            else:
                img_str = None
            book = {
                "商品編號": i[0],
                "商品名稱": i[1],
                "商品價格": i[2],
                "商品種類": i[3],
                "商品數量": i[5],
                "商品圖片": img_str,
            }
            if len(book_data) < 10:
                book_data.append(book)

        return render_template(
            "bookstore.html",
            book_data=book_data,
            user=current_user.name,
            page=1,
            flag=flag,
            count=count,
        )


# 會員購物車
@store.route("/cart", methods=["GET", "POST"])
@login_required  # 使用者登入後才可以看
def cart():
    # 以防管理者誤闖
    if request.method == "GET":
        if current_user.role == "manager":
            flash("No permission")
            return redirect(url_for("manager.home"))

    # 回傳有 pid 代表要 加商品
    if request.method == "POST":
        if "pid" in request.form:
            data = Cart.get_cart(current_user.id)

            if data == None:  # 假如購物車裡面沒有他的資料
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Cart.add_cart(current_user.id, time)  # 幫他加一台購物車
                data = Cart.get_cart(current_user.id)

            tno = data[2]  # 取得交易編號
            pid = request.values.get("pid")  # 使用者想要購買的東西
            # 檢查購物車裡面有沒有商品
            product = Record.check_product(pid, tno)
            # 取得商品價錢
            price = Product.get_product(pid)[2]

            # 如果購物車裡面沒有的話 把他加一個進去
            if product == None:
                Record.add_product(
                    {"id": tno, "tno": pid, "price": price, "total": price}
                )
            else:
                # 假如購物車裡面有的話，就多加一個進去
                amount = Record.get_amount(tno, pid)
                total = (amount + 1) * int(price)
                Record.update_product(
                    {"amount": amount + 1, "tno": tno, "pid": pid, "total": total}
                )

        elif "delete" in request.form:
            pid = request.values.get("delete")
            tno = Cart.get_cart(current_user.id)[2]

            Member.delete_product(tno, pid)
            product_data = only_cart()

        elif "user_edit" in request.form:
            change_order()
            return redirect(url_for("bookstore.bookstore"))

        elif "buy" in request.form:
            change_order()
            return redirect(url_for("bookstore.order"))

        elif "order" in request.form:
            tno = Cart.get_cart(current_user.id)[2]
            total = Record.get_total_money(tno)
            Cart.clear_cart(current_user.id)

            data = Record.get_product_sell_id(tno)

            pay = request.values.get("inputpayment")
            way = request.values.get("way")
            bankname = request.values.get("bankname")
            bankid = request.values.get("bankid")
            cardnumber = request.values.get("cardnumber")
            safecode = request.values.get("safecode")
            duedate = request.values.get("duedate")
            time = str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            format = "yyyy/mm/dd hh24:mi:ss"
            tool = request.values.get("toolway")
            no = "no"
            tmp = "404"

            if pay == "信用卡":
                for i in data:
                    Order_List.add_order(
                        {
                            "mid": current_user.id,
                            "time": time,
                            "total": total,
                            "format": format,
                            "tno": tno,
                            "way": way,
                            "pay": pay,
                            "bankname": bankname,
                            "bankid": bankid,
                            "cardnumber": cardnumber,
                            "safecode": safecode,
                            "duedate": duedate,
                            "tool": no,
                            "sellerid": i[0],
                        }
                    )
            elif pay == "貨到付款":
                for i in data:
                    Order_List.add_order(
                        {
                            "mid": current_user.id,
                            "time": time,
                            "total": total,
                            "format": format,
                            "tno": tno,
                            "way": way,
                            "pay": pay,
                            "bankname": no,
                            "bankid": tmp,
                            "cardnumber": tmp,
                            "safecode": tmp,
                            "duedate": tmp,
                            "tool": no,
                            "sellerid": i[0],
                        }
                    )
            else:
                for i in data:
                    Order_List.add_order(
                        {
                            "mid": current_user.id,
                            "time": time,
                            "total": total,
                            "format": format,
                            "tno": tno,
                            "pay": pay,
                            "way": way,
                            "bankname": "no",
                            "bankid": tmp,
                            "cardnumber": tmp,
                            "safecode": tmp,
                            "duedate": tmp,
                            "tool": tool,
                            "sellerid": i[0],
                        }
                    )
            return render_template("complete.html", user=current_user.name)
        # else:
        #   # Order_List.add_order(
        #        {
        #        'mid': current_user.id,
        #        'time':time,
        #       'total':total,
        #         'format':format,
        #      'tno':tno,
        #     'pay':pay,
        #    'way':way,
        #   'bankname':"no",
        #  'bankid':"no",
        #  'cardnumber':"no",
        #  'safecode':"no",
        #  'duedate':"no"
        #  }
        # )
        # return render_template('complete.html', user=current_user.name)

    product_data = only_cart()

    if product_data == 0:
        return render_template("empty.html", user=current_user.name)
    else:
        return render_template("cart.html", data=product_data, user=current_user.name)


@store.route("/order")
def order():
    data = Cart.get_cart(current_user.id)
    tno = data[2]

    product_row = Record.get_record(tno)
    product_data = []

    for i in product_row:
        pname = Product.get_name(i[1])
        product = {"商品編號": i[1], "商品名稱": pname, "商品價格": i[3], "數量": i[2]}
        product_data.append(product)

    total = Record.get_total(tno)[0]

    return render_template(
        "order.html", data=product_data, total=total, user=current_user.name
    )


@store.route("/orderlist")
def orderlist():
    if "oid" in request.args:
        pass

    user_id = current_user.id

    data = Member.get_order(user_id)
    orderlist = []

    for i in data:
        temp = {"訂單編號": i[0], "訂單總價": i[3], "訂單時間": i[2]}
        orderlist.append(temp)

    orderdetail_row = Order_List.get_orderdetail()
    orderdetail = []

    for j in orderdetail_row:
        temp = {
            "訂單編號": j[0],
            "商品名稱": j[1],
            "商品單價": j[2],
            "訂購數量": j[3],
            "領貨方式": j[4],
            "付款方式": j[5],
        }
        orderdetail.append(temp)

    return render_template(
        "orderlist.html", data=orderlist, detail=orderdetail, user=current_user.name
    )


# 加了這裡


@store.route("/news")
def news():
    newslist_row = News.get_news()
    newslist = []
    for i in newslist_row:
        temp = {
            "標題": i[0],
            "內容": i[1],
            "發布時間": i[2],
            "發布者": i[3],
        }
        newslist.append(temp)

    return render_template("news.html", news=newslist, user=current_user.name)


def change_order():
    data = Cart.get_cart(current_user.id)
    tno = data[2]  # 使用者有購物車了，購物車的交易編號是什麼
    product_row = Record.get_record(data[2])

    for i in product_row:
        # i[0]：交易編號 / i[1]：商品編號 / i[2]：數量 / i[3]：價格
        if int(request.form[i[1]]) != i[2]:
            Record.update_product(
                {
                    "amount": request.form[i[1]],
                    "pid": i[1],
                    "tno": tno,
                    "total": int(request.form[i[1]]) * int(i[3]),
                }
            )
            print("change")
        update_quantity(i[1], int(request.form[i[1]]))

    return 0


def update_quantity(pid, amount):  # 更新庫存數量
    # 取得目前商品庫存數
    product = Product.get_num(pid)

    # 計算新的數量
    new_quantity = product - amount

    # 更新商品數量
    Product.update_product_pnum(pid, new_quantity)

    return 0


def only_cart():
    count = Cart.check(current_user.id)

    if count == None:
        return 0

    data = Cart.get_cart(current_user.id)
    tno = data[2]
    product_row = Record.get_record(tno)
    product_data = []

    for i in product_row:
        pid = i[1]
        pname = Product.get_name(i[1])
        price = i[3]
        amount = i[2]

        product = {"商品編號": pid, "商品名稱": pname, "商品價格": price, "數量": amount}
        product_data.append(product)

    return product_data