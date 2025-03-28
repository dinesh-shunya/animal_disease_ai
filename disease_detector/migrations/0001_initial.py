# Generated by Django 5.1.7 on 2025-03-24 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='disease_images/')),
                ('disease_name', models.CharField(max_length=255)),
                ('probability', models.CharField(max_length=10)),
                ('urgency_level', models.CharField(max_length=50)),
                ('symptoms_analysis', models.TextField()),
                ('recommended_actions', models.TextField()),
                ('preventive_care', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
