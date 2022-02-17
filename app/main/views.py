# -*- coding: utf-8 -*-
from flask import send_from_directory
from . import main
from flask import render_template
from flask import Flask, request, abort
import psycopg2, json
from ..models import Device_Data , Device_Info , User_Mgmt
from app import db
from sqlalchemy import exists
import os
from . import language


@main.route('/hello',methods = ["GET"])
def publish_hello():

    token = request.args.get('token')
    userid = request.args.get('userid')
    redirect_app = request.args.get('redirect_app')
    
    #token = ""
    #userid = '94f43ded-55b6-4354-aaae-c5cc20fde280'
    #redirect_app = ""

    devicelist = Device_Info.get_by_userid(userid)
    user_info = User_Mgmt.query.filter_by(user_id=userid)
    return render_template('index.html',userid = userid,redirect_app=redirect_app ,user_info = user_info , devices = devicelist)
    #return render_template("product/order.html", orders=orders, catalogs=catalogs, message=message)

@main.route('/testpost/<userid>/<status>')
def update_notify_all(userid,status,methods = ["GET"]):

    user = User_Mgmt.query.filter_by(user_id=userid).first()
    if user != None :
        user.notify_all = status
        db.session.commit()
        return("200")
    else:
        return("400")


@main.route('/setting',methods = ["POST"])
def update_device_setting():
    # get required data 
    if request.method == "POST":
        print("For TSFM REQUIRED DATA Data: \n", request.form)
        #return json.dumps(request.json, ensure_ascii = False)
    else:
        abort(400)
    notification = "OFF"
    for key,value in request.form.items():
        if key == 'notification' :
            notification = "ON"
            break
    notification = notification
    goal = request.form["goal"]
    lower_bound = request.form["lower_bound"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    userid = request.form["userid"]
    redirect_app = request.form["redirect_app"]
    
    db.session.query(Device_Info).filter_by(uuid=request.form["uuid"]).update(dict(lower_bound=lower_bound,start_time=start_time,end_time=end_time,target_energy_level=goal,notify=notification))

    db.session.commit()
    devicelist = Device_Info.get_by_userid(userid)
    user_info = User_Mgmt.query.filter_by(user_id=userid)
    return render_template('index.html',userid = userid,redirect_app=redirect_app ,user_info = user_info , devices = devicelist)

@main.route('/postpicture/<string:filename>')
def get_postimage(filename,methords = ["GET"]):
    app_dir = os.getcwd()
    return send_from_directory(os.path.join(app_dir, 'static', 'img'), filename)


@main.route('/setting',methods = ["GET"])
def publish_setting():
    userid = request.args.get('userid')
    redirect_app = request.args.get('redirect_app')
    uuid = request.args.get('uuid')
    
    device_info = Device_Info.query.filter_by(uuid=uuid)
    return render_template('setting.html',userid=userid,redirect_app=redirect_app,device_info=device_info)

@main.route("/tsfm_required_data", methods = ["POST"])
def required_data():
    # get required data 
    if request.method == "POST":
        print("For TSFM REQUIRED DATA Data: \n", request.json)
        #return json.dumps(request.json, ensure_ascii = False)
    else:
        abort(400) 
        
    # Insert data to DB
    dict_raw_data = request.json
    list_data = dict_raw_data["data"]
    for i in range(len(list_data)):
        db.session.add(Device_Data(dev_uuid = list_data[i]['deviceUuid'],
                                    model = list_data[i]['model'], 
                                    scope = list_data[i]['scope'], 
                                    value = float(list_data[i]['value']), 
                                    generated_time = list_data[i]['generatedTime'], 
                                    uploaded_time = list_data[i]['uploadedTime']))
        db.session.commit()
    return json.dumps(request.json, ensure_ascii = False)

    
  
@main.route("/tsfm_device_status", methods = ["POST"])
def device_status():
    #get device status data
    if request.method == "POST":
        print("For TSFM DEVICE STATUS Data: \n", request.json)
        #return json.dumps(request.json, ensure_ascii = False)
    else:
        abort(400)
        
    dict_data = request.json
    if dict_data["gateway"]["devices"] is None:
        pass
    elif dict_data['triggerReason'] == "DEVICE_UNPAIRED":
        list_exist_data = []
        list_income_data = []
        for device_info in Device_Info().query.filter_by(user_id = dict_data["userId"]):
            #query all the devices which belongs to user_id = xxxxx
            list_exist_data.append(device_info.uuid)
        for new_income_data in range(len(dict_data['gateway']['devices'])):
            list_income_data.append(dict_data['gateway']['devices'][new_income_data]['uuid'])

        for i in range(len(list_exist_data)):
            if list_exist_data[i] not in list_income_data:
                Device_Info().query.filter_by(uuid = list_exist_data[i]).delete()
                db.session.commit()
    elif dict_data['triggerReason'] == "GATEWAY_DISASSOCIATED":
        Device_Info().query.filter_by(gw_uuid = dict_data['gateway']['uuid']).delete()
        db.session.commit()
    else:     
        for i in range(len(dict_data["gateway"]["devices"])):
            is_exist = db.session.query(exists().where(Device_Info.uuid == dict_data["gateway"]["devices"][i]["uuid"])).scalar()
            #if device uuid already exist in DB
            if is_exist == True:
                Device_Info().query.filter_by(uuid = dict_data["gateway"]["devices"][i]["uuid"]).update(
                        {
                            "name": dict_data["gateway"]["devices"][i]["name"],
                            "model": dict_data["gateway"]["devices"][i]["model"],
                            "online_status": dict_data["gateway"]["devices"][i]["status"]
                         }  
                    )
            # Insert a new device uuid
            else:
                db.session.add(
                                Device_Info(
                                        uuid = dict_data["gateway"]["devices"][i]["uuid"],
                                        name = dict_data["gateway"]["devices"][i]["name"],
                                        model = dict_data["gateway"]["devices"][i]["model"],
                                        online_status = dict_data["gateway"]["devices"][i]["status"],
                                        gw_uuid = dict_data["gateway"]["uuid"],
                                        user_id = dict_data["userId"],
                                        associated = 'TRUE'
                                    ))
            db.session.commit()  
    return json.dumps(request.json, ensure_ascii = False)
            ## Note:
            ##  For now won't insert the data of gateway associate/dissociate

@main.route("/tsfm_service_status", methods = ["POST"])
def service_status():
    #get device status data
    if request.method == "POST":
        print("For TSFM SERVICE STATUS Data: \n", request.json)
        whkSvcSta = request.json
    else:
        abort(400)
## update user service status / insert new entry
    if User_Mgmt().query.filter_by(user_id = whkSvcSta['userId']).count() > 0: 
      User_Mgmt().query.filter_by(user_id = whkSvcSta['userId']).update({
          'activated': whkSvcSta['status']
       })         
      db.session.commit()
    else:  
      db.session.add(User_Mgmt(user_id = whkSvcSta['userId'], activated = whkSvcSta['status']))
      db.session.commit()

## save user id for device
    _userid_ = whkSvcSta['userId']
## update device list info / insert new device info entry
    if len(whkSvcSta['associations']) > 0 :
      for i in range(len(whkSvcSta['associations'])) :
        _gatewayid_ = whkSvcSta['associations'][i]['gateway']['uuid']
        for j in range(len(whkSvcSta['associations'][i]['gateway']['devices'])) :
          if Device_Info().query.filter_by(uuid = whkSvcSta['associations'][i]['gateway']['devices'][j]['uuid']).count() > 0 : 
            Device_Info().query.filter_by(uuid = whkSvcSta['associations'][i]['gateway']['devices'][j]['uuid']).update({
              'online_status': whkSvcSta['associations'][i]['gateway']['devices'][j]['status'],
              'name' : whkSvcSta['associations'][i]['gateway']['devices'][j]['name'],
              'model': whkSvcSta['associations'][i]['gateway']['devices'][j]['model'],
              'gw_uuid': _gatewayid_ ,
              'user_id': _userid_ ,
              'associated': 'TRUE'
              }
            )

            db.session.commit()         
        
          else:  
            db.session.add(Device_Info(uuid = whkSvcSta['associations'][i]['gateway']['devices'][j]['uuid'], 
              online_status = whkSvcSta['associations'][i]['gateway']['devices'][j]['status'],
              name = whkSvcSta['associations'][i]['gateway']['devices'][j]['name'], 
              model = whkSvcSta['associations'][i]['gateway']['devices'][j]['model'], 
              gw_uuid = _gatewayid_ , 
              user_id = _userid_ , 
              associated = 'TRUE'))
          
            db.session.commit()
    
    return json.dumps(request.json, ensure_ascii = False)
