import base64
import datetime
import sqlite3
from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, g, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
autoflush = True
db = SQLAlchemy(app)
'''
    Create Company profile table
'''

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

'''
    Create a working days table
'''
class Working_Days(db.Model):
    __tablename__='Working_Days'
    id=db.Column(db.Integer,primary_key=True)
    working_day=db.Column(db.String(300))
    def __init__(self,working_day):
        self.working_day=working_day
'''
    Create employee data table
'''
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


'''
    Create Department table
'''


class Departments(db.Model):
    __tablename__ = 'Departments'
    id = db.Column(db.Integer, primary_key=True)
    Department = db.Column(db.String(300))

    def __init__(self, Department):
        self.Department = Department


'''
    Creating Register table
'''


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


'''
 Login Function
'''


@app.route("/login_func", methods=["GET", "POST"])
def login_func():
    if request.method == "POST":
        uname = request.form["username"]
        passw = request.form["password"]
        login = Register.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("index"))
    return render_template("login.html")


'''
 User Login
'''


@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")


'''
 Register user 
'''


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
            register = Register(username=uname, email=mail, password=passw)
            db.session.add(register)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            raise e
    return render_template("register.html")


'''
    Company image to all template html pages
'''


def image():
    try:
        file = Company.query.filter_by(id=1).first()
        imgs = base64.b64encode(file.image).decode('ascii')
    except:
        imgs = "User"
    return imgs


@app.route('/forgot')
def forgot():
    return render_template('forgot.html')
@app.route('/index',methods=['POST','GET'])
def index():
    imgs=image()
    return render_template('index.html',img=imgs)
'''
    Creating a company profile
'''
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
            new_file=Company(cname=Company_name,Tin=c_tin,nssf_number=c_nssf_num,address=c_address,email=c_email,telephone=c_Tel,image=img)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            raise e
    return render_template('index.html')
'''
    Edit company profile
'''
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
'''
    Set working days
'''
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
'''
    Add a department to the database
'''
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
'''
    Fetch department data
'''
@app.route('/department')
def department():
    imgs = image()
    db = getConnection()
    c = db.cursor()
    query = c.execute('''SELECT  Department FROM  Departments''')
    rows = query.fetchall()
    print(rows)
    db.commit()
    db.close()
    return render_template('department.html',rows=rows,img=imgs)
'''
    Route attendance 
'''
@app.route('/Attendance',methods=['POST','GET'])
def Attendance():
    imgs=image()
    img_df = []
    users = Employee_Data.query.all()
    # # base64.b64encode(file.image).decode('ascii')
    for i in users:
        images=base64.b64encode(i.Picture).decode('ascii')
        img_df.append(images)
    user_zipped = zip(users,img_df)
    return  render_template('attendance.html',img=imgs,user_zipped=user_zipped)
'''
    Take attendance
'''
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
'''
    Delete department
'''
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
    return render_template('employee.html',img=imgs)
'''
    Adding an employee to the database
'''
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
'''
    Display employees in a table
'''
@app.route('/Employee_list',methods=['POST','GET'])
def Employee_list():
    imgs=image()
    users = Employee_Data.query.all()
    return render_template('employee_list.html',img=imgs,users=users)
'''
    Screen lock
'''
@app.route('/screen_lock')
def screen_lock():
    return  render_template('screen_lock.html')
'''
    Holidays , sick leave and vacation module
'''
@app.route('/Leave',methods=['POST','GET'])
def Leave():
    imgs = image()
    users = Employee_Data.query.all()
    return render_template('leave.html',img=imgs,sql_rows=users)
'''
    Set Holidays
'''
@app.route('/Holidays',methods=['POST','GET'])
def Holidays():
    data = []
    if request.method=='POST':
        for fm in request.form:
            data.append(request.form[fm])
        form_values =tuple(data[:6])
        print(form_values)
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

'''
    Apply for sick leave 
'''
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


'''
    Apply for a vacation
'''
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


'''
    User settings
'''


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    imgs = image()
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
    return render_template('settings.html', rows=rows, sql_rows=users, depart_row=depart_row, img=imgs)


'''
    Assign Role
'''


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
                format(name=name, role=role, password=password, department=department))
            db.commit()
            db.close()
            return redirect(url_for('settings'))
        except Exception as e:
            raise e
    return render_template('settings.html', img=imgs)


'''
    Change password
'''


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
                '''UPDATE Roles SET Password =('{ps}') WHERE Employee_name=('{nm}')'''.format(ps=npassword, nm=name))
            db.commit()
            db.close()
            return redirect(url_for('settings'))
        except Exception as e:
            raise e
    return render_template('settings.html', img=imgs)


'''
    Delete user role
'''


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


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True)
