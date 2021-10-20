from django.shortcuts import render
from . import pool
from django.http import JsonResponse
import uuid
import random
import os

def EmployeeLogin(request):
    return render(request,"EmployeeLogin.html")


def EmployeeInterface(request):
    return render(request,"EmployeeInterface.html")

def FetchAllStates(request):
    try:
        db,cmd=pool.connectionPool()
        q="select * from states"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print("error:",e)
        return JsonResponse([],safe=False)

def FetchAllCities(request):
    try:
        db,cmd=pool.connectionPool()
        state=request.GET['state']
        q="select * from cities where stateId='{}'".format(state)
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print("err:",e)
        return JsonResponse([],safe=False)

def SubmitEmployeeDetails(request):
    try:
        db,cmd=pool.connectionPool()
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        gender=request.POST['gender']
        dob=request.POST['dob']
        paddress = request.POST['paddress']
        state = request.POST['state']
        city = request.POST['city']
        caddress = request.POST['caddress']
        email = request.POST['email']
        mobileno = request.POST['mobileno']
        designation = request.POST['designation']
        picture=request.FILES['picture']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]    #generate random file names
        password="".join(random.sample(['1','2','3','4','5','6','7','8','9','0','@','$','#','a','b','x','d','h','r'],k=7))


        q="insert into employee (firstname,lastname,gender,dob,paddress,state,city,caddress,email,mobileno,designation,picture,password) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')".format(fname,lname,gender,dob,paddress,state,city,caddress,email,mobileno,designation,filename,password)
        cmd.execute(q)
        db.commit()

        F=open("D:/MM/assets/Images/"+filename,"wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()

        db.close()
        return render(request,"EmployeeInterface.html",{'status':True})
    except Exception as e:
        print("error:",e)
        return render(request,"EmployeeInterface.html",{'status':False})


def displayAllEmployee(request):
    try:
        db,cmd=pool.connectionPool()
        q="select E.*,(select C.cityName from cities C where C.cityId=E.city),(select S.stateName from states S where S.stateId=E.state) from employee E"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,"displayAllEmployee.html",{'rows':rows})
    except Exception as e:
        print("error:",e)
        return render(request,"displayAllEmployee.html",{'rows':[]})

def EmployeeById(request):
    try:
        db,cmd=pool.connectionPool()
        eid=request.GET['eid']
        q="select E.* ,(select C.cityName from cities C where C.cityId=E.city),(select S.stateName from states S where S.stateId=E.state) from employee E where employeeId={}".format(eid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request,"EmployeeById.html",{'row':row})
    except Exception as e:
        print("error:",e)
        return render(request,"EmployeeById.html",{'row':[]})

def EditDeleteEmployeeRecord(request):
    try:
        btn=request.GET['btn']
        db,cmd=pool.connectionPool()
        if(btn=="Edit"):
            eid = request.GET['eid']
            fname = request.GET['firstname']
            lname = request.GET['lastname']
            gender = request.GET['gender']
            dob = request.GET['dob']
            paddress = request.GET['paddress']
            state = request.GET['state']
            city = request.GET['city']
            caddress = request.GET['caddress']
            email = request.GET['email']
            mobileno = request.GET['mobileno']
            designation = request.GET['designation']
            q = "update employee set firstname='{}',lastname='{}',gender='{}',dob='{}',paddress='{}',state='{}',city='{}',caddress='{}',email='{}',mobileno='{}',designation='{}' where employeeId='{}'".format(fname, lname, gender, dob, paddress,state,city,caddress,email,mobileno,designation,eid)
            cmd.execute(q)
            db.commit()
            db.close()
            return displayAllEmployee(request)
        elif(btn=="Delete"):
            eid = request.GET['eid']
            q="delete from employee where employeeId='{}'".format(eid)
            cmd.execute(q)
            db.commit()
            db.close()
            return displayAllEmployee(request)
    except Exception as e:
        print("err:",e)
        return render(request,"EmployeeById.html",{'status':False})

def EditEmployeePicture(request):
    try:
        eid=request.GET['eid']
        firstname=request.GET['firstname']
        lastname=request.GET['lastname']
        picture=request.GET['picture']
        row=[eid,firstname,lastname,picture]
        return render(request,"EditPicture.html",{'row':row})
    except Exception as e:
        print("error:",e)
        return render(request,"EditPicture.html",{'row':[]})

def SavePicture(request):
    try:
        eid = request.POST['eid']
        oldpicture=request.POST['oldpicture']
        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]
        q = "update employee set picture='{}' where employeeId={}".format(filename,eid)
        db, cmd = pool.connectionPool()
        cmd.execute(q)
        db.commit()
        F = open("D:/MM/assets/Images/" + filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()

        db.close()
        os.remove('D:/MM/assets/Images/' + oldpicture)
        return displayAllEmployee(request)

    except Exception as e:
        return displayAllEmployee(request)