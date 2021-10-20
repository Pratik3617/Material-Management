from django.shortcuts import render
from . import pool
import uuid
import os
from django.http import JsonResponse
import random

def productInterface(request):
    return render(request,"productInterface.html")

def SubmitProduct(request):
    try:
        db,cmd=pool.connectionPool()
        categoryId=request.POST['categoryId']
        subcategoryId = request.POST['subcategoryId']
        productName = request.POST['productName']
        description = request.POST['description']
        picture=request.FILES['picture']
        filename=str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        q="insert into product (categoryId,subcategoryId,productName,description,picture) values('{0}','{1}','{2}','{3}','{4}')".format(categoryId,subcategoryId,productName,description,filename)
        cmd.execute(q)
        db.commit()
        F=open("D:/MM/assets/Images/"+filename,"wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return render(request,"productInterface.html",{'status':True})
    except Exception as e:
        print("error:",e)
        return render(request, "productInterface.html", {'status': False})


def displayAllProducts(request):
    try:
        db,cmd=pool.connectionPool()
        q="select P.*,(select C.categoryName from category C where C.categoryId=P.categoryId),(select S.subcategoryName from subcategory S where S.subcategoryId=P.subcategoryId) from product P"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,"displayAllProducts.html",{'rows':rows})
    except Exception as e:
        print("error:",e)
        return render(request,"displayAllProducts.html",{'rows':[]})

def ProductById(request):
    try:
        db,cmd=pool.connectionPool()
        pid=request.GET['pid']
        q = "select P.*,(select C.categoryName from category C where C.categoryId=P.categoryId),(select S.subcategoryName from subcategory S where S.subcategoryId=P.subcategoryId) from product P where productId='{}'".format(pid)
        cmd.execute(q)
        row = cmd.fetchone()
        db.close()
        print(row)
        return render(request, "displayAllProducts.html", {'row': row})
    except Exception as e:
        print("error:", e)
        return render(request, "displayAllProducts.html", {'row': []})

def EditDeleteProduct(request):
    try:
        db,cmd=pool.connectionPool()
        pid=request.GET['pid']
        btn=request.GET['btn']
        if(btn=="edit"):
            categoryId = request.GET['categoryId']
            subcategoryId = request.GET['subcategoryId']
            productName=request.GET['productName']
            description = request.GET['description']
            q = "update product set categoryId='{}',subcategoryId='{}',productName='{}',description='{}' where productId='{}'".format(categoryId, subcategoryId,productName, description,pid)
            cmd.execute(q)
            db.commit()
            db.close()
            return displayAllProducts(request)
        elif(btn=='delete'):
            q="delete product where productId='{}'".format(pid)
            cmd.execute(q)
            db.commit()
            db.close()
            return displayAllProducts(request)
    except Exception as e:
        print("err:",e)
        return displayAllProducts(request)

def EditProductPicture(request):
    try:
        pid=request.GET['pid']
        productName=request.GET['productName']
        picture=request.GET['picture']
        row=[pid,productName,picture]
        return render(request,"displayAllProducts.html",{'row':row})
    except Exception as e:
        print('er:',e)
        return render(request, "displayAllProducts.html", {'row': []})

def SaveProductPicture(request):
    try:
        db,cmd=pool.connectionPool()
        pid = request.POST['pid']
        oldpicture=request.POST['oldpicture']
        picture=request.FILES['picture']
        filename = str(uuid.uuid4()) +picture.name[picture.name.rfind('.'):]
        q = "update product set picture='{}' where productId='{}'".format(filename, pid)
        cmd.execute(q)
        db.commit()
        F = open("D:/MM/assets/Images/" + filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove("D:/MM/assets/Images/" + oldpicture)
        return displayAllProducts(request)

    except Exception as e:
        print("err:", e)
        return displayAllProducts(request)

def ProductJSON(request):
    try:
        db, cmd = pool.connectionPool()
        scid = request.GET['scid']
        q = "select * from product where subcategoryId='{}'".format(scid)
        cmd.execute(q)
        rows = cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print("e:",e)
        return JsonResponse([], safe=False)
