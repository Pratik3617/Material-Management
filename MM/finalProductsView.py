from django.shortcuts import render
from . import pool
import uuid
import os

def FinalProducts(request):
    return render(request,"FinalProducts.html")

def SubmitFinalProducts(request):
    try:
        db,cmd=pool.connectionPool()
        categoryId=request.POST['categoryId']
        subcategoryId=request.POST['subcategoryId']
        productId=request.POST['productId']
        finalProductName=request.POST['finalProductName']
        size=request.POST['size']
        sizeUnit=request.POST['sizeUnit']
        weight=request.POST['weight']
        weightUnit=request.POST['weightUnit']
        color=request.POST['color']
        price=request.POST['price']
        stock=request.POST['stock']

        picture = request.FILES['picture']
        filename = str(uuid.uuid4()) + picture.name[picture.name.rfind('.'):]

        q="insert into finalproducts (categoryId,subcategoryId,productId,finalProductName,size,sizeUnit,weight,weightUnit,color,price,stock,picture) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')".format(categoryId,subcategoryId,productId,finalProductName,size,sizeUnit,weight,weightUnit,color,price,stock,filename)

        cmd.execute(q)
        db.commit()
        F = open("D:/MM/assets/Images/" + filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return render(request, "FinalProducts.html", {'status': True})
    except Exception as e:
        print("error:",e)
        return render(request, "FinalProducts.html", {'status': False})

def DisplayFinalProducts(request):
    try:

        db, cmd = pool.connectionPool()
        q = "select FP.*,(select C.categoryName from category C where C.categoryId=FP.categoryId),(select S.subcategoryName from subcategory S where S.subcategoryId=FP.subcategoryId),(select P.productName from product P where P.productId=FP.productId) from finalproducts FP"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,"displayFinalProducts.html",{'rows':rows})
    except Exception as e:
        print("errror:",e)
        return render(request,"displayFinalProducts.html",{'rows':[]})



def FinalProductsbyId(request):
    try:
        db,cmd=pool.connectionPool()
        fpid=request.GET['fpid']

        q="select F.*,(select C.categoryName from category C where C.categoryId=F.categoryId),(select S.subcategoryName from subcategory S where S.subcategoryId=F.subcategoryId),(select P.productName from product P where P.productId=F.productId),from finalproducts F where finalProductId='{}'".format(fpid)
        cmd.execute(q)
        row=cmd.fetchone()
        db.close()
        return render("FinalProducts.html",{'row':row})
    except Exception as e:
        print("err:",e)
        return render("FinalProducts.html", {'row':[]})

def EditDeleteFinalProduct(request):
    try:
        db,cmd=pool.connectionPool()
        fpid=request.GET['fpid']
        btn=request.GET['btn']
        if(btn=="edit"):
            categoryId = request.GET['categoryId']
            subcategoryId = request.GET['subcategoryId']
            productId = request.GET['productId']
            finalProductName = request.GET['finalProductName']
            size = request.GET['size']
            sizeUnit = request.GET['sizeUnit']
            weight = request.GET['weight']
            weightUnit = request.GET['weightUnit']
            color = request.GET['color']
            price = request.GET['price']
            stock = request.GET['stock']
            q = "update finalproducts set categoryId='{}',subcategoryId='{}',productId='{}',finalProductName='{}',size='{}',sizeUnit='{}',weight='{}',weightUnit='{}',color='{}',price='{}',stock='{}' where finalProductId='{}'".format(categoryId, subcategoryId,productId,finalProductName,size,sizeUnit,weight,weightUnit,color,price,stock,fpid)
            cmd.execute(q)
            db.commit()
            db.close()
            return DisplayFinalProducts(request)
        elif(btn=='delete'):
            q="delete finalproducts where finalProductId='{}'".format(fpid)
            cmd.execute(q)
            db.commit()
            db.close()
            return DisplayFinalProducts(request)
    except Exception as e:
        print("err:",e)
        return DisplayFinalProducts(request)

def EditFinalProductPicture(request):
    try:
        fpid=request.GET['fpid']
        finalProductName=request.GET['finalProductName']
        picture=request.GET['picture']
        row=[fpid,finalProductName,picture]
        return render(request,"displayFinalProducts.html",{'row':row})
    except Exception as e:
        print('er:',e)
        return render(request, "displayFinalProducts.html", {'row': []})

def SaveFinalProductPicture(request):
    try:
        db,cmd=pool.connectionPool()
        fpid = request.POST['fpid']
        oldpicture=request.POST['oldpicture']
        picture=request.FILES['picture']
        filename = str(uuid.uuid4()) +picture.name[picture.name.rfind('.'):]
        q = "update finalproducts set picture='{}' where finalProductId='{}'".format(filename, fpid)
        cmd.execute(q)
        db.commit()
        F = open("D:/MM/assets/Images/" + filename, "wb")
        for chunk in picture.chunks():
            F.write(chunk)
        F.close()
        db.close()
        os.remove("D:/MM/assets/Images/" + oldpicture)
        return DisplayFinalProducts(request)

    except Exception as e:
        print("err:", e)
        return DisplayFinalProducts(request)

