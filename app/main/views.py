
from . import main
from flask import render_template
from flask import Flask, request, abort
import psycopg2, json
from app.models import Device_Data , Device_Info , User_Mgmt
from app import db

@main.route('/hello')
def publish_hello():
    return render_template('index.html')

@main.route('/setting')
def publish_setting():
    return render_template('setting.html')

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

@main.route("/tsfm_service_status", methods = ["POST"])
def service_status():
    #get device status data
    if request.method == "POST":
        print("For TSFM SERVICE STATUS Data: \n", request.json)
        whkServiceStatus = json.dumps(request.json, ensure_ascii = False)
    else:
        abort(400) 
## update user service status / insert new entry
    if len(User_Mgmt.query.filter_by(user_id = whkServiceStatus['userId'])) > 0: 
      User_Mgmt.query.filter_by(user_id = whkServiceStatus['userId']).update({
          'activated': whkServiceStatus['status']
       })         
      db.session.commit()
    else:  
      db.session.add(User_Mgmt(user_id = whkServiceStatus['userId']))
      db.session.add(User_Mgmt(activated = whkServiceStatus['status']))
      db.session.commit()

## save user id for device
    _userid_ = whkServiceStatus['userId']
## update device list info / insert new device info entry
    for i in range(whkServiceStatus['associations']) :
      _gatewayid_ = whkServiceStatus['associations'][i]['gateway']['uuid']
      for j in range(whkServiceStatus['associations'][i]['gateway']['devices']) :
        if len(Device_Info.query.filter_by(uuid = whkServiceStatus['associations'][i]['gateway']['devices'][j]['uuid'])) > 0 : 
          Device_Info.query.filter_by(uuid = whkServiceStatus['associations'][i]['gateway']['devices'][j]['uuid']).update({
            'online_status': whkServiceStatus['associations'][i]['gateway']['devices'][j]['status'],
            'name' : whkServiceStatus['associations'][i]['gateway']['devices'][j]['name'],
            'model': whkServiceStatus['associations'][i]['gateway']['devices'][j]['model'],
            'gw_uuid': _gatewayid_,
            'user_id': _userid_ ,
            'associated': 'TRUE'
            }
          )

          db.session.commit()         
        
        else:  
          db.session.add(Device_Info(uuid = whkServiceStatus['associations'][i]['gateway']['devices'][j]['uuid']))
          db.session.add(Device_Info(online_status = whkServiceStatus['associations'][i]['gateway']['devices'][j]['status']))
          db.session.add(Device_Info(name = whkServiceStatus['associations'][i]['gateway']['devices'][j]['name']))
          db.session.add(Device_Info(model = whkServiceStatus['associations'][i]['gateway']['devices'][j]['model']))
          db.session.add(Device_Info(gw_uuid = _gatewayid_))
          db.session.add(Device_Info(user_id = _userid_))
          db.session.add(Device_Info(associated = 'TRUE'))
          db.session.commit() 


  
           
def dbconnect():
    ## Insert data to database
    conn = psycopg2.connect(database = "tsfm", user = "postgres", password = "link4581", host = "192.168.7.85", port = "5432")
    print("DB connected")
    cursor = conn.cursor()
    cursor.close()
    print("Cursor Closed")
    conn.close()
    print("DB Closed")