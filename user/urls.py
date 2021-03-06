from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
    path('orders/', views.user_orders, name='user_orders'),
    path('orders_product/', views.user_orders_product, name='user_orders_product'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),
    path('export_csv/<int:id>', views.export_csv, name='export-csv'),
    path('export_excel/<int:id>', views.export_excel, name='export-excel'),
    path('export_pdf/<int:id>', views.export_pdf, name='export-pdf'),
]