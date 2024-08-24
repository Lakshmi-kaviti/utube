import pickle
import sqlite3
from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/contact',methods = ["GEt","POST"])
def contactus():
    if request.method=="POST":
        fname = request.form.get("name")
        pno = request.form.get("phone")
        email = request.form.get('email')
        add = request.form.get("address")
        msg = request.form.get("message")
        conn=sqlite3.connect('ytdatabase.db')
        cur = conn.cursor()
        cur.execute(f''' insert into contact values("{fname}","{pno}","{email}","{add}","{msg}") ''')
        conn.commit()
        return render_template("message.html")
    else:
        return render_template("contactus.html")

@app.route('/analytical')
def analytical():
    return render_template("Analytical.html")

@app.route('/predict',methods =['GET', 'POST'])
def likepredict():
    if request.method == 'POST':
        views = request.form.get('views')
        dislikes = request.form.get('dislikes')
        comment = request.form.get('comments')
        genre = request.form.get('genre')
        print(views, dislikes, comment, genre)

        with open("model.pkl",'rb') as mod:
            model = pickle.load(mod)
        pred = model.predict([[float(views),float(dislikes),float(comment),float(genre)]])
        return render_template('results.html', pred = str(round(pred[0])))
    else:
        return render_template('likepredict.html')

if __name__ == '__main__':
    app.run()

