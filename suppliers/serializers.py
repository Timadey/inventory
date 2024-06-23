from rest_framework import serializers
from suppliers.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    """Item supplier serializer"""

    class Meta:
        model = Supplier
        fields = ['id', 'name']
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

    
