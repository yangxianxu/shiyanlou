from flask import Flask,render_template
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    target_dir = '/home/shiyanlou/files/'
    articles = []
    num = 0
    target_list = os.listdir(target_dir)
    for tar_file in target_list:
        with open(target_dir+tar_file) as file:
            article = json.loads(file.read())
            articles.append(article['title'])
            num += 1
    return render_template('index.html',articles=articles,num=num)


@app.route('/files/<filename>')
def file(filename):
    article = {}
    path = '/home/shiyanlou/files/'+filename+'.json'
    print(path)
    if os.path.exists(path):
        with open(path,'r') as file:
            article = json.loads(file.read())
            print(article)
        return render_template('file.html',article=article)
    else:
        #abort(404)
        pass

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
