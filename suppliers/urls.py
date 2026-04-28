from django.urls import path
from . import views

urlpatterns = [
    path("", views.suppliers, name="suppliers"),
    path("supplier/", views.supplier, name="supplier"),
    path("create_supplier/", views.create_supplier, name="create_supplier"),
    path("edit_supplier/<int:pk>/", views.edit_supplier, name="edit_supplier"),
    path("delete_supplier/<int:pk>/", views.delete_supplier, name="delete_supplier"),
    path("rate_supplier/", views.rate_supplier, name="rate_supplier"),
    path("categories/", views.categories, name="categories"),
    path('categories/delete/<int:sub_id>/', views.delete_subcategory, name='delete_subcategory'),
    path('supplier/<int:supplier_id>/', views.supplier, name='supplier'),
    path("<int:supplier_id>/review/", views.rate_supplier, name="rate_supplier"),
    path("<int:supplier_id>/review/delete/", views.delete_review, name="delete_review"),
]
