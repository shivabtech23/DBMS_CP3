from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database configuration (adjust as necessary)
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'r!$h!t0801',
    'database': 'HOSPITALS'
}

# Endpoint to fetch doctor data based on specialization and render HTML
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    specialization = request.args.get('specialization')
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT doctor_name, hospital_name, rating 
    FROM doctors 
    WHERE speciality = %s
    """
    cursor.execute(query, (specialization,))
    doctors = cursor.fetchall()

    cursor.close()
    connection.close()
    
    # Render the results in anjali_cardiologist.html
    return render_template('anjali_cardiologist.html', doctors=doctors)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
