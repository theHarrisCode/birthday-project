# App Entry Point
from flask import Flask, render_template, request, redirect, url_for
import psycopg2, os
from urllib.parse import urlparse

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
    # DATABASE_URL = os.environ.get('DATABASE_URL')

    # #Connecting to Heroku Postgres
    # postgresConn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # Connecting to SQLite Server
    # sqlConnection = sqlite3.connect('activityList.db')

    DATABASE_URL = os.environ.get('DATABASE_URL')

    # Parse the DATABASE_URL to extract components
    url = urlparse(DATABASE_URL)
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    # Construct the dsn (data source name) in the expected format
    dsn = f"dbname={dbname} user={user} password={password} host={host} port={port} sslmode=require"

    # Create the database connection
    postgresConn = psycopg2.connect(dsn)

    cursor = postgresConn.cursor()

    # Create a table if one does not exist
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS user_data (
                   activity1 TEXT,
                   activity2 TEXT
                   )
                   ''')

    try:
        # Insert Data into database 
        cursor.execute('INSERT INTO user_data (activity1, activity2) VALUES (%s,%s)',(activity1, activity2))

        cursor.execute('SELECT * FROM user_data')
        rows = cursor.fetchall()

        for i in rows:
            print(i)


        postgresConn.commit()
    except Exception as e:
        postgresConn.rollback() # Rollback changes if an exception occurs
        print(f"Error: {str(e)}")
    finally:
        cursor.close()
        postgresConn.close()


    print(f"Inserted data: activity1={activity1}, activity2={activity2}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)