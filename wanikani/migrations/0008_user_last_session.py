# Generated by Django 2.1.4 on 2019-02-17 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wanikani', '0007_auto_20190127_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_session',
            field=models.IntegerField(default=0),
        ),
    ]
