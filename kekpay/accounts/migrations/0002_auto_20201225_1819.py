# Generated by Django 3.1.4 on 2020-12-25 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistory',
            name='started_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transactionhistory',
            name='to_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_account', to='accounts.account'),
        ),
    ]
