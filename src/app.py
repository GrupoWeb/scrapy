from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import StreamListener
import tweepy, json
import streamCache


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/scrapyn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

consumer_key='gaITkllOhLp20v0jYoO94VF2C'
consumer_key_secret='CjYjIV2186FVV7qZcedSs1yvajgGSclFE4hW1uejKmyFnJMBR9'
access_token='142910198-ot2XMelum0ZVIsPQR1n4W8Rqqe2yDt46ax7yDcpQ'
access_token_secret='jzsWgrMJtEf0eWhGV6MBhQeP4Um06acNl3Hc7DNvaFfUn'
auth=tweepy.OAuthHandler(consumer_key,consumer_key_secret)
auth.set_access_token(access_token,access_token_secret)

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Schema
class Filter(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(70))
  filter = db.Column(db.String(70))


  def __init__(self, description, filter):
      self.description = description
      self.filter = filter

db.create_all()

class FilterSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description','filter')

filter_schema = FilterSchema()
filter_schema = FilterSchema(many=True)

# Route API
@app.route('/scrapyn', methods=['GET'])
def conectionPool():
    listener = StreamListener.MyStreamListener(tweepy.StreamListener)
    cache = streamCache.cachePool.Stream(auth,listener)
    return 'ok'

@app.route('/scrapy-list', methods=['POST'])
def create_filter():
    description = request.json[0]['description']
    filter = request.json[1]['filter']
    new_filter = FilterSchema(description= description, filter= filter)
    return request.json[1]['filter']
    # db.session.add(new_filter)
    # db.session.commit()

    # return FilterSchema.jsonify(new_filter)




















    
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