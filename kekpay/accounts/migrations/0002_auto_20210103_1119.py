# Generated by Django 3.1.4 on 2021-01-03 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='currency',
            field=models.CharField(choices=[('FR', 'Freshman')], default='FR', max_length=3),
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=255),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='amount',
            field=models.DecimalField(decimal_places=6, max_digits=255),
        ),
    ]