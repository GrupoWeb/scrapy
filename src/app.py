from flask import Flask, request, jsonify
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

app.secret_key = "mysecretkey"

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# Route API
@app.route('/scrapyn/<filtro>', methods=['GET'])   
def conectionPool(filtro):
    listFilter = mysql.connection.cursor()
    listFilter.execute('SELECT description FROM filter WHERE filter = "auto"')
    data = listFilter.fetchall()
    filterList = []
    for result in data:
        filterList.append(result[0])
    listFilter.close()
    json_response = []
    for tweet in tweepy.Cursor(api.search, q=filtro, tweet_mode="extended").items(10):
        json_response.append({ 'user' : tweet._json['user']})
    return jsonify(json_response)

@app.route('/scrapy-list', methods=['POST'])
def create_filter():
    description = request.json[0]['description']
    filter = request.json[1]['filter']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO filter (description, filter) VALUES (%s,%s)", (description, filter))
    mysql.connection.commit()
    return 'ok'



















    
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result =tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json[0]['title']

    task.title  = title
    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)


if __name__ == "__main__":
    app.run(debug=True)