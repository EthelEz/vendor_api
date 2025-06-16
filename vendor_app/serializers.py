from rest_framework import serializers
from .models import Category, Product, ProductVariant, Customer, Order, OrderItem, Cart, CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'length', 'color', 'texture', 'price_adjustment', 'stock']

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    image = serializers.ImageField(required=False, allow_null=True)  # Added ImageField
    # hair_type = serializers.ChoiceField(choices=Product.HAIR_TYPE_CHOICES)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'category', 'category_id', 'hair_type', 'base_price', 'stock', 'variants']

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'shipping_address', 'preferences']

class OrderItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='variant', write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'variant', 'variant_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'total_amount', 'created_at', 'items']

class CartItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='variant', write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'variant_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'items', 'total']

    def get_total(self, obj):
        return sum(item.variant.price_adjustment + item.variant.product.base_price for item in obj.items.all())