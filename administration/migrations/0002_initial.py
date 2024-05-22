# Generated by Django 4.2 on 2024-05-22 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvalrequest',
            name='stylist_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.stylist'),
        ),
    ]
