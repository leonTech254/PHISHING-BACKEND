from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail
import os
import logging
from models.db import db
from dotenv import load_dotenv
from models.models import MailPhishingDetector
from ML.process import ProcessData

load_dotenv()
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("mysql_path")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# app.config.from_pyfile("config.py")
# mail = Mail(app)


app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resorces={r'/*': {"orgins": '*'}})


@app.route("/")
def home():
    return "hello world"


@app.route("/api/send/mail", methods=['GET', 'POST'])
def send_mail():
    if request.method == 'POST':
        data = request.get_json()
        mail = data['mail']
        subject = data['subject']
        receiver = data['receiver']
        sender = data['from']
        checkFlag=ProcessData.messages(email=mail)
        print(checkFlag)    
        data = MailPhishingDetector(
            mail=mail, subject=subject, receiver=receiver, sender=sender, flaged=checkFlag)
        db.session.add(data)
        db.session.commit()

        print(data)

    return "hello world"

@app.route("/api/fetch/mail", methods=['GET', 'POST'])
def fetch_mail():
    content=request.get_json()
    email=content['email']
    query_result = MailPhishingDetector.query.filter_by(receiver=email).all()
    # loop through the query result and print the email and subject for each record
    result=[]
    for message in query_result:
        email_dict = {
        'email': message.mail,
        'receiver': message.receiver,
        'name': message.subject ,
        'flag':message.flaged,
        'subject':message.subject
    }
    result.append(email_dict)
    return jsonify({'emails':result})
    
    
    



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(host="0.0.0.0", port=5001, debug=True)
