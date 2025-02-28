# Generated by Django 5.1.2 on 2024-10-12 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fridges', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('count', models.IntegerField()),
                ('fridge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fridges.fridge')),
            ],
        ),
    ]
