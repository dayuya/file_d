# Generated by Django 4.2.5 on 2023-09-17 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_file_file_id_alter_file_modifie_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_id',
            field=models.CharField(default='408713f3bf5748c4acd29d0e69efdfe3', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='file',
            name='modifie_time',
            field=models.BigIntegerField(default=1694938196947),
        ),
    ]
