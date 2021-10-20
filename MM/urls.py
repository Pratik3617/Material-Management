"""MM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import EmployeeView
from . import CategoryView
from . import SubcategoryView
from . import productView
from . import finalProductsView
from . import AdminView
from . import SupplierView
from . import PurchaseView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('adminlogin/',AdminView.AdminLogin),
    path('checkadminlogin',AdminView.CheckAdminLogin),
    path('adminlogout/', AdminView.AdminLogout),

    path('employeelogin/',EmployeeView.EmployeeLogin),
    path('employeeInterface/',EmployeeView.EmployeeInterface),
    path('fetchallStates/',EmployeeView.FetchAllStates),
    path('fetchallCities/',EmployeeView.FetchAllCities),
    path('submitemployeeDetails',EmployeeView.SubmitEmployeeDetails),
    path('displayallEmployee/',EmployeeView.displayAllEmployee),
    path('employeebyId/',EmployeeView.EmployeeById),
    path('editdeleteEmployeeRecord/', EmployeeView.EditDeleteEmployeeRecord),
    path('editemployeepicture/', EmployeeView.EditEmployeePicture),
    path('savepicture', EmployeeView.SavePicture),

    path('categoryInterface/',CategoryView.categoryInterface),
    path('submitCategory',CategoryView.SubmitCategory),
    path('displayallCategories/',CategoryView.displayAllCategories),
    path('categorybyId/',CategoryView.CategoryById),
    path('editdeleteCategory/',CategoryView.EditDeleteCategory),
    path('editIcon/',CategoryView.EditIcon),
    path('saveicon',CategoryView.SaveIcon),
    path('categoryjson/',CategoryView.CategoryJSON),


    path('subcategoryInterface/',SubcategoryView.subcategoryInterface),
    path('submitsubCategory',SubcategoryView.SubmitsubCategory),
    path('displayallSubCategories/',SubcategoryView.displayAllSubCategories),
    path('subcategorybyId/',SubcategoryView.SubCategoryById),
    path('editdeletesubCategory/',SubcategoryView.EditDeleteSubCategory),
    path('editsubcategoryicon/',SubcategoryView.EditSubcategoryIcon),
    path('savesubcategoryicon',SubcategoryView.SaveSubcategoryIcon),
    path('subcategoryjson/',SubcategoryView.SubcategoryJSON),

    path('productInterface/',productView.productInterface),
    path('submitProduct',productView.SubmitProduct),
    path('displayallProducts/',productView.displayAllProducts),
    path('productbyId/',productView.ProductById),
    path('editdeleteProduct/',productView.EditDeleteProduct),
    path('editproductpicture/',productView.EditProductPicture),
    path('saveproductpicture',productView.SaveProductPicture),
    path('productjson/',productView.ProductJSON),

    path('finalProducts/', finalProductsView.FinalProducts),
    path('submitFinalProducts',finalProductsView.SubmitFinalProducts),
    path('displayFinalProducts/',finalProductsView.DisplayFinalProducts),
    path('finalproductsbyId/',finalProductsView.FinalProductsbyId),
    path('editdeleteFinalProduct/',finalProductsView.EditDeleteFinalProduct),
    path('editFinalproductpicture/',finalProductsView.EditFinalProductPicture),
    path('saveFinalproductpicture',finalProductsView.SaveFinalProductPicture),

    path('purchaseInterface/', PurchaseView.PurchaseInterface),
    path('fetchallFinalProduct/', PurchaseView.FetchAllFinalProduct),
    path('submitPurchase/', PurchaseView.SubmitPurchase),
    path('displayallPurchase/', PurchaseView.DisplayAllPurchase),
    path('editdeletePurchaseData/', PurchaseView.EditDeletePurchaseData),
    path('fetchallSupplier/', PurchaseView.FetchAllSupplier),

    path('supplierInterface/',SupplierView.SupplierInterface),
    path('submitSupplier/', SupplierView.SubmitSupplier),
    path('displayallSupplier/', SupplierView.DisplayAllSupplier),
    path('editdeleteSupplierData/', SupplierView.EditDeleteSupplierData),

]
