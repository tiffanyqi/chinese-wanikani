# Generated by Django 2.1.4 on 2019-01-22 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wanikani', '0003_auto_20190122_0516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progresscharacter',
            name='last_session',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='progresscharacter',
            name='upcoming_review_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
