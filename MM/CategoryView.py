from django.shortcuts import render
from . import pool
import uuid
import os
from django.http import JsonResponse


from django.http import JsonResponse
import random

def categoryInterface(request):
    return render(request,"categoryInterface.html")

def SubmitCategory(request):
    try:
        db,cmd=pool.connectionPool()
        categoryName=request.POST['categoryName']
        icon=request.FILES['icon']
        filename=str(uuid.uuid4())+icon.name[icon.name.rfind('.'):]
        q="insert into category (categoryName,icon) values('{0}','{1}')".format(categoryName,filename)
        cmd.execute(q)
        db.commit()
        F=open("D:/MM/assets/Images/"+filename,"wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return render(request,"categoryInterface.html",{'status':True})
    except Exception as e:
        print("error:",e)
        return render(request, "categoryInterface.html", {'status': False})

def displayAllCategories(request):
    try:
        db,cmd=pool.connectionPool()
        q="select * from category"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,"displayAllCategories.html",{'rows':rows})
    except Exception as e:
        print("error:",e)
        return render(request,"displayAllCategories.html",{'rows':[]})

def CategoryById(request):
    try:
        db,cmd=pool.connectionPool()
        cid=request.GET['cid']
        q="select * from category where categoryId='{}'".format(cid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request,'CategoryById.html',{'row':row})
    except Exception as e:
        print("error:",e)
        return render(request,'CategoryById.html',{'row':[]})

def EditDeleteCategory(request):
    try:
        db,cmd=pool.connectionPool()

        cid=request.GET['cid']
        btn=request.GET['btn']

        if(btn=="edit"):
            categoryName = request.GET['categoryName']
            q = "update category set categoryName='{}' where categoryId='{}'".format(categoryName,cid)
            cmd.execute(q)
            db.commit()
            db.close()
            return displayAllCategories(request)
        elif(btn=="delete"):
            q="delete category where categoryId='{}'".format(cid)
            db.commit()
            db.close()
            return displayAllCategories(request)
    except Exception as e:
        print('err:',e)
        return displayAllCategories(request)

def EditIcon(request):
    try:
        categoryName=request.GET['categoryName']
        cid = request.GET['cid']
        icon = request.GET['icon']
        row=[categoryName,icon,cid]
        return render(request,'displayAllCategories.html',{'row':row})
    except Exception as e:
        print('errr:',e)
        return render(request, 'displayAllCategories.html', {'row': []})
def SaveIcon(request):
    try:
        db, cmd = pool.connectionPool()

        cid = request.POST['cid']
        oldicon=request.POST['oldicon']
        icon = request.FILES['icon']
        filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]
        q = "update category set icon='{}' where categoryId='{}'".format(filename,cid)
        cmd.execute(q)
        db.commit()
        F = open("D:/MM/assets/Images/" + filename, "wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove("D:/MM/assets/Images/" + oldicon)
        return displayAllCategories(request)
    except Exception as e:
        print("err:",e)
        return displayAllCategories(request)

def CategoryJSON(request):
    try:
        db,cmd=pool.connectionPool()
        q="select * from category"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print("e:",e)
        return JsonResponse([],safe=False)
