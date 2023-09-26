# App Entry Point
from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():

    if request.method == 'POST':
        # Retrieve form data
        activity1 = request.form['activity1']
        activity2 = request.form['activity2']

    # Connecting to SQLite Server
    sqlConnection = sqlite3.connect('activityList.db')
    cursor = sqlConnection.cursor()

    # Create a table if one does not exist
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS user_data (
                   id INTEGER PRIMARY KEY,
                   activity1 TEXT,
                   activity2 TEXT
                   )
                   ''')

    try:
        # Insert Data into database 
        cursor.execute('INSERT INTO user_data (activity1, activity2) VALUES (?,?)',(activity1, activity2))
        sqlConnection.commit()
    except Exception as e:
        sqlConnection.rollback()  # Rollback changes if an exception occurs
        print(f"Error: {str(e)}")
    finally:
        sqlConnection.close()


    print(f"Inserted data: activity1={activity1}, activity2={activity2}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)