from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_jobs.db'
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)

@app.route('/search', methods=['GET'])
def job_search():
    title = request.args.get('title')
    location = request.args.get('location')
    
    jobs = Job.query.filter(Job.title.like(f'%{title}%'), Job.location.like(f'%{location}%')).all()
    
    return render_template('search_results.html', jobs=jobs)

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        description = request.form['description']

        job = Job(title=title, company=company, location=location, description=description)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_job.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
