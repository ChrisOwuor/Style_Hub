# Generated by Django 4.2 on 2024-04-10 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_document_rename_user_name_user_full_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Document',
        ),
    ]
