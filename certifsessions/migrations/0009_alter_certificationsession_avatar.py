# Generated by Django 3.2.5 on 2022-01-02 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certifsessions', '0008_alter_certificationsession_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificationsession',
            name='avatar',
            field=models.ImageField(blank=True, default='formation.jpg', null=True, upload_to='sessions'),
        ),
    ]
