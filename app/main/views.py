
from . import main
from flask import render_template

@main.route('/hello')
def publish_hello():
    return render_template('index.html')

@main.route("/tsfm_service_status", methods = ["POST"])
def service_status():
    # get service status
    if request.method == "POST":
        print("For TSFM SERVICE STATUS Data: \n", request.json)
        return json.dumps(request.json, ensure_ascii = False)
    else:
        abort(400)
        
@main.route("/tsfm_required_data", methods = ["POST"])
def required_data():
    # get required data 
    if request.method == "POST":
        print("For TSFM REQUIRED DATA Data: \n", request.json)
        return json.dumps(request.json, ensure_ascii = False)
    else:
        abort(400) 
    
@main.route("/tsfm_device_status", methods = ["POST"])
def device_status():
    #get device status data
    if request.method == "POST":
        print("For TSFM DEVICE STATUS Data: \n", request.json)
        return json.dumps(request.json, ensure_ascii = False)
    else:
        abort(400) 
           
def dbconnect():
    ## Insert data to database
    conn = psycopg2.connect(database = "tsfm", user = "postgres", password = "link4581", host = "192.168.7.85", port = "5432")
    print("DB connected")
    cursor = conn.cursor()
    cursor.close()
    print("Cursor Closed")
    conn.close()
    print("DB Closed")