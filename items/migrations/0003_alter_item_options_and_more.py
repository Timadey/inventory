# Generated by Django 5.0.6 on 2024-06-21 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_item_date_added'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['date_created']},
        ),
        migrations.RenameField(
            model_name='item',
            old_name='date_added',
            new_name='date_created',
        ),
    ]