# Generated by Django 3.2.24 on 2024-02-26 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_sku_mesurement_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sku',
            name='mesurement_unit',
        ),
        migrations.AddField(
            model_name='sku',
            name='measurement_unit',
            field=models.CharField(choices=[('gm', 'Grams'), ('kg', 'Kilograms'), ('mL', 'Milliliters'), ('L', 'Liters'), ('pc', 'Piece')], default='gm', max_length=2),
        ),
        migrations.AlterField(
            model_name='sku',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pending for approval'), (1, 'Approved'), (2, 'Discontinued')], default=0),
        ),
    ]