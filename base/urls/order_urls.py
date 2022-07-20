from django.urls import path
from base.views import order_views as views

urlpatterns =[
	path('', views.getOrders, name='orders'),
	path('simpleorders/', views.getSimpleOrders, name='simple-orders'),
	path('simpleorders/add/', views.addSimpleOrderItems, name='simpleorders-add'),
	path('add/', views.addOrderItems, name='orders-add'),
	path('myorders/', views.getMyOrders, name='myorders'),
	path('<str:pk>/deliver/', views.updateOrderToDelivered, name='order-delivered'),
	path('<str:pk>/simpledeliver/', views.updateSimpleOrderToDelivered, name='simpleorder-delivered'),
	path('<str:pk>/', views.getOrderById, name='user-order'),
	path('simpleorder/<str:pk>/', views.getSimpleOrderById, name='simpleorder-items'),
	path('<str:pk>/pay/', views.updateOrderToPaid, name='pay'),
]