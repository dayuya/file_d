# Generated by Django 4.2.5 on 2023-09-14 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('permission_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('path', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'permission',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='RolePermission',
            fields=[
                ('role_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('permission_id', models.BigIntegerField(null=True)),
            ],
            options={
                'db_table': 'role_permission',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('allocated_size', models.BigIntegerField(blank=True, default=None, null=True)),
                ('used_size', models.BigIntegerField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'storage',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('nickname', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('password', models.CharField(max_length=255)),
                ('role_id', models.BigIntegerField()),
                ('account', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AlterField(
            model_name='file',
            name='file_id',
            field=models.CharField(default='3842cad5fd274292a665fbae5edfea5f', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='file',
            name='modifie_time',
            field=models.BigIntegerField(default=1694681679094),
        ),
    ]
