# Generated by Django 4.2 on 2024-04-02 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_img_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img_url',
            field=models.ImageField(blank=True, default='C:\\django\\stye_hub\\style_hub\\Media\\user_icon.jpeg', null=True, upload_to='Media'),
        ),
    ]
