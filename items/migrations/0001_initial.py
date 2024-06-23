# Generated by Django 5.0.6 on 2024-06-21 15:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Item ID')),
                ('name', models.CharField(help_text='Unique name of item in the inventory', max_length=128, unique=True, verbose_name='Item Name')),
                ('description', models.TextField(max_length=2048, verbose_name='Detailed Description of Item')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Price of the Item')),
                ('suppliers', models.ManyToManyField(related_name='items', to='suppliers.supplier')),
            ],
            options={
                'db_table': 'items',
            },
        ),
    ]
