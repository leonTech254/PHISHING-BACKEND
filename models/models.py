from datetime import datetime
from models.db import db


class SsmpUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    phoneNumber = db.Column(db.String(100), unique=True)
    DeviceCode = db.Column(db.String(100), default="user")
    image = db.Column(db.String(100), default="false")
    dateJoined = db.Column(db.String(100), default=datetime.utcnow())

    def __init__(self, username, phone, DeviceCode):
        self.username = username
        self.phoneNumber = phone
        self.DeviceCode = DeviceCode


class MailPhishingDetector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    sender = db.Column(db.String(100))
    flaged = db.Column(db.String(100))

    def __init__(self, mail, subject, receiver, sender, flaged):
        self.mail = mail
        self.subject = subject
        self.receiver = receiver
        self.sender = sender
        self.flaged = flaged
