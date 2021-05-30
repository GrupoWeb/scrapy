from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mysqldb import MySQL
import StreamListener
import tweepy, json
import streamCache

# llamada a la api
consumer_key='gaITkllOhLp20v0jYoO94VF2C'
consumer_key_secret='CjYjIV2186FVV7qZcedSs1yvajgGSclFE4hW1uejKmyFnJMBR9'
access_token='142910198-ot2XMelum0ZVIsPQR1n4W8Rqqe2yDt46ax7yDcpQ'
access_token_secret='jzsWgrMJtEf0eWhGV6MBhQeP4Um06acNl3Hc7DNvaFfUn'
auth=tweepy.OAuthHandler(consumer_key,consumer_key_secret)
auth.set_access_token(access_token,access_token_secret)

# config app
app = Flask(__name__)
# config Mysql
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'scrapyn'
mysql = MySQL(app)
CORS(app)

app.secret_key = "mysecretkey"

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# Route API
@app.route('/categorie', methods=['POST'])
def setCategories():
    name = request.json['name']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO categories (name,status_id) VALUES (%s,1)", [name])
    mysql.connection.commit()
    return 'ok'

@app.route('/categories', methods=['GET'])  
def getCategories():
    listFilter = mysql.connection.cursor()
    listFilter.execute('SELECT id as code, name  FROM categories WHERE status_id = 1')
    data = listFilter.fetchall()
    row_headers=[x[0] for x in listFilter.description] 
    filterList = []
    print(type(row_headers))
    for result in data:
        filterList.append(dict(zip(row_headers,result)))
    listFilter.close()
    return json.dumps(filterList)

@app.route('/categoriesD', methods=['POST'])   
def deleteCategorie():
    id = request.json['id']
    listFilter = mysql.connection.cursor()
    listFilter.execute('UPDATE categories SET status_id = 2 WHERE id = %s', [id])
    mysql.connection.commit()
    return 'ok'

@app.route('/product', methods=['POST'])
def setProduct():
    name = request.json['name']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO products (name,status_id) VALUES (%s,1)", [name])
    mysql.connection.commit()
    return 'ok'

@app.route('/products', methods=['GET'])  
def getProducts():
    listFilter = mysql.connection.cursor()
    listFilter.execute('SELECT id as code, name  FROM products WHERE status_id = 1')
    data = listFilter.fetchall()
    row_headers=[x[0] for x in listFilter.description] 
    filterList = []
    for result in data:
        filterList.append(dict(zip(row_headers,result)))
    listFilter.close()
    return json.dumps(filterList)

@app.route('/productD', methods=['POST'])   
def deleteProduct():
    id = request.json['id']
    listFilter = mysql.connection.cursor()
    listFilter.execute('UPDATE products SET status_id = 2 WHERE id = %s', [id])
    mysql.connection.commit()
    return 'ok'

@app.route('/search', methods=['POST'])
def setSearch():
    name = request.json['name']
    categorie = request.json['categorie']
    products = request.json['products']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO search_masters (name) VALUES (%s)", [name])
    mysql.connection.commit()
    cur.execute('select id from search_masters where name = %s', [name])
    data = cur.fetchall()
    row_headers=[x[0] for x in cur.description] 
    filterList = []
    for result in data:
        filterList.append(dict(zip(row_headers,result)))
    id_data = filterList[0]['id']
    for item in products:
        cur.execute('INSERT INTO search_items (master_id, categories_id, products_id, status_id) VALUES(%s,%s,%s,1)', [int(id_data), int(categorie), int(item)])
        mysql.connection.commit()
    return 'ok'

@app.route('/search', methods=['GET'])
def getSearch():
    listFilter = mysql.connection.cursor()
    listFilter.execute('SELECT id as code, name FROM search_masters')
    data = listFilter.fetchall()
    row_headers=[x[0] for x in listFilter.description] 
    filterList = []
    for result in data:
        filterList.append(dict(zip(row_headers,result)))
    listFilter.close()
    return json.dumps(filterList)


@app.route('/scrapyn', methods=['POST'])   
def conectionPool():
    master_id = request.json['master_id']
    listFilter = mysql.connection.cursor()
    listFilter.execute('SELECT p.name FROM search_items sit INNER JOIN products p ON sit.products_id = p.id WHERE master_id = %s',[master_id])
    data = listFilter.fetchall()
    filterList = []
    row_headers = ['name','count']
    json_data = []
    for result in data:
        filterList.append(result[0])
        count_data = []
        for tweet in api.search(q=result[0], lang="en", rpp=100):
            count_data.append(f"{tweet.user.name}:{tweet.text}")
            tuplas = (result[0],len(count_data))
        json_data.append(dict(zip(row_headers,tuplas)))
    listFilter.close()
    return jsonify(json_data)

    # json_response = []
    # json_data = []
    # filter="juan"
    
    # for tweet in tweepy.Cursor(api.search, q='ferreteria', tweet_mode="extended").items(10):
    #     json_response.append(tweet._json)
        # json_response.append({ 'user' : tweet._json['user']})
    # for tweet in api.search(q=filter, lang="en", rpp=100):
    #     json_response.append(f"{tweet.user.name}:{tweet.text}")

    # json_data.append(json.dumps({ 'item' : filter, 'count' : len(json_response)}))
    # json_data.append(dict(zip(header_data,filter)))
    # print(len(json_response))
    # return 'ok'

@app.route('/listas', methods=['GET'])   
def searchPool():
    filter = ['mazda','toyota']
    resultado = StreamListener.MyStreamListener()
    cache = streamCache.cachePool.Stream(auth, resultado,filter)
    print(cache)
    json_response = []
    for item in cache:
        json_response.append({ 'user' : item})
    # return jsonify(json_response)
    return jsonify(json_response)

@app.route('/scrapy-list', methods=['POST'])
def create_filter():
    description = request.json[0]['description']
    filter = request.json[1]['filter']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO filter (description, filter) VALUES (%s,%s)", (description, filter))
    mysql.connection.commit()
    return 'ok'

@app.route('/getIntelligence', methods=['GET'])
def intelligence():
    cursor = mysql.connection.cursor()
    SQL = 'SELECT id as code, name FROM search_masters'
    cursor.execute(SQL)
    data = cursor.fetchall()
    response_data = []
    row_headers=[x[0] for x in cursor.description] 
    
    for item in data:
        response_data.append(dict(zip(row_headers,item)))
    return json.dumps(response_data)


if __name__ == "__main__":
    app.run(debug=True)