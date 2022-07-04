
from datetime import datetime
from email.policy import default
from tokenize import String
from flask import Flask, redirect,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


###################### ---- APP VARIABLE -----#################

app = Flask(__name__)
#-----------SQL LITE CONNECTION

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wardsys.db'


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kiyjxcfsojujet:9ddc7c2f5ab88dbb0a764e34f1d54561020d36463e8985215fe6ec02a1ee05a9@ec2-52-204-195-41.compute-1.amazonaws.com:5432/d16vlocu92l8pg'
#----------- MYSQL  CONNECTION

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/ward_patient'


###################### ----DATABASE CONFIGURATIONS -----#################
db = SQLAlchemy(app)
class Patient (db.Model):
        id = db.Column(db.Integer, primary_key = True) 
        first_name = db.Column(db.String(50),nullable = False)
        last_name = db.Column(db.String(50),nullable = False)
        ward_name = db.Column(db.String(50),nullable = False)
        bed_number = db.Column(db.Integer,nullable = False, default = 1)
        node_number = db.Column(db.Integer,nullable = False, default = 0)

        doctor_incharge = db.Column(db.String(80),nullable = False)
        patient_conditon = db.Column(db.String(20),nullable = False)
        patient_created = db.Column(db.DateTime, nullable = False , default =datetime.utcnow )
      #  HealthRecords = db.relationship('HealthRecord',backref='author', lazy = True)


        def __repr__(self):
                return f"Patient('{self.first_name}','{self.last_name}','{self.ward_name}','{self.node_number}', '{self.bed_number}','{self.doctor_incharge}','{self.patient_conditon}')"

class HealthRecord(db.Model): 
        id = db.Column(db.Integer, primary_key = True)
        temperature = db.Column(db.Float, nullable = False,)
        heart_rate = db.Column(db.Integer, nullable = False,)
        sensor_Id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable = False,default = 0)
        time_created = db.Column(db.DateTime, nullable = False , default =datetime.utcnow )

        def __repr__(self):
            return f"HealthRecord('{self.temperature}', '{self.heart_rate}', '{self.time_created}')"
        def __getitem__(self,key):
                return self.__dict__[key]
class Sensor(db.Model): 
        id = db.Column(db.Integer, primary_key = True)
        ward_name = db.Column(db.String(60),nullable = False)
        bed_number = db.Column(db.Integer,nullable = False, default = 1)
        HealthRecords = db.relationship('HealthRecord',backref='author', lazy = True) #relationship

        def __repr__(self):
            return f"Sensor('{self.id}','{self.ward_name}')"


###################### ----ROUTES -----#################
####----- HOME ----#####
#__________________________________________________________________________________
#__________________________________________________________________________________
@app.route('/')
def index():
        critital_condition  = "Critical"
        patients_list = Patient.query.all()
        criticals = Patient.query.filter(Patient.patient_conditon == critital_condition).all()
        Sensor_list = Sensor.query.all()
        patientNumber = len(patients_list)
        SensorNumber = len(Sensor_list)
        criticalNumber = len(criticals)
        return render_template('index.html',patientNumber = patientNumber,
         SensorNumber = SensorNumber, criticalNumber = criticalNumber)

####----- PATIENTS ----#####
#__________________________________________________________________________________
#__________________________________________________________________________________
@app.route('/add-patient-form')
def add_patient_form():
        ##return a form
         return render_template('add_patient_form.html')

 
#//////////////////////////////////////////////////////////////////////////////////////
#__________________________________________________________________________________
#__________________________________________________________________________________
@app.route('/add-patient', methods = ['POST'])
def add_patient():
        ### catpturing form data
        first_name = request.form.get('firt_name')
        last_name = request.form.get('last_name')
        ward_name = request.form.get('ward_name')
        bed_number = request.form.get('bed_number')
        doctor_incharge = request.form.get('doctor_incharge')
        patient_conditon = request.form.get('patient_conditon')

        if (first_name != '' and last_name != '') :
                 #patients add to Model in database
                new_patient = Patient(first_name = first_name,last_name = last_name,
                ward_name = ward_name, bed_number = bed_number, doctor_incharge = doctor_incharge, 
                patient_conditon = patient_conditon)

                ##message = "New Patient added"
                ####-----sending and committing data to Database 
                try:
                        db.session.add(new_patient)
                        db.session.commit()
                        return redirect('/patient-enrolled')
                except:
                        return "No patient added to database, check your Details again"
        else:
                
                return redirect('/add-patient-form')

       
 #__________________________________________________________________________________
#__________________________________________________________________________________

####----- REGISTER A SENSOR NODE ----#####
#__________________________________________________________________________________
#__________________________________________________________________________________
@app.route('/register-sensor-node-form')
def register_sensorNode_form():
        ##return a form
        nodeAvailable = Sensor.query.all()
        return render_template('add_sensor_form.html',nodeAvailable = nodeAvailable)


#__________________________________________________________________________________
#__________________________________________________________________________________

@app.route('/assign/<id>')
def assign_sensorNode(id = id):
        id = id
        #patientName = Patient.query.filter(Patient.id == id)
        patientName = Patient.query.filter(Patient.id == id).first()
        ##return a form
        nodeAvailable = Sensor.query.all()
        
        return render_template('assign-sensor.html',nodeAvailable = nodeAvailable, id = id, patientName = patientName)
#__________________________________________________________________________________
#__________________________________________________________________________________
@app.route('/remove/<id>')
def remove_sensorNode(id):
        patient_id = id
        removeSensorPatient = Patient.query.filter(Patient.id == patient_id).first()
        removeSensorPatient.node_number = 0
        #return removeSensorPatient.first_name
        try:
                db.session.commit()
                return redirect('/patient-enrolled')
        except:
                return "No patient added to database, check your Details again"
#__________________________________________________________________________________
#__________________________________________________________________________________

@app.route('/update-patient-node' , methods = ['POST'])
def update_patient_nodeNumber():
        ##return a form
        node_number = request.form.get('node_number')
        patient_id = request.form.get('patient_id')

        updatePatient = Patient.query.filter(Patient.id == patient_id).first()
        updatePatient.node_number = node_number
        try:
                db.session.commit()
                return redirect('patient-enrolled')
        except:
                return "No patient added to database, check your Details again"
      

  #__________________________________________________________________________________
#__________________________________________________________________________________      

#//////////////////////////////////////////////////////////////////////////////////////
@app.route('/register-node', methods = ['POST'])
def register_node():
        ### catpturing form data
        
        ward_name = request.form.get('ward_name')
        bed_number = request.form.get('bed_number')
        
        #patients add to Model in database
        new_node = Sensor(ward_name = ward_name, bed_number = bed_number)
        ##message = "New Node-sensor added"
        ####-----sending and committing data to Database 
        try:
                db.session.add(new_node)
                db.session.commit()
                return redirect('/register-sensor-node-form')
        except:
                return "No patient added to database, check your Details again"
  
#//////////////////////////////////////////////////////////////////////////////////////

#__________________________________________________________________________________
#__________________________________________________________________________________
@app.route('/patient-enrolled')
def patientEnrolled():

        ##Querying patients list From DB
        page = request.args.get('page', 1 , type=int) #passing page number 

        patients_list = Patient.query.order_by(Patient.patient_created.desc()).paginate(page=page, per_page=7)


        return render_template('patient_list.html', patients = patients_list)

#__________________________________________________________________________________
#__________________________________________________________________________________

@app.route('/patient-monitored')
def patientMonitored():

        ##Querying patients list From DB
        patients_list = Patient.query.filter(Patient.node_number != 0).all()
        patientNumber = len(patients_list)

        return render_template('patient_monitored.html', patients = patients_list, patientNumber = patientNumber)

#__________________________________________________________________________________

#__________________________________________________________________________________
@app.route('/patient-status/<id>')
def patientStatus(id = id):
        patientID = id
        patientInfo = Patient.query.filter(Patient.id == patientID).first()
        nodeNumber = patientInfo.node_number
        ##Querying patients-health records From DB
        page = request.args.get('page', 1 , type=int) #passing page number 
        healthRecord = HealthRecord.query.\
                filter(HealthRecord.sensor_Id == nodeNumber ).\
                        paginate(page=page, per_page=10)

                        # For Table
        data = HealthRecord.query.\
                filter(HealthRecord.sensor_Id == nodeNumber).all()
        labels = [row['id'] for row in data]
        temperatures = [row["temperature"] for row in data]
        heart_rate = [row["heart_rate"] for row in data]

        return render_template('patient_status.html', healthRecords = healthRecord\
                 ,patientInfo = patientInfo, labels = labels, temperatures = temperatures, heart_rate = heart_rate )
#//////////////////////////////////////////////////////////////////////////////////////

#-----------ACCEPTING SENSOR DATA VIA URL
@app.route('/sensor/data/<int:sensorId>/<float:temperature>/<int:heart_rate>')
def sensor_data(sensorId,temperature,heart_rate):
        sensorId = sensorId
# Validating sensor Data

        if (temperature > 25 and temperature < 41.0 and heart_rate > 60 and heart_rate < 120):
                temperatureNew = temperature
                heart_rateNew = heart_rate
                #sensor id and sensor data to db
                 #patients add to Model in database
                new_sensor_data = HealthRecord(temperature = temperatureNew, heart_rate = heart_rateNew , sensor_Id = sensorId)

                ##message = "New Sensor added"
                ####-----sending and committing data to Database 
                try:
                        db.session.add(new_sensor_data)
                        db.session.commit()
                        return "Sensor data added "
                except:
                        return "No data added to database, check your Details again"
        else:
                return "Invalid Sensor Values"
        
      

#__________________________________________________________________________________
#________________________________________________________
# 
@app.route('/graph')
def testGraph():
        nodeNumber = 1
        data1 = [
                []
        ]
        data = HealthRecord.query.\
                filter(HealthRecord.sensor_Id == nodeNumber).all()
        labels = [row['id'] for row in data]
        temperatures = [row["temperature"] for row in data]
        heart_rate = [row["heart_rate"] for row in data]
        # values1 = [row[2] for row in data]

        return render_template('test_graph.html', labels = labels, temperatures = temperatures , heart_rate = heart_rate)
        # return labels
#_
# __________________________
####----- GUIDE ----#####
@app.route('/guide')
def systemGuider():

        return render_template('sys_guide.html')

#__________________________________________________________________________________
#__________________________________________________________________________________

if __name__ == '__main__':
    app.run(debug = True)