from flask import Flask, render_template, url_for, flash, request, redirect, session, jsonify
from models import User, Task, Status, History, TaskSubmission, db
from config import *
from sqlalchemy import func
from functools import wraps
from datetime import datetime


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first!", "error")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if not name or not password or not confirm_password:
            flash("All fields are required!", "error")
            return render_template('register.html')
        
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return render_template('register.html')
        
        if len(password) < 4:
            flash("Password must be at least 4 characters!", "error")
            return render_template('register.html')
        
        existing_user = User.query.filter_by(name=name).first()
        if existing_user:
            flash("Username already exists!", "error")
            return render_template('register.html')
        
        new_user = User(name=name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please login.", "success")
        return redirect('/login')
    
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        
        if not name or not password:
            flash("All fields are required!", "error")
            return render_template('login.html')
        
        user = User.query.filter_by(name=name).first()
        
        if not user or not user.check_password(password):
            flash("Invalid username or password!", "error")
            return render_template('login.html')
        
        session['user_id'] = user.id
        session['user_name'] = user.name
        flash(f"Welcome, {user.name}!", "success")
        return redirect('/')
    
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out!", "success")
    return redirect('/login')

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        flash("Please login first!", "error")
        return redirect('/login')
    
    if request.method == "POST":

        desc = request.form.get("tasks")
        status = request.form.get("status", "Pending")
        
        if not desc:
            flash("Task description cannot be empty!", "error")
            all_data = Task.query.filter_by(user_id=session['user_id']).all()
            return render_template('index.html', datas = all_data)

        task = Task(
            tasks = desc,
            status = status,
            user_id = session['user_id']
        )
        
        db.session.add(task)
        db.session.commit()
        flash("Task added successfully!", "success")

    # Show only unsubmitted tasks
    all_data = Task.query.filter_by(user_id=session['user_id'], is_submitted=False).all()
    return render_template('index.html', datas = all_data)

@app.route("/delete/<int:id>")
def Delete(id):
    if 'user_id' not in session:
        flash("Please login first!", "error")
        return redirect('/login')
    
    dele = Task.query.filter_by(id=id, user_id=session['user_id']).first()
    
    if not dele:
        flash("Task not found!", "error")
        return redirect("/")

    db.session.delete(dele)
    db.session.commit()
    flash("Task deleted successfully!", "success")

    return redirect("/")

@app.route("/update/<int:id>", methods = ["GET", "POST"])
def Update(id):
    if 'user_id' not in session:
        flash("Please login first!", "error")
        return redirect('/login')
    
    task = Task.query.filter_by(id=id, user_id=session['user_id']).first()
    
    if not task:
        flash("Task not found!", "error")
        return redirect("/")
    
    if request.method == "POST":

        desc = request.form.get("tasks")
        status = request.form.get("status")
        
        if not desc:
            flash("Task description cannot be empty!", "error")
            return render_template('update.html', datas = task)

        task.tasks = desc
        task.status = status
        db.session.add(task)
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect("/")

    return render_template('update.html', datas = task)

@app.route("/submit/<int:id>", methods=['POST'])
def submit_task(id):
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Please login first!"})
    
    task = Task.query.filter_by(id=id, user_id=session['user_id']).first()
    
    if not task:
        return jsonify({"success": False, "message": "Task not found!"})
    
    if task.is_submitted:
        return jsonify({"success": False, "message": "Task already submitted!"})
    
    if task.status != "Completed":
        return jsonify({"success": False, "message": "Only Completed tasks can be submitted!"})
    
    try:
        # Mark task as submitted
        task.is_submitted = True
        task.submitted_at = datetime.now()
        
        # Create submission record in history
        submission = TaskSubmission(
            task_id=task.id,
            user_id=session['user_id'],
            task_name=task.tasks,
            status=task.status
        )
        
        db.session.add(submission)
        db.session.commit()
        
        return jsonify({"success": True, "message": "Task submitted successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route("/history")
def history():
    if 'user_id' not in session:
        flash("Please login first!", "error")
        return redirect('/login')
    
    submissions = TaskSubmission.query.filter_by(user_id=session['user_id']).order_by(TaskSubmission.submitted_at.desc()).all()
    
    return render_template('history.html', submissions=submissions)


if __name__ == "__main__":
    with app.app_context():
        # Only create tables if they don't exist
        db.create_all()
        print("✓ Database tables ready")
    app.run(debug=True)