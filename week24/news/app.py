from flask import Flask,render_template
import json
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/app'
db = SQLAlchemy(app)

client = MongoClient('127.0.0.1',27017)
mdb = client.app1

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    content = db.Column(db.Text)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('files', lazy='dynamic'))
    #tags = []

    def __init__(self, title, category, content):
        self.title = title
        created_time = datetime.utcnow()
        self.category = category
        self.content = content
        #self.tags = []

    def __repr__(self):
        return '<File %r>' % self.title

    def add_tag(self, tag_name):
        mfile = mdb.mfile.find_one({'title':self.title})
        #print(mfile)
        if not mfile:
            tags = self.tags
            tags.append(tag_name)
            mfile = {'title':self.title,'tags':tags}
            mdb.mfile.insert_one(mfile)
        elif not mfile['tags']:
            tags = self.tags
            tags.append(tag_name)
            mdb.mfile.update_one({'title':self.title},{'$set':{'tags':tags}})
        else:
            tags = mfile['tags']
            if tag_name in mfile['tags']:
                pass
            else:
                tags.append(tag_name)
                mdb.mfile.update_one({'title':self.title},{'$set':{'tags':tags}})

    def remove_tag(self, tag_name):
        mfile = mdb.mfile.find_one({'title':self.title})
        if tag_name in mfile['tags']:
            tags = mfile['tags']
            print(tags)
            #tags_new = tags.remove(tag_name)
            tags.remove(tag_name)
            print(tags)
            mdb.mfile.update_one({'title':self.title},{'$set':{'tags':tags}})
        else:
            pass

    @property
    def tags(self):
        mfile = mdb.mfile.find_one({'title':self.title})
        if not mfile:
            tags = []
            return tags
        elif not mfile['tags']:
            tags =[]
            return tags
        else:
            tags = mfile['tags']
            return tags

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

@app.route('/')
def index():
    target_dir = '/home/shiyanlou/files/'
    articles = File.query.all()
    return render_template('index.html',articles=articles)


@app.route('/files/<file_id>')
def file(file_id):
    article = File.query.filter_by(id=file_id).first()
    if not article:
        abort(404)
    else:
        return render_template('file.html',article=article)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
