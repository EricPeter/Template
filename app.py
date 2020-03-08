import sqlite3,hashlib
from flask import Flask, render_template, url_for, request,jsonify,redirect,g,send_file,Response,flash
from flask_sqlalchemy import SQLAlchemy
import base64
import datetime
from datetime import datetime
import xlsxwriter
import io
from io import BytesIO



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
autoflush=True
db  = SQLAlchemy(app)
'''Create Company profile table'''
class Company(db.Model):
    __tablename__="Company"
    id = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(300))
    Tin = db.Column(db.String(300))
    nssf_number = db.Column(db.String(300))
    address = db.Column(db.String(300))
    email = db.Column(db.String(300))
    telephone = db.Column(db.String(300))
    image=db.Column(db.LargeBinary)
    def __init__(self,cname,Tin,nssf_number,address,email,telephone,image):
        self.cname=cname
        self.Tin=Tin
        self.nssf_number=nssf_number
        self.address=address
        self.email=email
        self.telephone=telephone
        self.image=image
'''Create a working days table'''
class Working_Days(db.Model):
    __tablename__='Working_Days'
    id=db.Column(db.Integer,primary_key=True)
    working_day=db.Column(db.String(300))
    def __init__(self,working_day):
        self.working_day=working_day
'''Create employee data table'''
class Employee_Data(db.Model):
    __tablename__="Employee_Data"
    id=db.Column(db.Integer,primary_key=True)
    Emp_ID =db.Column(db.String(300))
    Tin_Number = db.Column(db.String(300))
    Nssf_Number = db.Column(db.String(300))
    Designation=db.Column(db.String(300))
    Employee_Status = db.Column(db.String(300))
    Residence_type=db.Column(db.String(20))
    Joining_Date = db.Column(db.String(300))
    End_of_Contract = db.Column(db.String(300))
    Surname =db.Column(db.String(300))
    Given_name = db.Column(db.String(300))
    Othername = db.Column(db.String(300))
    DOB=db.Column(db.String(300))
    Marital_Status=db.Column(db.String(300))
    Gender =db.Column(db.String(300))
    Nationality = db.Column(db.String(300))
    Current_Address=db.Column(db.String(300))
    Mobile = db.Column(db.String(300))
    Home_Phone = db.Column(db.String(300))
    Email = db.Column(db.String(300))
    Account_Name = db.Column(db.String(300))
    Account_Number =db.Column(db.String(300))
    Bank_Name=db.Column(db.String(300))
    Bank_Branch = db.Column(db.String(300))
    Level_of_Education = db.Column(db.String(300))
    Award = db.Column(db.String(300))
    Institution = db.Column(db.String(300))
    Cv=db.Column(db.LargeBinary)
    Gross_Pay = db.Column(db.String(300))
    Next_of_Kin = db.Column(db.String(300))
    Supervisor=db.Column(db.String(300))
    Department=db.Column(db.String(300))
    Picture = db.Column(db.LargeBinary)
    def __init__(self,Emp_ID,Tin_Number,Nssf_Number,Designation,Employee_Status,Joining_Date,End_of_Contract,Surname,
                 Given_name,Othername,DOB,Marital_Status,Residence_type,Gender,Nationality,Current_Address,Mobile,
                 Home_Phone,Email,Account_Name,Account_Number,Bank_Name,Bank_Branch,
                 Level_of_Education,Award,Institution,Cv,Gross_Pay,Next_of_Kin,Supervisor,Department,Picture):
        self.Emp_ID=Emp_ID
        self.Tin_Number=Tin_Number
        self.Nssf_Number=Nssf_Number
        self.Designation=Designation
        self.Employee_Status=Employee_Status
        self.Residence_type=Residence_type
        self.Joining_Date=Joining_Date
        self.End_of_Contract=End_of_Contract
        self.Surname=Surname
        self.Given_name=Given_name
        self.Othername=Othername
        self.DOB=DOB
        self.Marital_Status=Marital_Status
        self.Gender=Gender
        self.Nationality=Nationality
        self.Current_Address=Current_Address
        self.Mobile=Mobile
        self.Home_Phone=Home_Phone
        self.Email=Email
        self.Account_Name=Account_Name
        self.Account_Number=Account_Number
        self.Bank_Name=Bank_Name
        self.Bank_Branch=Bank_Branch
        self.Level_of_Education=Level_of_Education
        self.Award=Award
        self.Institution=Institution
        self.Cv=Cv
        self.Gross_Pay=Gross_Pay
        self.Next_of_Kin=Next_of_Kin
        self.Supervisor=Supervisor
        self.Department=Department
        self.Picture=Picture
'''Create Department table'''
class Departments(db.Model):
    __tablename__ = 'Departments'
    id = db.Column(db.Integer, primary_key=True)
    Department = db.Column(db.String(300))

    def __init__(self, Department):
        self.Department = Department
'''Creating Register table'''
class Register(db.Model):
    __tablename__ = 'Register'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
# creating a db to the database
DATABASE = 'Database.db'
def getConnection():
    con = getattr(g, '_database', None)
    if con is None:
        con = g._database = sqlite3.connect(DATABASE)
    return con
'''Login Function'''
@app.route("/login_func", methods=["GET", "POST"])
def login_func():
    db = getConnection()
    c = db.cursor()
    if request.method == "POST":
        uname = request.form["username"]
        passw = request.form["password"]
        login = Register.query.filter_by(username=uname, password=hash_pass(passw)).first()
        others=c.execute('''select * from Roles where Employee_name=('{name}') AND Password=('{passw}')'''.format(name=uname,passw=hash_pass(passw)))
        login_others=others.fetchall()
        try:
            if login is not None:
                return redirect(url_for("index"))
            else:
                
                if login_others is not None:
                    if login_others[0][1] =="Finance":
                        return redirect(url_for('salary'))
                        # return redirect(url_for('department'))
                    if login_others[0][1]=="HR":
                        return redirect(url_for('department'))
                   
        except:
            
            render_template("login.html")
        
    return render_template("login.html")
'''User Login'''
@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")
'''Register user '''
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")
@app.route("/register_func", methods=["GET", "POST"])
def register_func():
    if request.method == "POST":
        uname = request.form['username']
        mail = request.form['email']
        passw = request.form['password']
        try:
            register = Register(username=uname, email=mail, password=hash_pass(passw))
            db.session.add(register)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            raise e
    return render_template("register.html")
'''Company image to all template html pages'''
def image():
    try:
        file = Company.query.filter_by(id=1).first()
        imgs = base64.b64encode(file.image).decode('ascii')
    except:
        imgs = "User"
    return imgs
'''Select company name'''
def com_name():
    try:
        file = Company.query.filter_by(id=1).first()
        cnames =file.cname
    except:
        cnames = ""
    return cnames
#create data
def add_data(name,rname,salary,vmonth,vyear,vdate):
    #a list for adding data into the finance module
    detail=[]
    db = getConnection()
    c = db.cursor()
    detail.append(name)
    detail.append(rname)
    detail.append(vmonth)
    detail.append(vyear)
    allowances=c.execute('''SELECT SUM(Amount) FROM Allowances WHERE Emp_ID=('{name}') OR (('{moth}') AND ('{yr}'))'''.format(name=name,moth=vmonth,yr=vyear))
    nets=allowances.fetchall()
    
    try:
        net_allowance=float(nets[0][0])
        
    except:
        net_allowance=0.0
        
        
    detail.append(net_allowance)
    try:
        mGross_pay = float(salary) + net_allowance
    except:
        mGross_pay = float(salary) + 0.0
    detail.append(mGross_pay)
    #     #calculate NSSf contribution
    #     #5% calculation
    employee_contrnssf = 0.05 * float(mGross_pay)
    detail.append(float(employee_contrnssf))
    # employer NSSf contribution)
    employeer_contrnssf = 0.1 * float(mGross_pay)
    detail.append(float(employeer_contrnssf))
    nssf_contribution = employee_contrnssf + employeer_contrnssf
    detail.append(nssf_contribution)

#     #calculate payee
    status=c.execute('''SELECT Residence_type FROM Employee_Data WHERE Emp_ID=('{name}')'''.format(name=name))
    bom=allowances.fetchall() 
    residence=bom[0][0]  
    if residence=='Yes':
        #Paye for residents
        if mGross_pay <235000:
            paye=0
                    
        elif mGross_pay in range(235000,335000):
            paye=0.1*mGross_pay
                    
        elif mGross_pay in range(335000,410000):
            paye=10000 + 0.2*mGross_pay
                
        elif mGross_pay >410000:
            paye=25000+0.3*mGross_pay
                    
        elif mGross_pay >10000000:
            paye=25000+0.3*mGross_pay+0.1*mGross_pay
                    
        else:
            print("Enter valid money for the employeee")

    elif residence== 'No':
        #paye for non residents
        if mGross_pay <335000:
            paye=0.1*mGross_pay
                    
        elif mGross_pay in range(335000,410000):
            paye=33500 + 0.2*mGross_pay
                    
        elif mGross_pay>410000:
            paye=48500+0.3*mGross_pay
                    
        elif mGross_pay>10000000:
            paye=48500+0.3*mGross_pay+0.1*mGross_pay
                    
        else:
            print("Enter valid money for the employeee")


    else:
        print("warning this field is required !!!")
    detail.append(paye)
    mtt_deductions = paye + nssf_contribution
    detail.append(mtt_deductions)
    deductions = c.execute(
        '''SELECT SUM(Amount) FROM Deduction WHERE Emp_ID=('{name}') OR (('{moth}') AND ('{yr}'))'''.format(name=name,
                                                                                                            moth=vmonth,
                                                                                                            yr=vyear))
    ded = deductions.fetchall()
    try:
        dect = float(ded[0][0])
    except:
        dect = 0.0
    detail.append(dect)
    try:
        cded = dect + mtt_deductions
        detail.append(cded)
        dnetpay = mGross_pay - cded
    except:
        dnetpay=mGross_pay-mtt_deductions
    detail.append(dnetpay) 
    detail.append(vdate)      
    arr=[str(i) for i in detail]
    detail_data = tuple(arr)
    
    c.execute('''Insert INTO Payment(Emp_ID,Emp_name,pmonth,pyear,tt_allowances,gross_pay,emp_contrib,emplry_contrib,nssf_contrib,paye,mdeduction,other_ded,ttded,net_pay,Issue_Date) VALUES {vdata}'''.format(vdata=detail_data))
            
    db.commit()
    db.close()
@app.route('/forgot')
def forgot():
    return render_template('forgot.html')
@app.route('/index',methods=['POST','GET'])
def index():
    imgs=image()
    cm = com_name()
    return render_template('index.html',img=imgs,cm=cm)
'''Creating a company profile'''
@app.route("/Profile", methods=["GET", "POST"])
def Profile():
    if request.method=='POST':
        image = request.files['image']
        img = image.read()
        Company_name = request.form['c_name']
        c_tin=request.form['c_tin']
        c_nssf_num = request.form['c_nssf']
        c_address = request.form['c_address']
        c_email = request.form['c_email']
        c_Tel = request.form['c_tel']
        ###insert data into the table in the sqlite database
        try:
            df = db.session.query(Company).filter_by(id=1).one()
            if df != []:
                df.cname =Company_name
                df.image = img
                df.Tin =c_tin
                df.nssf_number =c_nssf_num
                df.address = c_address
                df.email = c_email
                df.telephone =c_Tel
                db.session.add(df)
                db.session.commit()
                return redirect(url_for('index'))
        except:
            new_file = Company(cname=Company_name, Tin=c_tin, nssf_number=c_nssf_num, address=c_address, email=c_email,
                               telephone=c_Tel, image=img)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('index.html')
'''Edit company profile'''
@app.route('/Update_Profile',methods=['POST','GET'])
def Update_Profile():
    if request.method=='POST':
        image=request.files['Image']
        img = image.read()
        company_name=request.form['c_Name']
        nssf=request.form['c_Nssf']
        tin=request.form['c_Tin']
        address=request.form['c_Address']
        email=request.form['c_Email']
        tel = request.form['c_Tel']
        try:
            df = db.session.query(Company).filter_by(id=1).one()
            if df != []:
                df.cname = company_name
                df.image=img
                df.Tin= tin
                df.nssf_number = nssf
                df.address=address
                df.email=email
                df.telephone=tel
                db.session.add(df)
                db.session.commit()
                return redirect(url_for('index'))
        except Exception as  e:
            raise e
    return render_template('index.html')
'''Set working days'''
@app.route('/working_days',methods=['POST','GET'])
def working_days():
    if request.method=='POST':
        data = request.form.getlist("day")
        try:
            for d in data:
                new_file = Working_Days(working_day=d)
                db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            raise e
    return render_template('index.html')
'''Add a department to the database'''
@app.route('/add_department',methods=['POST','GET'])
def add_department():
    if request.method=='POST':
        dname=request.form['dname']
        list1 =dname.split(',')
        try:
            for d in list1:
                file = Departments.query.filter_by(Department=d).first()
                if file:
                    message = "Department exists"
                    flash(message)
                else:
                    new_file = Departments(Department=d)
                    db.session.add(new_file)
                    msg="Successfully inserted"
                    flash(msg)
            db.session.commit()
            return  redirect(url_for('department'))
        except Exception as e:
            raise e
    return render_template('department.html')
'''Fetch department data'''
@app.route('/department')
def department():
    imgs = image()
    cm=com_name()
    db = getConnection()
    c = db.cursor()
    query = c.execute('''SELECT  Department FROM  Departments''')
    rows = query.fetchall()
    db.commit()
    db.close()
    return render_template('department.html',rows=rows,img=imgs,cm=cm)
@app.route('/department_admin')
def department_admin():
    imgs = image()
    cm=com_name()
    db = getConnection()
    c = db.cursor()
    query = c.execute('''SELECT  Department FROM  Departments''')
    rows = query.fetchall()
    db.commit()
    db.close()
    return render_template('department_admin.html',rows=rows,img=imgs,cm=cm)
'''Route attendance '''
@app.route('/Attendance',methods=['POST','GET'])
def Attendance():
    imgs=image()
    cm=com_name()
    img_df = []
    users = Employee_Data.query.all()
    # # base64.b64encode(file.image).decode('ascii')
    for i in users:
        images=base64.b64encode(i.Picture).decode('ascii')
        img_df.append(images)
    user_zipped = zip(users,img_df)
    return  render_template('attendance.html',img=imgs,user_zipped=user_zipped,cm=cm)
'''Take attendance'''
@app.route('/Take_Attendance',methods=['POST','GET'])
def Take_Attendance():
    data=[]
    if request.method=='POST':
        today=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        for v in request.form:
            data.append(request.form[v])
        data.append(today)
        table_insert = tuple(data)
        db = getConnection()
        c=db.cursor()
        try:
            c.execute("""CREATE TABLE IF NOT EXISTS Attendance(Given_name VARCHAR(100) ,Attendance VARCHAR(100),Day_Date DATE)""")
            c.execute("""INSERT INTO Attendance(Given_name,Attendance,Day_Date) VALUES {tbv}""".format(tbv=table_insert))
            db.commit()
            db.close()
            return  redirect(url_for('Attendance'))
        except Exception as e:
            raise  e
    return render_template('attendance.html')
'''Delete department'''
@app.route('/Delete_Department',methods=['POST','GET'])
def Delete_Department():
    if request.method=='POST':
        depart=request.form['depart']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''DELETE FROM Departments WHERE Department=('{nm}') '''.format(nm=depart))
            db.commit()
            db.close()
            return redirect(url_for('department'))
        except Exception as e:
            raise e
    return  render_template('department.html')
@app.route('/Employee')
def Employee():
    imgs=image()
    cm=com_name()
    #connecting and selecting departments
    db=getConnection()
    c=db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Finances(Emp_ID VARCHAR(15),Employee_Name VARCHAR(100),Gross_pay VARCHAR(100),employee_contrb VARCHAR(100),employer_contrb VARCHAR(100),nssf_contrib VARCHAR(50),Paye VARCHAR(100),Total_Dect VARCHAR(100),Net_pay VARCHAR(100))''')
    query = c.execute('SELECT * FROM  Departments')
    rows = query.fetchall()
    db.commit()
    db.close()
    return render_template('employee.html',img=imgs,rows=rows,cm=cm)

@app.route('/Employee_admin')
def Employee_admin():
    imgs=image()
    cm=com_name()
    #connecting and selecting departments
    db=getConnection()
    c=db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Finances(Emp_ID VARCHAR(15),Employee_Name VARCHAR(100),Gross_pay VARCHAR(100),employee_contrb VARCHAR(100),employer_contrb VARCHAR(100),nssf_contrib VARCHAR(50),Paye VARCHAR(100),Total_Dect VARCHAR(100),Net_pay VARCHAR(100))''')
    query = c.execute('SELECT * FROM  Departments')
    rows = query.fetchall()
    db.commit()
    db.close()
    return render_template('employee_admin.html',img=imgs,rows=rows,cm=cm)

'''Adding an employee to the database'''
@app.route('/add_employee',methods=['POST','GET'])
def add_employee():
    if request.method=='POST':
        emp_id=request.form['emp_id']
        designation=request.form['designation']
        join_date=request.form['join_date']
        end_date=request.form['end_date']
        emp_status=request.form['emp_status']
        status=request.form['status']
        tin=request.form['tin']
        gross_pay=request.form['gross_pay']
        nssf=request.form['nssf']
        next_of_kin=request.form['next_of_kin']
        department=request.form['department']
        supervisor=request.form['supervisor']
        pic=request.files['pic']
        pic_image=pic.read()
        surname=request.form['surname']
        given_name=request.form['given_name']
        other_names=request.form['other_names']
        name=surname+" "+given_name
        marital_status=request.form['marital_status']
        nationality=request.form['nationality']
        date_of_birth=request.form['date_of_birth']
        gender=request.form['gender']
        account_name=request.form['account_name']
        account_number=request.form['account_number']
        bank_name=request.form['bank_name']
        bank_branch=request.form['bank_branch']
        level=request.form['level']
        award=request.form['award']
        instition=request.form['instition']
        cv=request.files['cv']
        cv_file=cv.read()
        current_address=request.form['current_address']
        mobile=request.form['mobile']
        phone=request.form['phone']
        email=request.form['email']
        try:
            data = Employee_Data(Emp_ID=emp_id,Joining_Date=join_date,End_of_Contract=end_date,Designation=designation,Employee_Status=emp_status,
                                 Residence_type=status,Tin_Number=tin,Gross_Pay=gross_pay,Nssf_Number=nssf,Next_of_Kin=next_of_kin,Department=department,
                                 Supervisor=supervisor,Picture=pic_image,Surname=surname,Given_name=given_name,Othername=other_names,Marital_Status=marital_status,
                                 Nationality=nationality,DOB=date_of_birth,Gender=gender,Account_Name=account_name,Account_Number=account_number,
                                 Bank_Name=bank_name,Bank_Branch=bank_branch,Level_of_Education=level,Award=award,Institution=instition,Cv=cv_file,
                                 Current_Address=current_address,Mobile=mobile,Home_Phone=phone,Email=email)
            db.session.add(data)

            db.session.commit()
            return redirect(url_for('Employee'))
        except Exception as e:
            raise e
    return render_template('employee.html')

'''Edit employee Details'''
'''Display employees in a table'''
@app.route('/Employee_list',methods=['POST','GET'])
def Employee_list():
    imgs=image()
    cm=com_name()
    users = Employee_Data.query.all()
    return render_template('employee_list.html',img=imgs,users=users,cm=cm)
'''Edit employee records'''
@app.route('/Edit_Employee',methods=['POST','GET'])
def Edit_Employee():
    imgs = image()
    cm = com_name()
    if request.method=="POST":
        id  = request.form['id']
        surname =request.form['surname']
        gname = request.form['gname']
        depart = request.form['depart']
        tin = request.form['tin']
        nssf =request.form['nssf']
        designation=request.form['designation']
        employee_status=request.form['employee_status']
        joining_date=request.form['joining_date']
        end_of_contract=request.form['end_of_contract']
        rtype=request.form['rtype']
        othername=request.form['othername']
        DOB=request.form['DOB']
        mstatus=request.form['mstatus']
        gender=request.form['gender']
        nationality=request.form['nationality']
        caddress=request.form['caddress']
        mobile=request.form['mobile']
        phone=request.form['phone']
        email=request.form['email']
        accname=request.form['accname']
        accnumber=request.form['accnumber']
        bname=request.form['bname']
        level=request.form['level']
        award=request.form['award']
        institution=request.form['institution']
        gpay=request.form['gpay']
        nkin=request.form['nkin']
        supervisor=request.form['supervisor']
        bbranch=request.form['bbranch']


    return render_template('edit_employee.html',img=imgs,cm=cm,id=id,surname=surname,gname=gname,depart=depart,tin=tin,nssf=nssf,designation=designation,employee_status=employee_status,
                           joining_date=joining_date,end_of_contract=end_of_contract,rtype=rtype,othername=othername,DOB=DOB,mstatus=mstatus,gender=gender,
                           nationality=nationality,caddress=caddress,mobile=mobile,phone=phone,email=email,accname=accname,accnumber=accnumber,bname=bname,
                           level=level,award=award,institution=institution,gpay=gpay,nkin=nkin,supervisor=supervisor,bbranch=bbranch)

'''Update Employee data '''
@app.route('/Update_Employee',methods=['POST','GET'])
def Update_Employee():
    if request.method == "POST":
        id = request.form['id']
        surname = request.form['surname']
        gname = request.form['gname']
        depart = request.form['depart']
        tin = request.form['tin']
        nssf = request.form['nssf']
        designation = request.form['designation']
        employee_status = request.form['employee_status']
        joining_date = request.form['joining_date']
        end_of_contract = request.form['end_of_contract']
        rtype = request.form['rtype']
        othername = request.form['othername']
        DOB = request.form['DOB']
        mstatus = request.form['mstatus']
        gender = request.form['gender']
        nationality = request.form['nationality']
        caddress = request.form['caddress']
        mobile = request.form['mobile']
        phone = request.form['phone']
        email = request.form['email']
        accname = request.form['accname']
        accnumber = request.form['accnumber']
        bname = request.form['bname']
        level = request.form['level']
        award = request.form['award']
        institution = request.form['institution']
        gpay = request.form['gpay']
        nkin = request.form['nkin']
        supervisor = request.form['supervisor']
        bbranch = request.form['bbranch']
        cv = request.files['cv']
        cv_file = cv.read()
        pic = request.files['pic']
        pic_image = pic.read()
        try:
            admin = Employee_Data.query.filter_by(Emp_ID=id).first()
            admin.Emp_ID = id
            admin.Surname = surname
            admin.Given_name = gname
            admin.Next_of_Kin = nkin
            admin.Joining_Date = joining_date
            admin.End_of_Contract = end_of_contract
            admin.Current_Address = caddress
            admin.Employee_Status = employee_status
            admin.Othername = othername
            admin.Tin_Number = tin
            admin.Nssf_Numebr = nssf
            admin.Account_Name = accname
            admin.Account_Number = accnumber
            admin.Level_of_Education = level
            admin.Gender = gender
            admin.Residence_type = rtype
            admin.Designation = designation
            admin.Supervisor = supervisor
            admin.Gross_Pay = gpay
            admin.Award = award
            admin.Nationality = nationality
            admin.Marital_Status = mstatus
            admin.Mobile = mobile
            admin.Home_Phone = phone
            admin.Department = depart
            admin.DOB = DOB
            admin.Email = email
            admin.Institution = institution
            admin.CV = cv_file
            admin.Picture = pic_image
            admin.Bank_Branch = bbranch
            admin.Bank_Name = bname
            db.session.commit()
            return redirect(url_for('Employee_list'))
        except Exception as e:
            raise e
    return render_template('edit_employee.html')
'''Screen lock'''
@app.route('/screen_lock')
def screen_lock():
    return  render_template('screen_lock.html')
'''Holidays , sick leave and vacation module'''
@app.route('/Leave',methods=['POST','GET'])
def Leave():
    imgs = image()
    cm=com_name()
    users = Employee_Data.query.all()
    return render_template('leave.html',img=imgs,sql_rows=users,cm=cm)
'''Set Holidays'''
@app.route('/Holidays',methods=['POST','GET'])
def Holidays():
    data = []
    if request.method=='POST':
        for fm in request.form:
            data.append(request.form[fm])
        form_values =tuple(data[:6])
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Holidays(Public_Holiday VARCHAR(4000) ,Public_Date DATE ,Personal_Event VARCHAR(100),Personal_Date DATE ,
            Company_Event VARCHAR(100),Company_Event_Date DATE )''')
            c.execute('Insert INTO Holidays(Public_Holiday,Public_Date,Personal_Event,Personal_Date,Company_Event,Company_Event_Date) VALUES {tbv}'.format(tbv=form_values))
            db.commit()
            db.close()
            return  redirect(url_for('Leave'))
        except Exception as e:
            raise e
    return render_template('leave.html')
'''Apply for sick leave '''
@app.route('/Sick_Leave',methods=['POST','GET'])
def Sick_Leave():
    imgs=image()
    if request.method=='POST':
        name=request.form['name']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        replacement=request.form['rep']
        db=getConnection()
        c=db.cursor()
        try:
            c.execute('''CREATE TABLE IF NOT EXISTS Sick_Leave(Employee_Name VARCHAR(100),Replacement VARCHAR(100),Start_Date DATE ,End_Date DATE)''')
            c.execute("Insert INTO Sick_Leave(Employee_Name,Replacement,Start_Date,End_Date) VALUES('{name}','{rep}','{start_date}','{end_date}')".format(name=name,rep=replacement,start_date=start_date,end_date=end_date))
            db.commit()
            db.close()
            return  redirect(url_for('Leave'))
        except Exception as e:
            raise e
    return render_template('leave.html',img=imgs)
@app.route('/salary')
def salary():
    db = getConnection()
    c = db.cursor()
    imgs=image()
    cm=com_name()
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
    try:
        query = c.execute('SELECT * FROM Payment')
        sql_rows = query.fetchall()

    except Exception as e:
        raise e
    return render_template('salary.html',sql_rows=sql_rows,img=imgs,cm=cm)
'''Apply for a vacation'''
@app.route('/Vacation',methods=['POST','GET'])
def Vacation():
    imgs=image()
    if request.method=='POST':
        name=request.form['name']
        start_date=request.form['start_date1']
        end_date=request.form['end_date1']
        replacement = request.form['replacement']
        db = getConnection()
        c = db.cursor()
        try:
            c.execute(
                '''CREATE TABLE IF NOT EXISTS Vacation(Employee_Name VARCHAR(4000),Replacement VARCHAR(100),Start_Date DATE ,End_Date DATE)''')
            c.execute(
                "Insert INTO Vacation(Employee_Name,Replacement,Start_Date,End_Date) VALUES('{name}','{rep}','{start_date}','{end_date}')".format(
                    name=name, rep=replacement, start_date=start_date, end_date=end_date))
            db.commit()
            db.close()
            return redirect(url_for('Leave'))
        except Exception as e:
            raise e
    return render_template('leave.html', img=imgs)
'''User settings'''
@app.route('/settings', methods=['POST', 'GET'])
def settings():
    imgs = image()
    cm=com_name()
    db = getConnection()
    c = db.cursor()
    d = db.cursor()
    users = Employee_Data.query.all()
    try:
        query = c.execute('SELECT * FROM Roles')
        rows = query.fetchall()
        depart = d.execute('SELECT Department FROM Departments')
        depart_row = depart.fetchall()
    except:
        c.execute(
            '''CREATE TABLE IF NOT EXISTS Roles(Employee_name VARCHAR(100),Role VARCHAR(100),Password VARCHAR(100),Department VARCHAR(100))''')
        db.commit()
        return redirect('settings')
    db.close()
    return render_template('settings.html', rows=rows, sql_rows=users, depart_row=depart_row, img=imgs,cm=cm)
'''Assign Role'''
@app.route('/Role', methods=['POST', 'GET'])
def Role():
    imgs = image()
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        password = request.form['password']
        department = request.form['department']
        try:
            db = getConnection()
            c = db.cursor()
            c.execute(
                """INSERT INTO Roles(Employee_name,Role,Password,Department) VALUES('{name}','{role}','{password}','{department}')""".
                format(name=name, role=role, password=hash_pass(password), department=department))
            db.commit()
            db.close()
            return redirect(url_for('settings'))
        except Exception as e:
            raise e
    return render_template('settings.html', img=imgs)
'''Change password'''
@app.route('/Change_Password', methods=['POST', 'GET'])
def Change_Password():
    imgs = image()
    if request.method == 'POST':
        name = request.form['name']
        npassword = request.form['npassword']
        db = getConnection()
        c = db.cursor()
        try:
            c.execute(
                '''UPDATE Roles SET Password =('{ps}') WHERE Employee_name=('{nm}')'''.format(ps=hash_pass(npassword), nm=name))
            db.commit()
            db.close()
            return redirect(url_for('settings'))
        except Exception as e:
            raise e
    return render_template('settings.html', img=imgs)
'''Delete user role'''
@app.route('/Delete_User', methods=['POST', 'GET'])
def Delete_User():
    if request.method == 'POST':
        name = request.form['name']
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''DELETE FROM Roles WHERE Employee_name=('{nm}') '''.format(nm=name))
            db.commit()
            db.close()
            return redirect(url_for('settings'))
        except Exception as e:
            raise e
    return render_template('settings.html')
#delete deduction
@app.route('/delete_dd',methods=['POST','GET'] )
def delete_dd():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        nmonth = request.form['nmonth']
        nyear = request.form['nyear']
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''DELETE FROM Deduction WHERE Emp_id=('{nm}')  OR (('{moth}') AND ('{yr}'))'''.format(nm=emp_id,moth=nmonth,yr=nyear))
            db.commit()
            db.close()
            return redirect(url_for('deductions'))
        except Exception as e:
            raise e
    return render_template('deductions.html')
#delete allowances 
@app.route('/delete_allow',methods=['POST','GET'])
def delete_allow():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        nmonth = request.form['nmonth']
        nyear = request.form['nyear']
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''DELETE FROM Allowances WHERE Emp_id=('{nm}')  OR (('{moth}') AND ('{yr}'))'''.format(nm=emp_id,moth=nmonth,yr=nyear))
            db.commit()
            db.close()
            return redirect(url_for('allowances'))
        except Exception as e:
            raise e
    return render_template('allowances.html')
@app.route('/allowances')
def allowances():
    imgs = image()
    cm = com_name()
    db = getConnection()
    c = db.cursor()
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
    try:
        # select employe name from employee table
        erows = c.execute('SELECT * FROM Employee_Data')
        serows = erows.fetchall()
        # select allowance type from allowance type table
        atype = c.execute('SELECT * FROM Allowance_types')
        arows = atype.fetchall()
        # select allownaces
        query = c.execute('SELECT * FROM Allowances')
        allowance_rows = query.fetchall()
    except Exception as e:
        c = db.cursor()
        #creat allowances table is not existing
        
        c.execute('''CREATE TABLE IF NOT EXISTS Allowances(Emp_id VARCHAR(15),Emp_name VARCHAR(30),Allowance_type VARCHAR(100),month VARCHAR(15),year VARCHAR(15),Amount VARCHAR(100))''')
        #create employee table is not exist
        #create allowance type  table is not exist
        c.execute('''CREATE TABLE IF NOT EXISTS Allowance_types(Allowance_type VARCHAR(100),description VARCHAR(100))''')
        db.commit()
        return redirect(url_for('allowances'))
    return render_template('allowances.html', data1=allowance_rows, arows=arows, serows=serows, img=imgs, cm=cm)
@app.route('/add_allowance',methods=('POST','GET'))
def add_allowance():
    dallowance=[]
    if request.method=='POST':
        atype=request.form['a_type']
        dallowance.append(atype)
        cdescr=request.form['descr']
        dallowance.append(cdescr)
        arr4=[str(i) for i in dallowance]
        dallowance_data = tuple(arr4)
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''INSERT INTO Allowance_types(Allowance_type,description)  VALUES {table_value}'''.format(table_value=dallowance_data))
            db.commit()
            db.close()
        except Exception as e:
            raise e

    return  redirect(url_for('allowances'))
@app.route('/issue_allowance', methods=('POST', 'GET'))
def issue_allowance():
    db = getConnection()
    c = db.cursor()
    allowance = []
    if request.method == 'POST':
        emp_name = request.form['a_empname']
        allowance.append(emp_name)
        #get employye name
        depart = c.execute('''SELECT * FROM Employee_Data WHERE Emp_ID=('{nd}')'''.format(nd=emp_name))
        depart_row = depart.fetchall()
        for i in depart_row:
            lname=i[9]
            mname=i[10]
            
        rname=lname +" "+ mname
        allowance.append(rname)
        allowance_type=request.form['a_type']
        allowance.append(allowance_type)
        Issue_date = request.form['a_date']
        allowance.append(Issue_date)
        Issue_year = request.form['year']
        allowance.append(Issue_year)
        amt = request.form['a_ammount']
        allowance.append(amt)
        arr2 = [str(i) for i in allowance]
        allowance_data = tuple(arr2)
        
        try:
            c.execute('''INSERT INTO Allowances(Emp_id,Emp_name,Allowance_type,month,year,Amount)  VALUES {table_values}'''.format(table_values=allowance_data))
            db.commit()
            db.close()
            return redirect(url_for('allowances'))
        except Exception as e:
            raise e

    return render_template('allowances.html')
@app.route('/deductions')
def deductions():
    imgs = image()
    cm = com_name()
    db = getConnection()
    c = db.cursor()
    try:
        # select employe name from employee table
        erows = c.execute('SELECT * FROM Employee_Data')
        serows = erows.fetchall()
        # select allowance type from allowance type table
        dtype = c.execute('SELECT * FROM Deduction_types')
        drows = dtype.fetchall()
        # select allownaces
        query = c.execute('SELECT * FROM  Deduction')
        adeduction_rows = query.fetchall()
       
    except:
        c = db.cursor()
        #creat allowances table is not existing
        c.execute('''CREATE TABLE IF NOT EXISTS Deduction(Emp_id VARCHAR(15),Emp_name VARCHAR(30),deduction_type VARCHAR(100),month VARCHAR(15),year VARCHAR(15),Amount VARCHAR(100))''')
        #create employee table is not exist
        #create allowance type  table is not exist
        c.execute('''CREATE TABLE IF NOT EXISTS Deduction_types(Deduction_type VARCHAR(100),Description VARCHAR(100))''')
        db.commit()
        return redirect(url_for('deductions'))
    db.close()
    return render_template('deductions.html', adeduction_rows=adeduction_rows, drows=drows, serows=serows, img=imgs,
                           cm=cm)
@app.route('/add_deduction',methods=['POST','GET'])
def add_deduction():
    dd=[]
    if request.method=='POST':
        dtype=request.form['d_type']
        dd.append(dtype)
        descrip=request.form['descip']
        dd.append(descrip)

        arr4=[str(i) for i in dd]
        dd_data = tuple(arr4)
        db = getConnection()
        c = db.cursor()
        try:
            c.execute('''INSERT INTO Deduction_types(Deduction_type,Description)  VALUES {table_value}'''.format(table_value=dd_data))
            db.commit()
            db.close()
        except Exception as e:
            raise e

    return  redirect(url_for('deductions'))
@app.route('/compute_deduction', methods=['POST', 'GET'])
def compute_deduction():
    edd = []
    imgs=image()
    cm=com_name()
    db = getConnection()
    c = db.cursor()
    if request.method == 'POST':
        emp_name = request.form['a_empname']
        edd.append(emp_name)
        #get employye name
        depart = c.execute('''SELECT * FROM Employee_Data WHERE Emp_ID=('{nd}')'''.format(nd=emp_name))
        depart_row = depart.fetchall()
        for i in depart_row:
            lname=i[9]
            mname=i[10]
            
        rname=lname +" "+ mname
        edd.append(rname)
        allowance_type=request.form['d_type']
        edd.append(allowance_type)
        Issue_date = request.form['a_date']
        edd.append(Issue_date)
        
        Issue_year=request.form['year']
        edd.append(Issue_year)

        amt = request.form['a_ammount']
        edd.append(amt)
        arr2 = [str(i) for i in edd]
        edd_data = tuple(arr2)
        
        try:
            
            c.execute('''INSERT INTO Deduction(Emp_id,Emp_name,deduction_type,month,year,Amount)  VALUES {table_values}'''.format(table_values=edd_data))
            db.commit()
            return redirect(url_for('deductions'))
        except Exception as e:
            raise e
    return render_template('deductions.html', img=imgs, cm=cm)
@app.route('/pay')
def pay():
    imgs = image()
    cm = com_name()
    # file = Data.query.filter_by(id=1).first()
    # img = base64.b64encode(file.image).decode('ascii')
    try:
        db = getConnection()
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Payment(Emp_ID VARCHAR(100),Emp_name VARCHAR(30),pmonth VARCHAR(15),pyear VARCHAR(15),tt_allowances VARCHAR(10),gross_pay VARCHAR(20),emp_contrib VARCHAR(20),emplry_contrib VARCHAR(20),nssf_contrib VARCHAR(20),paye VARCHAR(20),mdeduction VARCHAR(20),other_ded VARCHAR(20),ttded VARCHAR(20),net_pay VARCHAR(20),Issue_Date DATE)''')
        
        depart = c.execute('SELECT * FROM Employee_Data')
        depart_row = depart.fetchall()
        db.commit()
        

    except Exception as e:
        raise e
        return redirect(url_for('pay'))


    return render_template('pay.html',Finance=depart_row,img=imgs,cm=cm)
@app.route('/add_tpaylist',methods=['POST','GET'])
def add_tpaylist():
    imgs = image()
    cm = com_name()
    db = getConnection()
    c = db.cursor()
    if request.method=='POST':
        name=request.form['emp_id']
        #get employye name
        depart = c.execute('''SELECT * FROM Employee_Data WHERE Emp_ID=('{nd}')'''.format(nd=name))
        depart_row = depart.fetchall()
        for i in depart_row:
            lname=i[9]
            mname=i[10]
            
        rname=lname +" "+ mname
        
        emdata = c.execute('''SELECT Gross_Pay FROM Employee_Data WHERE Emp_ID=('{nd}')'''.format(nd=name))
        rdata =  emdata.fetchall()
        salary=rdata[0][0]
        
        vmonth=request.form['vMonth']
        
        vyear=request.form['vyear']
        
        vdate=request.form['vdate']

        try:
            add_data(name,rname,salary,vmonth,vyear,vdate)
            return redirect(url_for('pay'))
        except Exception as e:
            raise e
    return render_template('pay.html', img=imgs, cm=cm)
@app.route('/gen_slip', methods=['POST', 'GET'])
def gen_slip():
    imgs = image()
    cm = com_name()
    if request.method == 'POST':
        db = getConnection()
        c = db.cursor()
        new_data=request.form['myFile']
        nmonth=request.form['sMonth']
        nyear=request.form['year']
        emdata = c.execute('''SELECT * FROM Employee_Data WHERE Emp_ID=('{nd}')'''.format(nd=new_data))
        rdata =  emdata.fetchall()
        crows=Company.query.all()
        
            
        gpayment = c.execute('''SELECT * FROM Payment WHERE Emp_ID=('{name}') OR (('{moth}') AND ('{yr}'))'''.format(name=new_data,moth=nmonth,yr=nyear))
        rf_list = gpayment.fetchall()

        return render_template('dis_slip.html',crows=crows,rdata=rdata,rf_list=rf_list,img=imgs, cm=cm)
#generate pay-slip page
@app.route('/create_pay')
def create_pay():
    db = getConnection()
    c = db.cursor()
    imgs=image()
    cm=com_name()
    pay_list = c.execute('SELECT * FROM Payment')
    dpay_list = pay_list.fetchall()
    return render_template('gen_slip.html',pay_list=dpay_list,cm=cm,img=imgs)
#NSSF submission
@app.route('/nssf')
def nssf():
    imgs=image()
    cm=com_name()
    return render_template('nssf_subf.html',img=imgs,cm=cm)
@app.route('/nssf_sub', methods=['POST', 'GET'])
def nssf_sub():
    if request.method=='POST':
        syear=request.form['year']
        submonth=request.form['sMonth']
        
        db = getConnection()
        c = db.cursor()
        # company_details=c.execute('SELECT * FROM  Artistry')
        crows = Company.query.all()
        for i in crows:
            cname = i.cname
            nssf_number = i.nssf_number
        ford = c.execute("""SELECT  Employee_Data.Emp_ID,
        Employee_Data.Emp_ID,Employee_Data.Nssf_Number,
        Employee_Data.Residence_type,Payment.Emp_name,
        Payment.gross_pay,Payment.emp_contrib,Payment.emplry_contrib,
        Payment.nssf_contrib,Employee_Data.Mobile FROM Payment JOIN Employee_Data ON(Payment.Emp_ID=Employee_Data.Emp_ID)  WHERE Payment.pmonth=('{nmonth}') AND  Payment.pYear=('{yr}')"""
                         .format(nmonth=submonth, yr=syear))
        drows = ford.fetchall()
        
        #sum
        tsum=c.execute("select SUM(nssf_contrib)from Payment WHERE Payment.pmonth=('{nmonth}') AND Payment.pyear=('{nyear}')".format(nmonth=submonth,nyear=syear))
        tsumval = tsum.fetchall()
        try:
            ttr = float(tsumval[0][0])
        except:
            ttr=0.0
        
        output=BytesIO()
        
        workbook = xlsxwriter.Workbook(output)
        # writing excel headers
        workbook.formats[0].set_bold()
        workbook.formats[0].set_font_size(10)
        workbook.formats[0].set_font_name('Arial')
        

        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:J',20)
        cell_format = workbook.add_format({'color':'blue'})
        #cell background colors
        bcel_format=workbook.add_format({'bg_color':'#C6EFCE','font_size':'10'})
        wcel_format=workbook.add_format({'bg_color':'#C5EADA','font_size':'10'})
        
        ncel_format=workbook.add_format({'bg_color':'#ff4f33','font_size':'10'})
     #create a format to use in the merged range
        cell_format.set_font_color('Sliver')
        coname=cname
        nssf=nssf_number
        
        # print(tsumval[0][0])
    
        nmembers=len(drows)
        year=syear
        nMonth=submonth
        merge_format=workbook.add_format({'bold':1,'border':1,'align':'center','valign':'vcenter','color':'blue'})
        # merge_format2=workbook.add_format({'fg_color':'sliver'})
        #merge 7 cells
        worksheet.merge_range('A1:H1','NATIONAL SOCIAL SECURITY FUND',merge_format)
        worksheet.merge_range('A2:H2','MONTHLY SCHEDULE',merge_format)
        worksheet.merge_range('A3:H3','C-SPEED MOBILE',merge_format)
        worksheet.write('C6','Company Name')
        worksheet.write('C7','Company NSSF Number')
        worksheet.write('C8','Total Amount')
        worksheet.write('C9','No.of members')
        worksheet.write('D6',coname,bcel_format)
        worksheet.write('D7',nssf,bcel_format)
        worksheet.write('D8',ttr,wcel_format)
        worksheet.write('D9',nmembers,wcel_format)
        worksheet.write('E6','Year')
        worksheet.write('E7','Month')
        worksheet.write('F6',year,bcel_format)
        worksheet.write('F7',nMonth,bcel_format)
        #legend
        worksheet.write('G4','Legend')
        worksheet.merge_range('G5:H5','Calculated Protected',wcel_format)
        worksheet.merge_range('G6:H6','Required',bcel_format)
        worksheet.merge_range('G7:H7','Optional',ncel_format)
        #contribution
        worksheet.write('I3','NORMAL',wcel_format)
        worksheet.write('I4','BONUS',wcel_format)
        worksheet.write('I5','ARREAR',wcel_format)
        worksheet.write('I6','MULTIPLE',wcel_format)
        worksheet.write('I7','10%CONTRIBUTION',wcel_format)
        worksheet.write('I8','5%CONTRIBUTION',wcel_format)
        worksheet.write('I9','SPECIAL CONTRIBUTION',wcel_format)
        worksheet.write('I10','INTEREST',wcel_format)
        #Description
        worksheet.write('J2','DESCRIPTION',wcel_format)
        worksheet.write('J3','15% normal contribution',wcel_format)
        worksheet.write('J4','15% bonus contribution',wcel_format)
        worksheet.write('J5','15% arrear contribution',wcel_format)
        worksheet.write('J6','15% contributions paid more than once',wcel_format)
        worksheet.write('J7','10% contribution',wcel_format)
        worksheet.write('J8','5% contribution',wcel_format)
        worksheet.write('J9','Special contribution',wcel_format)
        worksheet.write('J10','Interest contribution',wcel_format)
        #column headers
        worksheet.write('A12','NO')
        worksheet.write('B12','NationalID/StaffNo',ncel_format)
        worksheet.write('C12','Employee NSSF Number',bcel_format)
        worksheet.write('D12','Contribution Type',bcel_format)
        worksheet.write('E12','Employee Names',bcel_format)
        worksheet.write('F12','Employee Gross Pay',bcel_format)
        worksheet.write('G12','Employee Contribution',wcel_format)
        worksheet.write('H12','Employer Contribution',wcel_format)
        worksheet.write('I12','Total Contribution',wcel_format)
        worksheet.write('J12','Telephone Number',ncel_format)
        #add values to the file
        
        for i, row in enumerate(drows):
            for j, value in enumerate(row):
                worksheet.write(i+12, j, row[j])
        workbook.close() 
        #go back to the beginning of the stream
        output.seek(0)
        
  
    # return redirect(url_for('nssf'))
    return send_file(output, attachment_filename="nssf.xlsx", as_attachment=True)
# Create password hashes
def hash_pass(passw):
	m = hashlib.md5()
	m.update(passw.encode('utf-8'))
	return m.hexdigest()
if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run()

# db.create_all()
# db.session.commit()
# ui.run()
