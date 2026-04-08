from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Order, OrderItem    
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        with transaction.atomic():
            order = Order.objects.create(user=user)

            for item in items_data:
                product = item['product']
                quantity = item['quantity']

                if product.stock < quantity:
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name}"
                    )

                # ✅ Reduce stock
                product.stock -= quantity
                product.save()

                # ✅ Create order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

        return order

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email' 