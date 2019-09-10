from flask import Flask, jsonify, request,json
import dbutility
import faceapiplay
from datetime import datetime

app = Flask(__name__) 

# This method is used to retrieve the details of registered Visitor from the DB
@app.route('/getVisitorDetails/<int:visId>',methods=['GET'])
def getVisitorDetails(visId):
    return jsonify({'about': visId})


# This method is used to retrieve the details of registered Visitor from the DB
@app.route('/registerVisitor',methods=['POST'])
def registerVisitorDetails():
    #if(request.method()=='POST'):

    # Get the JSON details from the request
    visitordetailsJson = request.json
    visitordetailsJsonstr= json.dumps(visitordetailsJson)
    parsed_json = json.loads(visitordetailsJsonstr)
    name = parsed_json['name']
    company = parsed_json['name']
    mobilenumber = parsed_json['mobilenumber']
    faceimg = parsed_json['faceimg']
    type(faceimg)
    persistedfaceid = registerpersonface(name,faceimg)

    #persistedfaceid ="0f31e390-17fc-4ee7-b325-60068f1e9c15"

    visitorrow = []
    visitorrow.append(name)
    visitorrow.append(company)
    visitorrow.append(mobilenumber)
    visitorrow.append(faceimg)
    visitorrow.append(persistedfaceid)

    persontomeet = parsed_json['persontomeet']
    reason = parsed_json['reason']

    visitdetailsrow = []
    

    cnnx = dbutility.getConnection("vmsappdb.database.windows.net","vms_app","vmsUser","Newuser@123","{SQL Server}")
    dbutility.executeInsertSQL(cnnx,"insert into [visitormaster] (visname, viscompany, vismobilenumber, faceimg,vispersistedFaceId) VALUES (?,?,?,?,?)",visitorrow)
    cnnx = dbutility.getConnection("vmsappdb.database.windows.net","vms_app","vmsUser","Newuser@123","{SQL Server}")

    selectquery = "SELECT max(vistorid) FROM visitormaster where visname='" + name + "'"
    print(selectquery)
    vistoridlst = dbutility.executeSelectSQL(cnnx,selectquery)

    vistorid = vistoridlst[0][0]
    print(vistorid)
    visitdetailsrow.append(vistorid)
    visitdetailsrow.append(persontomeet)
    visitdetailsrow.append(reason)

    # current date and time
    now = datetime.now()
    visitdetailsrow.append(now)
    cnnx = dbutility.getConnection("vmsappdb.database.windows.net","vms_app","vmsUser","Newuser@123","{SQL Server}")
    dbutility.executeInsertSQL(cnnx,"insert into [visitdetails] (vistorid, persontomeet, reason, checkintime ) VALUES (?,?,?,?)",visitdetailsrow)
        
    #print(visitordetailsJson)
    return jsonify(request.json)


# This method is used to register a user in Face API
def registerpersonface(name,faceimg):
    personID = faceapiplay.createPerson("rkgroup2",name)
    faceapiplay.addFacewithBinary("rkgroup2",personID,faceimg)
    return personID

@app.route('/identifyVisitor',methods=['POST'])
def identifyVisitor():
    # Get the Image
    # Pass the image & get the face ID
    # Detect Face & get the face ID
    # Invoke Identify and return the faceID
    visitoridentifierjson = request.json
    visitoridentifierjsonstr= json.dumps(visitoridentifierjson)
    parsed_json = json.loads(visitoridentifierjsonstr)
    faceimg = parsed_json['faceimg']

    detectedFaceId = faceapiplay.detectFaceWithBinary(faceimg)
    faceapiplay.identifyFace("mainbu",detectedFaceId)







