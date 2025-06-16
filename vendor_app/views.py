from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductVariant, Customer, Order, OrderItem, Cart, CartItem
from .serializers import (
    CategorySerializer, ProductSerializer, ProductVariantSerializer,
    CustomerSerializer, OrderSerializer, CartSerializer, CartItemSerializer
)
# from .filters import ProductFilter
from django.db import transaction
from django.db.models import Sum
import stripe
from django.conf import settings

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]  # Admin-only for managing categories

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'hair_type']
    # filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['base_price', 'created_at']
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        threshold = request.query_params.get('threshold', 10)
        products = Product.objects.filter(stock__lte=threshold)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Customer.objects.all()
        return Customer.objects.filter(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer__user=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        status = request.data.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            # TODO: Trigger notification (email/SMS) via Celery task
            return Response({'status': order.status})
        return Response({'error': 'Invalid status'}, status=400)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer__user=self.request.user)

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        cart = self.get_object()
        with transaction.atomic():
            total = sum(
                (item.variant.price_adjustment + item.variant.product.base_price) * item.quantity
                for item in cart.items.all()
            )
            order = Order.objects.create(
                customer=cart.customer,
                total_amount=total,
                status='pending'
            )
            for item in cart.items.all():
                if item.variant.stock < item.quantity:
                    return Response({'error': f'Insufficient stock for {item.variant}'}, status=400)
                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.price_adjustment + item.variant.product.base_price
                )
                item.variant.stock -= item.quantity
                item.variant.save()
            cart.items.all().delete()
            stripe.api_key = settings.STRIPE_SECRET_KEY
            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(total * 100),  # Convert to cents
                    currency='usd',
                    payment_method_types=['card'],
                )
                # TODO: Integrate with shipping provider (e.g., Shippo) for label generation
                return Response(
                    {
                        'order': OrderSerializer(order).data,
                        'client_secret': payment_intent.client_secret,
                    },
                    status=201
                )
            except stripe.error.StripeError as e:
                return Response({'error': str(e)}, status=400)

# import stripe
# stripe.api_key = "your_stripe_secret_key"
# payment_intent = stripe.PaymentIntent.create(
#     amount=int(total * 100),  # Convert to cents
#     currency='usd',
#     payment_method_types=['card'],
# )
     
from rest_framework.views import APIView
class SalesReportView(APIView):
    def get(self, request):
        total_revenue = Order.objects.aggregate(total=Sum('total_amount'))
        return Response({'total_revenue': total_revenue['total']})