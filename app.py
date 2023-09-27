# App Entry Point
from flask import Flask, render_template, request, redirect, url_for
import psycopg2, os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():

    if request.method == 'POST':
        # Retrieve form data
        activity1 = request.form.get('activity1')
        activity2 = request.form.get('activity2')


    # Heroku Postgres Databse URl
    DATABASE_URL = os.environ.get('DATABASE_URL')

    #Connecting to Heroku Postgres
    postgresConn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # Connecting to SQLite Server
    # sqlConnection = sqlite3.connect('activityList.db')

    cursor = postgresConn.cursor()

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
        postgresConn.commit()
    except Exception as e:
        postgresConn.rollback()  # Rollback changes if an exception occurs
        print(f"Error: {str(e)}")
    finally:
        cursor.close()
        postgresConn.close()


    print(f"Inserted data: activity1={activity1}, activity2={activity2}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)