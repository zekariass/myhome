# Generated by Django 4.0.3 on 2022-06-04 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0034_propertyamenity_property_amenity_unique_constraint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='properties.property'),
        ),
    ]