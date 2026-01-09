from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    tasks = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="Pending")
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_submitted = db.Column(db.Boolean, default=False)
    submitted_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    user = db.relationship("User", backref = "tasks")
    submissions = db.relationship("TaskSubmission", backref="task", cascade="all, delete-orphan")

class TaskSubmission(db.Model):
    __tablename__ = "task_submission"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    task_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship("User", backref="submissions")

class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(50))
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))

    task = db.relationship("Task", backref="statuses")

class History(db.Model):
    __tablename__ = "task_history"
    id = db.Column(db.Integer, primary_key=True)
    history_name = db.Column(db.String(50))
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"))

    status = db.relationship("Status", backref = "task_histories")
