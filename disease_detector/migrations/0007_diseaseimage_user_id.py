# Generated by Django 5.1.7 on 2025-03-26 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disease_detector', '0006_diseaserecord_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='diseaseimage',
            name='user_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
