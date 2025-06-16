# import django_filters
# from .models import Product

# class ProductFilter(django_filters.FilterSet):
#     class Meta:
#         model = Product
#         fields = {
#             'category': ['exact'],
#             'hair_type': ['exact'],
#             'base_price': ['lt', 'gt', 'lte', 'gte'], # Example for numeric filtering
#             'stock': ['lt', 'gt', 'lte', 'gte'],
#         }