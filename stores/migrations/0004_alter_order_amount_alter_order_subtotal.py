# Generated by Django 5.1.2 on 2024-10-18 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_cart_cartproduct_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='subtotal',
            field=models.PositiveBigIntegerField(),
        ),
    ]
