from django.shortcuts import render
from django.http import JsonResponse
from . import pool


def PurchaseInterface(request):
    return render(request,"PurchaseInterface.html")

def FetchAllFinalProduct(request):
    try:
        db,cmd=pool.connectionPool()
        productId=request.GET['pid']
        q="select * from finalproducts where productId='{}'".format(productId)
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print('error:',e)
        return JsonResponse([],safe=False)

def SubmitPurchase(request):
    try:
        db,cmd=pool.connectionPool()
        employeeId=request.GET['employeeId']
        categoryId=request.GET['categoryId']
        subcategoryId=request.GET['subcategoryId']
        productId=request.GET['productId']
        finalproductId=request.GET['finalproductId']
        date=request.GET['date']
        supplierId=request.GET['supplierId']
        stock=request.GET['stock']
        amount=request.GET['amount']
        q="insert into purchase ( employeeId, categoryId, subcategoryId, productId, finalproductId, date, supplierId, stock, amount) values({},{},{},{},{},'{}',{},'{}','{}')".format(employeeId, categoryId, subcategoryId, productId, finalproductId, date, supplierId, stock, amount)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request,"PurchaseInterface.html",{'status':True})
    except Exception as e:
        print('error:',e)
        return render(request,"PurchaseInterface.html",{'status':False})


def DisplayAllPurchase(request):
    try:
        db,cmd=pool.connectionPool()
        q = "select p.*,(select C.categoryName from category C where C.categoryId=p.categoryId),(select S.subcategoryName from subcategory S where S.subcategoryId=p.subcategoryId),(select P.productName from product P where P.productId=p.productId),(select F.finalproductName from finalproducts F where F.finalproductId=p.finalproductId) from purchase p"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return render(request,"DisplayAllPurchase.html",{'rows':rows})
    except Exception as e:
        return render(request,"DisplayAllPurchase.html",{'rows':[]})

def EditDeletePurchaseData(request):
    try:
        db,cmd=pool.connectionPool()
        btn=request.GET['btn']
        transactionId=request.GET['transactionId']
        if(btn=="Edit"):
          employeeId = request.GET['employeeId']
          categoryId = request.GET['categoryId']
          subcategoryId = request.GET['subcategoryId']
          productId = request.GET['productId']
          finalproductId = request.GET['finalproductId']
          date = request.GET['date']
          supplierId = request.GET['supplierId']
          stock = request.GET['stock']
          amount = request.GET['amount']
          q="update purchase set employeeId={},categoryId={},subcategoryId={},productId={},finalproductId={},date='{}',supplierId={},stock='{}',amount='{}' where transactionId={}".format(employeeId,categoryId,subcategoryId,productId,finalproductId,date,supplierId,stock,amount,transactionId)
          cmd.execute(q)
          db.commit()
        elif(btn=="Delete"):
            q="delete from purchase where transactionId={}".format(transactionId)
            cmd.execute(q)
            db.commit()
        db.close()
        return DisplayAllPurchase(request)
    except Exception as e:
        print('error:',e)
        return DisplayAllPurchase(request)

def FetchAllSupplier(request):
    try:
        db,cmd=pool.connectionPool()
        q="select * from supplier"
        cmd.execute(q)
        rows=cmd.fetchall()
        db.close()
        return JsonResponse(rows,safe=False)
    except Exception as e:
        print('error:',e)
        return JsonResponse([],safe=False)
