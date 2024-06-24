from rest_framework import serializers
from items.models import Item
from suppliers.models import Supplier
from suppliers.serializers import SupplierSerializer

class ItemSerializer(serializers.ModelSerializer):
    """Inventory item serializer"""

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'date_created']
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

class ItemSupplierSerializer(serializers.ModelSerializer):
    """Serializer for the suppliers of an item"""
    suppliers = SupplierSerializer(many=True, read_only=True) 
    suppliers_id = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), many=True, write_only=True)


    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'date_created', 'suppliers', 'suppliers_id']
        read_only_fields = ['id', 'name', 'description', 'price', 'date_created', 'suppliers']


class SupplierWithItemsSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    items_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), many=True, write_only=True)

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'items', 'items_id']
        read_only_fields = ['name']