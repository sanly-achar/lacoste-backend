from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from base.models import Product, Order, OrderItem, ShippingAddress, SimpleOrder, SimpleOrderItem
from base.serializers import ProductSerializer, OrderSerializer, SimpleOrderItemSerializer, SimpleOrderSerializer

from rest_framework import serializers, status

from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
	user = request.user
	data = request.data

	orderItems = data['orderItems']

	if orderItems and len(orderItems) == 0:
		return Response({'detail': 'Sargyt harydy ýok'}, status=status.HTTP_400_BAD_REQUEST)
	else:
		# (1) Create Order
		order = Order.objects.create(
			user=user,
			paymentMethod = data['paymentMethod'],
			shippingPrice = data['shippingPrice'],
			totalPrice = data['totalPrice']
		)

		# (2) Create shipping address
		shipping = ShippingAddress.objects.create(
			order = order,
			mobile = data['shippingAddress']['mobile'],
			address = data['shippingAddress']['address'],
			city = data['shippingAddress']['city'],
			postalCode = data['shippingAddress']['postalCode'],
			country = data['shippingAddress']['country'],
		)

		# (3) Create order items and set order to orderItem relationship
		for i in orderItems:
			product = Product.objects.get(_id=i['product'])
			item = OrderItem.objects.create(
				product = product,
				order=order,
				name = product.name,
				qty = i['qty'],
				price=i['price'],
				image=product.image.url,
			)

			# (4) Update stock
			product.countInStock -= item.qty
			product.save()

		serializer = OrderSerializer(order, many=False)
		print(serializer.data)
		data = serializer.data
		return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

	user = request.user

	try:
		order = Order.objects.get(_id=pk)
		if user.is_staff or order.user == user:
			serializer = OrderSerializer(order, many=False)
			return Response(serializer.data)
		else:
			Response({'detail':'Bu sargydy görmänä rugsadyňyz ýok.'}, status=status.HTTP_400_BAD_REQUEST)
	except:
		return Response({'detail':'Beýle sargyt ýok.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
	user = request.user
	orders = user.order_set.all()
	serializer = OrderSerializer(orders, many=True)
	return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
	orders =Order.objects.all().order_by('-createdAt')
	serializer = OrderSerializer(orders, many=True)
	return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
	order = Order.objects.get(_id=pk)

	order.isPaid = True
	order.paidAt = datetime.now()
	order.save()

	return Response('Sargyt Tölendi')

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
	order = Order.objects.get(_id=pk)

	order.isDelivered = True
	order.deliveredAt = datetime.now()
	order.save()

	return Response('Sargyt Eltip berildi')


############################################################

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getSimpleOrders(request):
	orders =SimpleOrder.objects.all().order_by('-createdAt')
	serializer = SimpleOrderSerializer(orders, many=True)
	return Response(serializer.data)


@api_view(['POST'])
def addSimpleOrderItems(request):
	data = request.data

	orderItems = data['orderItems']

	if orderItems and len(orderItems) == 0:
		return Response({'detail': 'Sargyt harytlary ýok'}, status=status.HTTP_400_BAD_REQUEST)
	else:
		# (1) Create Order
		order = SimpleOrder.objects.create(
			mobile = data['mobile'],
			name = data['clientName'],
			totalPrice = data['totalPrice']
		)


		# (3) Create order items and set order to orderItem relationship
		for i in orderItems:
			product = Product.objects.get(_id=i['product'])
			item = SimpleOrderItem.objects.create(
				product = product,
				order=order,
				name = product.name,
				qty = i['qty'],
				price=i['price'],
				image=product.image.url,
			)

			# (4) Update stock
			# product.countInStock -= item.qty
			product.save()

		serializer = SimpleOrderSerializer(order, many=False)
		print(serializer.data)
		data = serializer.data
		return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSimpleOrderById(request, pk):

	user = request.user

	try:
		order = SimpleOrder.objects.get(_id=pk)
		if user.is_staff or order.user == user:
			serializer = SimpleOrderSerializer(order, many=False)
			return Response(serializer.data)
		else:
			Response({'detail':'Bu sargydy görmänä rugsadyňyz ýok.'}, status=status.HTTP_400_BAD_REQUEST)
	except:
		return Response({'detail':'Beýle sargyt ýok.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateSimpleOrderToDelivered(request, pk):
	order = SimpleOrder.objects.get(_id=pk)

	order.isDelivered = True
	order.save()

	return Response('Sargyt eltip berildi.')