# Generated by Django 4.2.5 on 2023-09-15 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_file_file_id_alter_file_modifie_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_id',
            field=models.CharField(default='8ae7b1af51ec4b6a8bee48d2d0c72e3b', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='file',
            name='modifie_time',
            field=models.BigIntegerField(default=1694795487126),
        ),
    ]