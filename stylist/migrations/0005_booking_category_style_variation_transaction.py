# Generated by Django 4.2 on 2024-04-29 17:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_admin_u_id_client_u_id_stylist_u_id_stylist_verified_and_more'),
        ('stylist', '0004_rename_stylist_id_userresponse_stylist_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')], default='pending', max_length=20)),
                ('completed', models.BooleanField(default=False)),
                ('u_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
                ('stylist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.stylist')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('u_id', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('u_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stylist.category')),
                ('stylist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.stylist')),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.TextField()),
                ('photo', models.ImageField(upload_to='')),
                ('video', models.ImageField(upload_to='')),
                ('u_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stylist.style')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('u_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stylist.booking')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
                ('stylist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.stylist')),
            ],
        ),
    ]
