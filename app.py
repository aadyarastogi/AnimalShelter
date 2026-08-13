import mysql.connector
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
import json
import decimal
import datetime

# --- 1. SETUP ---

app = Flask(__name__, static_folder='.', template_folder='.')

db_config = {
    'host': 'localhost',
    'user': 'root',                # Your user
    'password': 'aadya123',        # Your password
    'database': 'animalshelter'
}

# This is a placeholder for a real login system.
# All volunteer pages will show data for Volunteer ID 1.
CURRENT_VOLUNTEER_ID = 1

# Function to get a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# Helper function to format MySQL data (like dates and decimals) for JSON
def default_converter(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, decimal.Decimal):
        return float(o)

# --- 2. JAVASCRIPT FILE ROUTES (12 Routes) ---
# Serves all your .js files

@app.route('/admin_dashboard.js')
def serve_admin_dashboard_js():
    return send_from_directory('.', 'admin_dashboard.js')
@app.route('/admin_users.js')
def serve_admin_users_js():
    return send_from_directory('.', 'admin_users.js')
@app.route('/admin_finances.js')
def serve_admin_finances_js():
    return send_from_directory('.', 'admin_finances.js')
@app.route('/admin_events.js')
def serve_admin_events_js():
    return send_from_directory('.', 'admin_events.js')
@app.route('/staff_dashboard.js')
def serve_staff_dashboard_js():
    return send_from_directory('.', 'staff_dashboard.js')
@app.route('/staff_animals.js')
def serve_staff_animals_js():
    return send_from_directory('.', 'staff_animals.js')
@app.route('/staff_adoptions.js')
def serve_staff_adoptions_js():
    return send_from_directory('.', 'staff_adoptions.js')
@app.route('/staff_donations.js')
def serve_staff_donations_js():
    return send_from_directory('.', 'staff_donations.js')
@app.route('/staff_health.js')
def serve_staff_health_js():
    return send_from_directory('.', 'staff_health.js')
@app.route('/volunteer_dashboard.js')
def serve_volunteer_dashboard_js():
    return send_from_directory('.', 'volunteer_dashboard.js')
@app.route('/volunteer_profile.js')
def serve_volunteer_profile_js():
    return send_from_directory('.', 'volunteer_profile.js')
    
# This serves the new JS file for the profile page
@app.route('/animal_profile.js')
def serve_animal_profile_js():
    return send_from_directory('.', 'animal_profile.js')


# --- 3. HTML PAGE ROUTES (15 Routes now) ---
# Serves all your .html pages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/volunteer_dashboard.html')
def volunteer_dashboard():
    return render_template('volunteer_dashboard.html')

@app.route('/volunteer_profile.html')
def volunteer_profile():
    return render_template('volunteer_profile.html')

@app.route('/staff_dashboard.html')
def staff_dashboard():
    return render_template('staff_dashboard.html')

@app.route('/staff_animals.html')
def staff_animals():
    return render_template('staff_animals.html')

@app.route('/staff_adoptions.html')
def staff_adoptions():
    return render_template('staff_adoptions.html')

@app.route('/staff_donations.html')
def staff_donations():
    return render_template('staff_donations.html')

@app.route('/staff_health.html')
def staff_health():
    return render_template('staff_health.html')

# --- Routes for the "Add" forms ---
@app.route('/add_animal.html')
def add_animal_page():
    return render_template('add_animal.html')

@app.route('/add_adoption.html')
def add_adoption_page():
    return render_template('add_adoption.html')
    
# --- (FIX) These routes were missing ---
@app.route('/add_treatment.html')
def add_treatment_page():
    return render_template('add_treatment.html')

@app.route('/add_checkup.html')
def add_checkup_page():
    return render_template('add_checkup.html')
# ---------------------------------

@app.route('/animal_profile.html')
def animal_profile_page():
    return render_template('animal_profile.html')

@app.route('/admin_dashboard.html')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin_users.html')
def admin_users():
    return render_template('admin_users.html')

@app.route('/admin_finances.html')
def admin_finances():
    return render_template('admin_finances.html')

@app.route('/admin_events.html')
def admin_events():
    return render_template('admin_events.html')


# --- 4. LOGIN ROUTE ---
# This route is optional, used by the "Login" button.
# The demo buttons (e.g., "Login as Admin") bypass this.
@app.route('/login', methods=['POST'])
def login():
    # --- START DEBUGGING ---
    print("\n--- LOGIN ATTEMPT ---")
    
    try:
        username = request.form['username']
        password = request.form['password']
        print(f"Form data received: Username='{username}', Password='{password}'")
        
        conn = get_db_connection()
        if not conn:
            print("Login Error: Database connection failed.")
            return "Database connection failed", 500
            
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT Role, PasswordHash FROM UserLogin WHERE Username = %s"
        print(f"Executing query: {query} with username: {username}")
        
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            print(f"SUCCESS: User found. Role: {user['Role']}")
            # Password check would go here in a real app
            
            role = user['Role']
            
            if role == 'Admin':
                print("Redirecting to: admin_dashboard")
                return redirect(url_for('admin_dashboard'))
            elif role == 'Staff':
                print("Redirecting to: staff_dashboard")
                return redirect(url_for('staff_dashboard'))
            elif role == 'Volunteer':
                print("Redirecting to: volunteer_dashboard")
                return redirect(url_for('volunteer_dashboard'))
            else:
                print("Login Error: User has unknown role.")
                return redirect(url_for('index'))
                
        else:
            print("LOGIN FAILED: User not found in database.")
            return redirect(url_for('index'))
            
    except Exception as e:
        print(f"--- !!! LOGIN ERROR !!! ---")
        print(f"An exception occurred: {e}")
        print("--- END OF ERROR ---")
        return redirect(url_for('index'))


# --- 5. API DATA ROUTES (FOR JAVASCRIPT) ---
# These routes provide the data to your JS files.

@app.route('/api/admin/stats')
def api_admin_stats():
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT SUM(DonationAmount) as total_donations FROM donation")
    donations = cursor.fetchone()['total_donations'] or 0
    cursor.execute("SELECT SUM(Amount) as total_expenses FROM expense")
    expenses = cursor.fetchone()['total_expenses'] or 0
    cursor.execute("SELECT COUNT(StaffID) as total_staff FROM staff")
    staff = cursor.fetchone()['total_staff'] or 0
    cursor.execute("SELECT COUNT(VolunteerID) as total_volunteers FROM volunteer")
    volunteers = cursor.fetchone()['total_volunteers'] or 0
    cursor.execute("SELECT SUM(FundsRaised) as total_event_funds FROM event")
    event_funds = cursor.fetchone()['total_event_funds'] or 0
    conn.close()
    stats = {
        "donations": f"₹{donations:,.0f}",
        "expenses": f"₹{expenses:,.0f}",
        "staff": staff,
        "volunteers": volunteers,
        "event_funds": f"₹{event_funds:,.0f}",
        "net_month": f"₹{donations - expenses:,.0f}"
    }
    return jsonify(stats)
@app.route('/api/admin/expense-breakdown')
def api_expense_breakdown():
    query = "SELECT ExpenseType, SUM(Amount) as Total FROM expense GROUP BY ExpenseType"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = {"labels": [], "data": []}
    for row in results:
        data["labels"].append(row['ExpenseType'])
        data["data"].append(row['Total'])
    return json.dumps(data, default=default_converter)
@app.route('/api/admin/monthly-expenses')
def api_monthly_expenses():
    query = "SELECT MONTHNAME(ExpenseDate) as Month, SUM(Amount) as Total FROM expense WHERE ExpenseDate >= DATE_SUB(NOW(), INTERVAL 6 MONTH) GROUP BY MONTH(ExpenseDate), MONTHNAME(ExpenseDate) ORDER BY MONTH(ExpenseDate)"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = {"labels": [], "data": []}
    for row in results:
        data["labels"].append(row['Month'])
        data["data"].append(row['Total'])
    return json.dumps(data, default=default_converter)

@app.route('/api/admin/all-users')
def api_all_users():
    # This query is now simpler and only gets data from userlogin
    query = "SELECT Username, Role FROM userlogin"
    
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()
    
    # Format data for JS (no 'full_name' needed)
    data = []
    for user in users:
        data.append({
            "username": user['Username'],
            "role": user['Role']
        })
    return jsonify(data)

@app.route('/api/admin/recent-expenses')
def api_recent_expenses():
    query = "SELECT e.ExpenseID, e.ExpenseType, e.Amount, e.ExpenseDate, s.Name FROM expense e LEFT JOIN staff s ON e.StaffID = s.StaffID ORDER BY e.ExpenseDate DESC LIMIT 10"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({
            "id": row['ExpenseID'],
            "type": row['ExpenseType'],
            "amount": row['Amount'],
            "date": row['ExpenseDate'].isoformat(),
            "staff_name": row['Name'] or "N/A"
        })
    return json.dumps(data, default=default_converter)
@app.route('/api/admin/all-events')
def api_all_events():
    query = "SELECT ev.EventName, ev.EventDate, s.Name, ev.FundsRaised FROM event ev LEFT JOIN staff s ON ev.StaffID = s.StaffID ORDER BY ev.EventDate DESC"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({
            "name": row['EventName'],
            "date": row['EventDate'].isoformat(),
            "staff_name": row['Name'] or "N/A",
            "funds_raised": row['FundsRaised'] or 0
        })
    return json.dumps(data, default=default_converter)
@app.route('/api/staff/stats')
def api_staff_stats():
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(AnimalID) as count FROM animal WHERE Status != 'Adopted'")
    animals_onsite = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(AdoptionID) as count FROM adoption WHERE AdoptionDate >= DATE_SUB(NOW(), INTERVAL 1 MONTH)")
    pending_adoptions = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(RecordID) as count FROM animalhealthrecord WHERE NextVisit = CURDATE()")
    checkups_today = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(DISTINCT VolunteerID) as count FROM volunteerassignment WHERE TaskDate = CURDATE()")
    volunteers_today = cursor.fetchone()['count']
    conn.close()
    stats = {"animals_onsite": animals_onsite, "pending_adoptions": pending_adoptions, "checkups_today": checkups_today, "volunteers_today": volunteers_today}
    return jsonify(stats)
@app.route('/api/staff/needs-attention')
def api_staff_needs_attention():
    query = "SELECT AnimalID, Name, Species, Status FROM animal WHERE Status != 'Available' AND Status != 'Adopted'"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({"id": row['AnimalID'], "name": row['Name'], "species": row['Species'], "status": row['Status'], "status_class": row['Status'].lower().replace(" ", "-")})
    return jsonify(data)
@app.route('/api/staff/recent-adoptions')
def api_staff_recent_adoptions():
    query = "SELECT ad.AdoptionID, an.Name, ad.AdopterName, ad.AdoptionDate FROM adoption ad JOIN animal an ON ad.AnimalID = an.AnimalID ORDER BY ad.AdoptionDate DESC LIMIT 5"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({"id": row['AdoptionID'], "animal_name": row['Name'], "adopter_name": row['AdopterName'], "date": row['AdoptionDate'].isoformat()})
    return json.dumps(data, default=default_converter)
@app.route('/api/staff/all-animals')
def api_all_animals():
    
    # MODIFICATION: The query now calls your new function CalculateAge()
    query = "SELECT AnimalID, Name, Species, Breed, Status, CalculateAge(DOB) as Age FROM animal"
    
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    data = []
    for row in results:
        data.append({
            "id": row['AnimalID'],
            "name": row['Name'],
            "species": row['Species'],
            "breed": row['Breed'],
            "status": row['Status'],
            "status_class": row['Status'].lower().replace(" ", "-"),
            "age": row['Age'] 
        })
    return jsonify(data)
@app.route('/api/staff/all-adoptions')
def api_all_adoptions():
    query = "SELECT ad.AdoptionID, an.Name, ad.AdopterName, ad.AdopterContact, ad.AdoptionDate FROM adoption ad LEFT JOIN animal an ON ad.AnimalID = an.AnimalID ORDER BY ad.AdoptionDate DESC"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({"id": row['AdoptionID'], "animal_name": row['Name'] or "N/A", "adopter_name": row['AdopterName'], "contact": row['AdopterContact'], "date": row['AdoptionDate'].isoformat()})
    return json.dumps(data, default=default_converter)
@app.route('/api/staff/all-donations')
def api_all_donations():
    query = "SELECT d.DonationID, dn.Name, d.DonationAmount, d.DonationType, d.DonationDate FROM donation d LEFT JOIN donor dn ON d.DonorID = dn.DonorID ORDER BY d.DonationDate DESC"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({"id": row['DonationID'], "donor_name": row['Name'] or "Anonymous", "amount": f"₹{row['DonationAmount']:,.2f}" if row['DonationAmount'] else "N/A", "type": row['DonationType'], "date": row['DonationDate'].isoformat()})
    return json.dumps(data, default=default_converter)
@app.route('/api/staff/all-supplies')
def api_all_supplies():
    query = "SELECT SupplyID, SupplyName, Quantity, ReceivedDate, DonationID FROM supply ORDER BY ReceivedDate DESC"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({"id": row['SupplyID'], "name": row['SupplyName'], "quantity": row['Quantity'], "date": row['ReceivedDate'].isoformat(), "donation_id": row['DonationID'] or "N/A"})
    return json.dumps(data, default=default_converter)
@app.route('/api/staff/all-treatments')
def api_all_treatments():
    query = "SELECT a.Name as AnimalName, t.TreatmentType, t.DateGiven, s.Name as StaffName, t.Veterinarian FROM treatment t LEFT JOIN animal a ON t.AnimalID = a.AnimalID LEFT JOIN staff s ON t.StaffID = s.StaffID ORDER BY t.DateGiven DESC"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({"animal_name": row['AnimalName'] or "N/A", "treatment": row['TreatmentType'], "date": row['DateGiven'].isoformat(), "staff_name": row['StaffName'] or "N/A", "vet": row['Veterinarian']})
    return json.dumps(data, default=default_converter)
@app.route('/api/staff/all-checkups')
def api_all_checkups():
    query = "SELECT a.Name, ar.CheckupDate, ar.Weight, ar.Diagnosis, ar.NextVisit FROM animalhealthrecord ar LEFT JOIN animal a ON ar.AnimalID = a.AnimalID ORDER BY ar.CheckupDate DESC"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({"animal_name": row['Name'] or "N/A", "date": row['CheckupDate'].isoformat(), "weight": row['Weight'], "diagnosis": row['Diagnosis'], "next_visit": row['NextVisit'].isoformat() if row['NextVisit'] else "N/A"})
    return json.dumps(data, default=default_converter)
@app.route('/api/volunteer/stats')
def api_volunteer_stats():
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    params = (CURRENT_VOLUNTEER_ID,)
    cursor.execute("SELECT HoursContributed FROM volunteer WHERE VolunteerID = %s", params)
    total_hours = cursor.fetchone()['HoursContributed']
    cursor.execute("SELECT COUNT(TaskID) as count FROM volunteertask WHERE VolunteerID = %s AND HoursWorked > 0", params)
    tasks_completed = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(TaskID) as count FROM volunteertask WHERE VolunteerID = %s AND (HoursWorked IS NULL OR HoursWorked = 0)", params)
    tasks_pending = cursor.fetchone()['count']
    conn.close()
    stats = {"total_hours": total_hours, "tasks_completed": tasks_completed, "tasks_pending": tasks_pending}
    return jsonify(stats)
@app.route('/api/volunteer/tasks')
def api_volunteer_tasks():
    query = "SELECT vt.TaskDate, vt.TaskDescription, a.Name, vt.HoursWorked FROM volunteertask vt LEFT JOIN animal a ON vt.AnimalID = a.AnimalID WHERE vt.VolunteerID = %s ORDER BY vt.TaskDate DESC"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (CURRENT_VOLUNTEER_ID,))
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        is_completed = (row['HoursWorked'] or 0) > 0
        data.append({"date": row['TaskDate'].isoformat(), "description": row['TaskDescription'], "animal_name": row['Name'] or "N/A", "status": "Completed" if is_completed else "Pending", "hours": row['HoursWorked'] or 0})
    return json.dumps(data, default=default_converter)
@app.route('/api/volunteer/profile')
def api_volunteer_profile():
    query = "SELECT Name, Role, ContactInfo, HoursContributed FROM volunteer WHERE VolunteerID = %s"
    conn = get_db_connection()
    if not conn: return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (CURRENT_VOLUNTEER_ID,))
    profile = cursor.fetchone()
    conn.close()
    data = {"name": profile['Name'], "role": profile['Role'], "contact": profile['ContactInfo'], "total_hours": profile['HoursContributed']}
    return jsonify(data)

# This route now calls a Stored Procedure instead of running 3 queries
@app.route('/api/animal_profile/<int:animal_id>')
def api_animal_profile(animal_id):
    try:
        conn = get_db_connection()
        if not conn: return "Database connection failed", 500
        cursor = conn.cursor(dictionary=True)
        
        # Call the stored procedure by name
        cursor.callproc('sp_GetAnimalProfile', [animal_id,])
        
        # --- This is how you read multiple results from a procedure ---
        results = []
        for result_set in cursor.stored_results():
            results.append(result_set.fetchall())
        # -----------------------------------------------------------
        
        conn.close()
        
        # results[0] contains the data from the first SELECT (Animal Details)
        # results[1] contains the data from the second SELECT (Health Records)
        # results[2] contains the data from the third SELECT (Treatments)
        
        # Combine all results into one JSON object
        data = {
            "details": results[0][0] if results[0] else None, # Get the first (and only) row
            "health": results[1] if results[1] else [],
            "treatments": results[2] if results[2] else []
        }
        
        return json.dumps(data, default=default_converter)
        
    except Exception as e:
        print(f"Error in api_animal_profile: {e}")
        return jsonify({"error": "An error occurred"}), 500


# --- 6. ACTION (CRUD) ROUTES ---

@app.route('/add_animal_action', methods=['POST'])
def add_animal_action():
    try:
        name = request.form['animal_name']
        species = request.form['animal_species']
        breed = request.form['animal_breed'] 
        dob = request.form['animal_dob']
        status = request.form['animal_status']
        
        if not dob:
            dob = None
                
        conn = get_db_connection()
        if not conn: return "Database connection failed", 500
        cursor = conn.cursor()
                
        query = "INSERT INTO animal (Name, Species, Breed, DOB, Status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, species, breed, dob, status))
        conn.commit()
        conn.close()
                
        return redirect(url_for('staff_animals'))
        
    except Exception as e:
        print(f"Error in add_animal_action: {e}")
        return "Error processing request", 500

@app.route('/api/admin/delete_user/<string:username>', methods=['DELETE'])
def delete_user_action(username):
    try:
        if username == 'admin':
            return jsonify({"success": False, "error": "Cannot delete main admin account."}), 400

        conn = get_db_connection()
        if not conn: return "Database connection failed", 500
        
        cursor = conn.cursor()
        
        query = "DELETE FROM UserLogin WHERE Username = %s"
        cursor.execute(query, (username,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Successfully deleted user: {username}")
            conn.close()
            return jsonify({"success": True})
        else:
            print(f"Delete failed: User not found: {username}")
            conn.close()
            return jsonify({"success": False, "error": "User not found."}), 404
        
    except Exception as e:
        print(f"Error in delete_user_action: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    

# This route handles the form submission from volunteer_profile.html
@app.route('/update_volunteer_contact', methods=['POST'])
def update_volunteer_contact():
    try:
        new_contact_info = request.form['contact_info']
        volunteer_id = CURRENT_VOLUNTEER_ID 
        
        conn = get_db_connection()
        if not conn: return "Database connection failed", 500
        cursor = conn.cursor()
                
        query = "UPDATE volunteer SET ContactInfo = %s WHERE VolunteerID = %s"
        cursor.execute(query, (new_contact_info, volunteer_id))
        conn.commit()
        conn.close()
                
        return redirect(url_for('volunteer_profile'))
        
    except Exception as e:
        print(f"Error in update_volunteer_contact: {e}")
        return "Error processing request", 500
    
# This route handles the form submission from add_treatment.html
@app.route('/add_treatment_action', methods=['POST'])
def add_treatment_action():
    try:
        animal_id = request.form['animal_id']
        staff_id = request.form['staff_id']
        treatment_type = request.form['treatment_type']
        date_given = request.form['date_given']
        vet_name = request.form['vet_name']
        notes = request.form['notes']

        conn = get_db_connection()
        if not conn: return "Database connection failed", 500
        cursor = conn.cursor()
                
        query = """
            INSERT INTO treatment (AnimalID, StaffID, TreatmentType, DateGiven, Veterinarian, Notes) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (animal_id, staff_id, treatment_type, date_given, vet_name, notes))
        conn.commit()
        conn.close()
                
        return redirect(url_for('staff_health'))
        
    except Exception as e:
        print(f"Error in add_treatment_action: {e}")
        return "Error processing request", 500
    
# This route handles the form submission from add_adoption.html
@app.route('/add_adoption_action', methods=['POST'])
def add_adoption_action():
    try:
        animal_id = request.form['animal_id']
        adopter_name = request.form['adopter_name']
        adopter_contact = request.form['adopter_contact']
        adoption_date = request.form['adoption_date']

        conn = get_db_connection()
        if not conn: return "Database connection failed", 500
        cursor = conn.cursor()
        
        query = """INSERT INTO adoption (AnimalID, AdoptionDate, AdopterName, AdopterContact) 
            VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (animal_id, adoption_date, adopter_name, adopter_contact))
        conn.commit()
        conn.close()
        
        # Your TRIGGER will have automatically updated the animal's status.
        return redirect(url_for('staff_adoptions'))
        
    except mysql.connector.Error as err:
        # This will catch the error from your TRIGGER
        print(f"Error in add_adoption_action: {err}")
        return f"Error: {err.msg}", 500
    except Exception as e:
        print(f"Error in add_adoption_action: {e}")
        return "Error processing request", 500


# --- 7. RUN THE APP ---

if __name__ == '__main__':
    print("--- Starting Animal Shelter Web Server ---")
    print("Go to this URL in your browser: http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)