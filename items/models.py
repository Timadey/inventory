from django.db import models
from django.utils.translation import gettext_lazy as _

from uuid import uuid4

# Create your models here.

class Item(models.Model):
    """An inventory item model"""

    id = models.UUIDField(_("Item ID"), primary_key=True, editable=False, default=uuid4)
    name = models.CharField(_("Item Name"), max_length=128, unique=True, help_text="Unique name of item in the inventory")
    description = models.TextField(_("Detailed Description of Item"), max_length=2048)
    price = models.DecimalField(_("Price of the Item"), max_digits=9, decimal_places=2)
    suppliers = models.ManyToManyField("suppliers.Supplier", related_name='items')
    date_created = models.DateTimeField(_("Date Added"), auto_now_add=True)

    class Meta:
        db_table = 'items'
        ordering = ['date_created']

    def __str__(self):
        return f"Inventory Item: {self.name}"
    
