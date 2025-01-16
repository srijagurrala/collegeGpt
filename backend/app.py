from flask import Flask, render_template, request, redirect, url_for, session
from pdf_processing import create_search_index
from search_model import search

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Create the search index directory
create_search_index('data/indexdir')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/clubs')
def clubs():
    return render_template('clubs.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        # Logic to save user data (e.g., store in a database)

        # Set the session variable to indicate the user has signed up
        session['authenticated'] = True
        
        # Redirect to the landing page or show a confirmation message
        return render_template('email.html', username=username)

    return render_template('signup.html')

@app.route('/landingpage', methods=['GET', 'POST'])
def landingpage():
    user_authenticated = session.get('authenticated', False)  # Check if the user is authenticated
    default_query = "Who is principal"
    # default_query = "Faculty of CSE"
    if request.method == 'POST':
        query = request.form['query']
        results = search(query)
        return render_template('landingpage.html', results=results, user_authenticated=user_authenticated)
    
    return render_template('landingpage.html', results=None, user_authenticated=user_authenticated)

if __name__ == '__main__':
    app.run(debug=True)
