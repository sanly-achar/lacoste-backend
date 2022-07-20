from django.db import models
from django.contrib.auth.models import User

class Settings(models.Model):
	course 					= models.FloatField('Course', default=1)
	company         		= models.CharField('Firmanyň ady', max_length=50, default='CompanyName')
	logo_main            	= models.ImageField('Firma Logotip 1-5', blank=True, upload_to='images/')
	logo_secondary          = models.ImageField('Firma Logotip 1-1', blank=True, upload_to='images/')
	slogan          		= models.CharField('Slogan', blank=True, null=True, max_length=255)
	description 			= models.TextField(null=True, blank=True)
	ht_order 				= models.TextField(null=True, blank=True)
	ht_register 			= models.TextField(null=True, blank=True)
	address         		= models.CharField('Firmanyň adresi', blank=True, max_length=255)
	phone           		= models.CharField('Telefon', blank=True, max_length=15)
	email           		= models.CharField('Email', blank=True, max_length=50)
	instagram       		= models.CharField('Instagram Link', blank=True, max_length=250)
	created_at      		= models.DateTimeField('Döredilen Sene', auto_now_add=True)
	_id						= models.AutoField(primary_key=True, editable=False)

	def __str__(self):
		return str(self.company)

class Banner(models.Model):
	name					= models.CharField(max_length=200, null=True, blank=True)
	image					= models.ImageField(null=True, blank=True, default='/banner_default.jpg')
	createdAt				= models.DateTimeField(auto_now_add=True)
	_id						= models.AutoField(primary_key=True, editable=False)

	def __str__(self):
		return str(self.name)

class Category(models.Model):
	name 					= models.CharField(max_length=200, null=True, blank=True, default='Category')
	icon					= models.ImageField(null=True, blank=True, default='/placeholder.jpg')
	description 			= models.TextField(null=True, blank=True)
	_id						= models.AutoField(primary_key=True, editable=False)

	def __str__(self):
		return str(self.name)

class Product(models.Model):
	GENDER = (
		('Male', 'Male'),
		('Female', 'Female'),
		('Kids', 'Kids'),
	)
	user 					= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	name					= models.CharField(max_length=200, null=True, blank=True)
	image					= models.ImageField(null=True, blank=True, default='/placeholder.jpg')
	brand 					= models.CharField(max_length=200, null=True, blank=True, default='Lacoste')
	category				= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	gender          		= models.CharField(max_length=10, choices=GENDER, default='Male')
	isInSale 				= models.BooleanField(default=False)
	description 			= models.TextField(null=True, blank=True)
	rating					= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	numReviews				= models.IntegerField(null=True, blank=True, default=0)
	price					= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	countInStock			= models.IntegerField(null=True, blank=True, default=50)
	createdAt				= models.DateTimeField(auto_now_add=True)
	_id						= models.AutoField(primary_key=True, editable=False)

	def __str__(self):
		return str(self.name)

class Review(models.Model):
	product 				= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	user 					= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	name					= models.CharField(max_length=200, null=True, blank=True)
	rating 					= models.IntegerField(null=True, blank=True, default=0)
	comment 				= models.TextField(null=True, blank=True)
	createdAt 				= models.DateTimeField(auto_now_add=True)
	_id						= models.AutoField(primary_key=True, editable=False)

	def __str__(self):
		return str(self.rating)

class Order(models.Model):
	user 					= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	paymentMethod 			= models.CharField(max_length=200, null=True, blank=True)
	taxPrice				= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	shippingPrice 			= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	totalPrice 				= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	isPaid 					= models.BooleanField(default=False)
	paidAt 					= models.DateTimeField(auto_now_add=False, null=True, blank=True)
	isDelivered				= models.BooleanField(default=False)
	deliveredAt				= models.DateTimeField(auto_now_add=False, null=True, blank=True)
	createdAt 				= models.DateTimeField(auto_now_add=True)
	_id						= models.AutoField(primary_key=True, editable=False)

	def __str__(self):
		return str(self.createdAt)

class OrderItem(models.Model):
	product 				= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order					= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	name					= models.CharField(max_length=200, null=True, blank=True)
	qty						= models.IntegerField(null=True, blank=True, default=0)
	price					= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	image					= models.CharField(max_length=200, null=True, blank=True)
	_id						= models.AutoField(primary_key=True, editable=False)

	def __str__(self):
		return str(self.name)

class ShippingAddress(models.Model):
	order					= models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
	mobile					= models.CharField(max_length=200, null=True, blank=True)
	address					= models.CharField(max_length=200, null=True, blank=True)
	city					= models.CharField(max_length=200, null=True, blank=True)
	postalCode				= models.CharField(max_length=200, null=True, blank=True)
	country					= models.CharField(max_length=200, null=True, blank=True)
	shippingPrice			= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	_id						= models.AutoField(primary_key=True, editable=False)

	def __str__(self):
		return str(self.address)


# This is edited for ordering without registering, only with mobile and preferably with name
####################################################################################################

class SimpleOrder(models.Model):
	mobile					= models.CharField(max_length=200)
	name 					= models.CharField(max_length=200, null=True, blank=True)
	totalPrice 				= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	isDelivered				= models.BooleanField(default=False)
	createdAt 				= models.DateTimeField(auto_now_add=True)
	_id						= models.AutoField(primary_key=True, editable=False)

	def __str__(self):
		return str(self.mobile)

class SimpleOrderItem(models.Model):
	product 				= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order					= models.ForeignKey(SimpleOrder, on_delete=models.SET_NULL, null=True)
	name					= models.CharField(max_length=200, null=True, blank=True)
	qty						= models.IntegerField(null=True, blank=True, default=0)
	price					= models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	image					= models.CharField(max_length=200, null=True, blank=True)
	_id						= models.AutoField(primary_key=True, editable=False)

	def __str__(self):
		return str(self.product.name)
# ###################################################################################################