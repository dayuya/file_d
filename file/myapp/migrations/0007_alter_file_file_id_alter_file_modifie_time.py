# Generated by Django 4.2.5 on 2023-09-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_file_file_id_alter_file_modifie_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_id',
            field=models.CharField(default='88383424ce8f4657be54c8af3943995c', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='file',
            name='modifie_time',
            field=models.BigIntegerField(default=1694959989327),
        ),
    ]
