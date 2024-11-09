from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import mysql.connector

app = Flask(__name__, static_folder='static', template_folder='templates')

# Flask-Mail configuration for Gmail
app.config['MAIL_SERVER'] = 'live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = 'cfdd98ab36199f07e3070bfe64edc5bd'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Initialize Flask-Mail
mail = Mail(app)

# Database connection configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'r!$h!t0801',
    'database': 'HOSPITALS'
}

# Home route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dr._anjali_reddy')
def dr_anjali_reddy():
    return render_template('dr._anjali_reddy.html')

@app.route('/Rohit_A.html')
def dr_aarti_malhotra():
    return render_template('Rohit_A.html')


@app.route('/dr_dr._karan_gupta.html')
def dr_karan_gupta():
    return render_template('dr_karan_gupta.html')

@app.route('/dr_dr._kavita_pandey.html')
def dr_kavita_pandey():
    return render_template('dr_kavita_pandey.html')

@app.route('/dr_dr._rakesh_jain.html')
def dr_rakesh_jain():
    return render_template('dr_rakesh_jain.html')

@app.route('/dr_dr._vandana_joshi.html')
def dr_vandana_joshi():
    return render_template('dr_vandana_joshi.html')



# Route to send email notification after booking
@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    selected_date = data.get('date')
    selected_time = data.get('time')

    if not selected_date or not selected_time:
        return jsonify({'status': 'error', 'message': 'Date or time not provided.'})

    # Prepare the email message
    msg = Message(
        'Booking Confirmed',  # Subject of the email
        sender='hi@demomailtrap.com',  # Your email address
        recipients=['resqservices12@gmail.com']  # Replace with the recipient's email address
    )
    msg.body = f'Your booking with the doctor has been confirmed for {selected_date} at {selected_time}.For further queries kindly contact us via our Customer support Email: resqservices12@gmail.com  or  Phone number:- +9198203840274 '

    try:
        # Send the email
        mail.send(msg)
        return jsonify({'status': 'success', 'message': 'Email has been sent!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# API route to search doctors by specialization, hospital, and sort by rating
@app.route('/api/doctors', methods=['GET'])
def search_doctors():
    specialization = request.args.get('specialization')
    hospital_name = request.args.get('hospital')  # Original variable name
    sort_by_rating = request.args.get('sort_by_rating')  # Original variable name

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Build the query based on the parameters
    query = "SELECT doctor_name, hospital_name, rating FROM doctors WHERE 1=1"
    params = []

    # Add conditions based on the parameters
    if specialization:
        query += " AND speciality = %s"
        params.append(specialization)
    
    if hospital_name:  # Filter based on hospital name
        query += " AND hospital_name = %s"
        params.append(hospital_name)
    
    # Apply sorting if requested
    if sort_by_rating == 'true':  # Sort by rating if specified
        query += " ORDER BY rating DESC"

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
# Close the connection
    cursor.close()
    conn.close()

    # Return results as JSON
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)