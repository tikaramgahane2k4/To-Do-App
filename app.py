from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

db = SQLAlchemy(app)


class Datas(db.Model):
    SN = db.Column(db.Integer, primary_key = True)
    Desc = db.Column(db.String(500), nullable = False)
    Status = db.Column(db.String(100), nullable = False)
    Date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str: 
        return f"{self.SN}- {self.Desc}- {self.Status}"

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":

        desc = request.form.get("tasks")

        datas = Datas(
            Desc = desc,
            Status = "Working"
        )
        
        db.session.add(datas)
        db.session.commit()

    all_data = Datas.query.all()
    return render_template('index.html', datas = all_data)

@app.route("/delete/<int:SN>")
def Delete(SN):
    dele = Datas.query.filter_by(SN=SN).first()

    db.session.delete(dele)
    db.session.commit()

    return redirect("/")

@app.route("/update/<int:SN>", methods = ["GET", "POST"])
def Update(SN):
    if request.method == "POST":

        desc = request.form.get("tasks")
        
        datas = Datas.query.filter_by(SN=SN).first()

        datas.Desc = desc
        db.session.add(datas)
        db.session.commit()
        return redirect("/")

    datas = Datas.query.filter_by(SN=SN).first()
    return render_template('update.html', datas = datas)


if __name__ == "__main__":
    app.run(debug=True)