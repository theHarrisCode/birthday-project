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
    # DATABASE_URL = os.environ.get('DATABASE_URL')

    # #Connecting to Heroku Postgres
    # postgresConn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # Connecting to SQLite Server
    # sqlConnection = sqlite3.connect('activityList.db')

    # Heroku Postgres Database URL
    DATABASE_URL = os.environ.get('DATABASE_URL')

    # Construct the dsn (data source name) in the expected format
    dsn = f"dbname={DATABASE_URL.path[1:]} user={DATABASE_URL.username} " \
          f"password={DATABASE_URL.password} host={DATABASE_URL.hostname} " \
          f"port={DATABASE_URL.port} sslmode=require"

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