# Generated by Django 4.1 on 2022-11-28 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebServer', '0003_usuario_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitios',
            name='completo',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
