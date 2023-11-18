from typing import Optional
from link import *

class DB():
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()

class Member():
    def get_member(account):
        sql = "SELECT ACCOUNT, PASSWORD, MID, IDENTITY, NAME FROM MEMBER WHERE ACCOUNT = :id"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'id' : account}))
    
    def get_all_account():
        sql = "SELECT ACCOUNT FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def create_member(input):
        sql = 'INSERT INTO MEMBER VALUES (null, :name, :account, :password, :identity, :tel, :email, TO_DATE(:time, :format ), :address)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(tno, pid):
        sql = 'DELETE FROM RECORD WHERE TNO=:tno and PID=:pid '
        DB.execute_input(DB.prepare(sql), {'tno': tno, 'pid':pid})
        DB.commit()
        
    def get_order(userid):
        sql = 'SELECT * FROM ORDER_LIST WHERE MID = :id ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':userid}))
    
    def get_role(userid):
        sql = 'SELECT IDENTITY, NAME FROM MEMBER WHERE MID = :id '
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':userid}))

class Cart():
    def check(user_id):
        sql = 'SELECT * FROM CART, RECORD WHERE CART.MID = :id AND CART.TNO = RECORD.TNO'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
        
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))

    def add_cart(user_id, time):
        sql = 'INSERT INTO CART VALUES (:id, :time, cart_tno_seq.nextval)'
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time})
        DB.commit()

    def clear_cart(user_id):
        sql = 'DELETE FROM CART WHERE MID = :id '
        DB.execute_input( DB.prepare(sql), {'id': user_id})
        DB.commit()
       #product
class Product():
    def count():
        sql = 'SELECT COUNT(*) FROM PRODUCT'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    
    def get_product(pid):
        sql ='SELECT * FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))

    def get_num(pid):
        sql = 'SELECT PNUM FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':pid}))[0]
    def get_all_product(mid):
        sql = 'SELECT * FROM PRODUCT WHERE ACCOUNT = :id'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'id': mid}))#####
    def get_all():
        sql = 'SELECT * FROM PRODUCT WHERE PNUM > 0'
        return DB.fetchall(DB.execute(DB.connect(),sql))
    def get_name(pid):
        sql = 'SELECT PNAME FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':pid}))[0]

    def get_all_name():
        sql= 'SELECT PNAME FROM PRODUCT'
        return DB.fetchall(DB.execute(DB.connect(),sql))
    
   # def get_MID_Product():
    #    sql = 'SELECT ACCOUNT FROM PRODUCT'
   #     return DB.fetchall(DB.execute(DB.connect(),sql))
    
    def add_product(input):
        sql = 'INSERT INTO PRODUCT VALUES (:pid, :name, :price, :category, :description, :num, :id, :image)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
   # def add_image(input):
   #     sql = 'INSERT INTO PRODUCT VALUES ()'
    
    
    def delete_product(pid):
        sql = 'DELETE FROM PRODUCT WHERE PID = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()

    def update_product(input):
        sql = 'UPDATE PRODUCT SET PNAME=:name, PRICE=:price, CATEGORY=:category, PDESC=:description, PNUM=:num WHERE PID=:pid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    def update_product_pnum(pid, num):
    #更新商品庫存量
        sql = 'UPDATE PRODUCT SET PNUM=:num WHERE PID=:pid'
        DB.execute_input(DB.prepare(sql), {'pid': pid, 'num': num})
        DB.commit()



    #record
class Record():
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'tno': tno}))[0]


    def get_product_sell_id(tno):
        sql = 'SELECT PRODUCT.ACCOUNT FROM PRODUCT,RECORD WHERE RECORD.PID = PRODUCT.PID AND RECORD.TNO =:id'
        return DB.fetchall(DB.execute_input(DB.prepare(sql),{'id' :tno}))

    def check_product(pid, tno):
        sql = 'SELECT * FROM RECORD WHERE PID = :id and TNO = :tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid, 'tno':tno}))

    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))[0]

    def add_product(input):
        sql = 'INSERT INTO RECORD VALUES (:id, :tno, 1, :price, :total)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = :id'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'id': tno}))

    def get_amount(tno, pid):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = :id and PID=:pid'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'id': tno, 'pid':pid}) )[0]
    
    def update_product(input):
        sql = 'UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE PID=:pid and TNO=:tno'
        DB.execute_input(DB.prepare(sql), input)

    def delete_check(pid):
        sql = 'SELECT * FROM RECORD WHERE PID=:pid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pid':pid}))

    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':tno}))[0]
    

class Order_List():
    def add_order(input):
        sql = 'INSERT INTO ORDER_LIST VALUES (null, :mid, TO_DATE(:time, :format ), :total, :tno, :way, :pay, :bankname, :bankid, :cardnumber, :safecode, :duedate, :tool, :sellerid)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()


    def get_order(input):
        sql = 'SELECT O.OID, M.NAME, O.PRICE, O.ORDERTIME FROM ORDER_LIST O, MEMBER M WHERE O.MID=M.MID AND O.SELLERID = :sno'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'sno': input}))
    
    def get_orderdetail():
        sql = 'SELECT O.OID, P.PNAME, R.SALEPRICE, R.AMOUNT ,O.WAY, O.PAYWAY FROM ORDER_LIST O, RECORD R, PRODUCT P WHERE O.TNO = R.TNO AND R.PID = P.PID'
        return DB.fetchall(DB.execute(DB.connect(), sql))


class Analysis():#這裡都有改
    def month_price(i, mid):
        sql = 'SELECT EXTRACT(YEAR FROM O.ORDERTIME), EXTRACT(MONTH FROM O.ORDERTIME), SUM(R.TOTAL) FROM ORDER_LIST O INNER JOIN RECORD R ON O.TNO = R.TNO AND O.SELLERID = :mid WHERE EXTRACT(MONTH FROM O.ORDERTIME)=:mon GROUP BY EXTRACT(YEAR FROM O.ORDERTIME), EXTRACT(MONTH FROM O.ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i,"mid": mid}))

    def month_count(i, mid):
        sql = 'SELECT EXTRACT(YEAR FROM O.ORDERTIME), EXTRACT(MONTH FROM O.ORDERTIME), COUNT(O.OID) FROM ORDER_LIST O WHERE EXTRACT(MONTH FROM O.ORDERTIME)=:mon AND O.SELLERID = :mid GROUP BY EXTRACT(YEAR FROM O.ORDERTIME), EXTRACT(MONTH FROM O.ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i,"mid": mid}))
    
    def category_sale(mid):
        sql = 'SELECT SUM(R.TOTAL), P.CATEGORY FROM PRODUCT P NATURAL JOIN RECORD R WHERE P.ACCOUNT = :mid GROUP BY CATEGORY'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mid": mid}))

    def member_sale(mid):
        sql = 'SELECT SUM(O.PRICE), M.MID, M.NAME FROM ORDER_LIST O INNER JOIN MEMBER M ON O.MID = M.MID AND O.SELLERID = :mid WHERE M.IDENTITY = :identity GROUP BY M.MID, M.NAME ORDER BY SUM(O.PRICE) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user',"mid": mid}))

    def member_sale_count(mid):
        sql = 'SELECT COUNT(*), M.MID, M.NAME FROM ORDER_LIST O INNER JOIN MEMBER M ON O.MID = M.MID AND O.SELLERID = :mid WHERE M.IDENTITY = :identity GROUP BY M.MID, M.NAME ORDER BY COUNT(*) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user',"mid": mid}))
class News():
    def get_seller_title(mid):
        sql = "SELECT TITLE FROM NEWS WHERE SELLERID = :mid"
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mid": mid}))
    
    def add_news(input):
        sql = 'INSERT INTO NEWS VALUES (:title, :content, :releasetime, :sellerid)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()
    
    def get_news():
        sql = 'SELECT N.TITLE, N.CONTENT, N.RELEASETIME, M.NAME FROM NEWS N INNER JOIN MEMBER M ON N.SELLERID = M.MID ORDER BY RELEASETIME DESC'
        return DB.fetchall(DB.execute(DB.connect(), sql))   

    def delete_check(newsname):
        sql = 'SELECT * FROM NEWS WHERE TITLE=:newsname'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'newsname':newsname}))     
    

    def get_news_data(newsname):
        sql ='SELECT * FROM NEWS WHERE TITLE = :newsname'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'newsname': newsname}))
    def delete_news(newsname):
        sql = 'DELETE FROM NEWS WHERE TITLE = :newsname '
        DB.execute_input(DB.prepare(sql), {'newsname': newsname})
        DB.commit()


    def get_all_news(mid):
        sql = 'SELECT * FROM NEWS WHERE SELLERID = :id'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'id': mid}))#####    
    
    def update_news(input):
        sql = 'UPDATE NEWS SET TITLE=:title, CONTENT=:content WHERE SELLERID=:sellerid AND RELEASETIME=:releasetime'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()