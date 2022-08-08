# Generated by Django 4.0.3 on 2022-06-14 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_alter_mainlisting_listing_mode'),
        ('properties', '0045_remove_listingpricebycategory_listing_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='listingpricebycategory',
            name='listing_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='listings.listingtype'),
            preserve_default=False,
        ),
    ]