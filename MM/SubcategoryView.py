from django.shortcuts import render
from . import pool
import uuid
import os
from django.http import JsonResponse
import random

def subcategoryInterface(request):
    return render(request,"subcategoryInterface.html")

def SubmitsubCategory(request):
    try:
        db,cmd=pool.connectionPool()
        categoryId=request.POST['categoryId']
        subcategoryName = request.POST['subcategoryName']
        description = request.POST['description']
        icon=request.FILES['icon']
        filename=str(uuid.uuid4())+icon.name[icon.name.rfind('.'):]
        q="insert into subcategory (categoryId,subcategoryName,description,icon) values('{0}','{1}','{2}','{3}')".format(categoryId,subcategoryName,description,filename)
        cmd.execute(q)
        db.commit()
        F=open("D:/MM/assets/Images/"+filename,"wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return render(request,"subcategoryInterface.html",{'status':True})
    except Exception as e:
        print("error:",e)
        return render(request, "subcategoryInterface.html", {'status': False})

def displayAllSubCategories(request):
    try:
        db,cmd=pool.connectionPool()
        q="select S.*,(select C.categoryName from category C where C.categoryId=S.categoryId)from subcategory S"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,"displayAllSubcategories.html",{'rows':rows})
    except Exception as e:
        print("error:",e)
        return render(request,"displayAllSubcategories.html",{'rows':[]})

def SubCategoryById(request):
    try:
        db,cmd=pool.connectionPool()
        scid=request.GET['scid']
        q="select S.*,(select C.categoryName from category C where C.categoryId=S.categoryId) from subcategory S where subcategoryId='{}'".format(scid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render(request,"SubcategoryById.html",{'row':row})
    except Exception as e:
        print("error:",e)
        return render(request, "SubcategoryById.html", {'row': []})

def EditDeleteSubCategory(request):
    try:
        db,cmd=pool.connectionPool()
        scid=request.GET['scid']
        btn=request.GET['btn']
        if(btn=="edit"):
            categoryId = request.GET['categoryId']
            subcategoryName = request.GET['subcategoryName']
            description = request.GET['description']
            q = "update subcategory set categoryId='{}',subcategoryName='{}',description='{}' where subcategoryId='{}'".format(categoryId, subcategoryName, description,scid)
            cmd.execute(q)
            db.commit()
            db.close()
            return displayAllSubCategories(request)
        elif(btn=='delete'):
            q="delete subcategory where subcategoryId='{}'".format(scid)
            cmd.execute(q)
            db.commit()
            db.close()
            return displayAllSubCategories(request)
    except Exception as e:
        print("err:",e)
        return displayAllSubCategories(request)

def EditSubcategoryIcon(request):
    try:
        scid=request.GET['scid']
        subcategoryName=request.GET['subcategoryName']
        icon=request.GET['icon']
        row=[scid,subcategoryName,icon]
        return render(request,"displayAllSubcategories.html",{'row':row})
    except Exception as e:
        print("errr:",e)
        return render(request,"displayAllSubcategories.html",{'row':[]})

def SaveSubcategoryIcon(request):
    try:
        db,cmd=pool.connectionPool()
        scid = request.POST['scid']
        oldicon=request.POST['oldicon']
        icon=request.FILES['icon']
        filename = str(uuid.uuid4()) + icon.name[icon.name.rfind('.'):]
        q = "update subcategory set icon='{}' where subcategoryId='{}'".format(filename, scid)
        cmd.execute(q)
        db.commit()
        F = open("D:/MM/assets/Images/" + filename, "wb")
        for chunk in icon.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove("D:/MM/assets/Images/" + oldicon)
        return displayAllSubCategories(request)

    except Exception as e:
        print("err:", e)
        return displayAllSubCategories(request)

def SubcategoryJSON(request):
    try:
        db,cmd=pool.connectionPool()
        cid=request.GET['cid']
        q="select * from subcategory where categoryId='{}'".format(cid)
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print('er:',e)
        return JsonResponse([],safe=False)

