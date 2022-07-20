from django.urls import path
from base.views import product_views as views


urlpatterns = [
	path('', views.getProducts, name="products"),

	path('create/', views.createProduct, name="product-create"),

	path('upload/', views.uploadImage, name="image-upload"),

	path('banners/', views.getBanners, name="banners"),

	path('settings/', views.getSettings, name="settings"),

	path('categories/', views.getCategories, name="categories"),

	path('categories/<str:pk>/', views.getCategoryProducts, name="category"),

	path('top/', views.getTopProducts, name="product-top"),

	path('selected/', views.getSalesProducts, name="product-sales"),

	path('settings/update/', views.updateSettings, name="settings-update"),

	path('gender/male/', views.getMaleProducts, name='gender-male'),
	path('gender/female/', views.getFemaleProducts, name='gender-female'),
	path('gender/kids/', views.getKidsProducts, name='gender-kids'),

	path('<str:pk>/reviews/', views.createProductReview, name="product-review"),

	path('<str:pk>/', views.getProduct, name="product"),

	path('update/<str:pk>/', views.updateProduct, name="product-update"),

	path('delete/<str:pk>/', views.deleteProduct, name="product-delete"),
]