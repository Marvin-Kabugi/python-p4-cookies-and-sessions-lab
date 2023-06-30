#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles_dict = [article.to_dict() for article in Article.query.all()]
    print(articles_dict)
    
    return make_response(jsonify(articles_dict), 200)
    

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views') or 0
    
    article_dict = Article.query.filter_by(id=id).first().to_dict()

    if session.get('page_views') <= 2:
        response = make_response(jsonify({'article':article_dict, 'cookies':[{cookie: request.cookies[cookie]} for cookie in request.cookies]}), 200)
        session['page_views'] += 1
        return response
    else:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401
    
if __name__ == '__main__':
    app.run(port=5555)
