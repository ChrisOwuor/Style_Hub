# Generated by Django 4.2 on 2024-05-01 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_rename_avaiilability_stylist_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='u_id',
            field=models.UUIDField(editable=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='u_id',
            field=models.UUIDField(editable=False),
        ),
        migrations.AlterField(
            model_name='stylist',
            name='u_id',
            field=models.UUIDField(editable=False),
        ),
    ]
