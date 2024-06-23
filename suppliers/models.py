from django.db import models
from django.utils.translation import gettext_lazy as _

from uuid import uuid4

# Create your models here.

class Supplier(models.Model):
    """A supplier model"""

    id = models.UUIDField(_("Supplier ID"), primary_key=True, editable=False, default=uuid4)
    name = models.CharField(_("Supplier Name"), max_length=128, unique=True, help_text="Unique name of the supplier")

    class Meta:
        db_table = 'suppliers'

    def __str__(self):
        return f"Supplier: {self.name}"
    