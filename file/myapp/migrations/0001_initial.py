# Generated by Django 4.2.5 on 2023-09-14 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('file_id', models.CharField(default='f497a7eb753f4d30923afd7740e326f2', max_length=32, primary_key=True, serialize=False)),
                ('user_id', models.BigIntegerField()),
                ('file_type', models.PositiveSmallIntegerField(default=None, null=True)),
                ('file_name', models.CharField(default=None, max_length=255, null=True)),
                ('status', models.PositiveSmallIntegerField(default=None, null=True)),
                ('file_url', models.CharField(default=None, max_length=255, null=True)),
                ('modifie_time', models.BigIntegerField(default=1694680891343)),
            ],
            options={
                'db_table': 'file',
            },
        ),
    ]
