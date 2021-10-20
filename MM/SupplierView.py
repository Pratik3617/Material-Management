from django.shortcuts import render
from . import pool

def SupplierInterface(request):
    return render(request,"SupplierInterface.html")

def SubmitSupplier(request):
    try:
        db,cmd=pool.connectionPool()
        suppliername=request.GET['suppliername']
        emailid=request.GET['emailid']
        mobileno=request.GET['mobileno']
        address=request.GET['address']
        state=request.GET['state']
        city=request.GET['city']
        q="insert into supplier (suppliername, emailid, mobileno, address, state, city) values('{}','{}','{}','{}','{}','{}')".format(suppliername, emailid, mobileno, address, state, city)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request,"SupplierInterface.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"SupplierInterface.html",{'status':False})

def DisplayAllSupplier(request):
    try:
        db,cmd=pool.connectionPool()
        q="select s.*,(select S.stateName from states S where S.stateId=s.state),(select C.cityName from cities C where C.cityid=s.city) from supplier s"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,"DisplayAllSupplier.html",{'rows':rows})
    except Exception as e:
        print('rror:',e)
        return render(request,"DisplayAllSupplier.html",{'rows':[]})

def EditDeleteSupplierData(request):
    try:
        db,cmd=pool.connectionPool()
        btn=request.GET['btn']
        spid=request.GET['spid']
        if(btn=="Edit"):
          suppliername = request.GET['suppliername']
          emailid = request.GET['emailid']
          mobileno = request.GET['mobileno']
          address = request.GET['address']
          state = request.GET['state']
          city = request.GET['city']
          q="update supplier set suppliername='{}',emailid='{}',mobileno='{}',address='{}',state='{}',city='{}' where supplierid={}".format(suppliername,emailid,mobileno,address,state,city,spid)
          cmd.execute(q)
          db.commit()
          db.close()
        elif(btn=="Delete"):
            q="delete from supplier where supplierid={}".format(spid)
            cmd.execute(q)
            db.commit()
            db.close()
        return DisplayAllSupplier(request)
    except Exception as e:
        print('error:',e)
        return DisplayAllSupplier(request)
