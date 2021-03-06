# Generated by Django 2.1.4 on 2019-01-13 00:06

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseCharacter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.CharField(max_length=50, null=True)),
                ('definitions', django.contrib.postgres.fields.jsonb.JSONField()),
                ('pinyin', django.contrib.postgres.fields.jsonb.JSONField()),
                ('hsk_level', models.IntegerField(default=0)),
                ('frequency', models.IntegerField(default=0)),
                ('user_level', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LevelCharacter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unlocked', models.BooleanField(default=False)),
                ('num_correct_pinyin', models.IntegerField(default=0)),
                ('num_correct_definitions', models.IntegerField(default=0)),
                ('num_correct_all', models.IntegerField(default=0)),
                ('num_times_shown', models.IntegerField(default=0)),
                ('unlocked_date', models.DateTimeField(default=None)),
                ('upcoming_review_date', models.DateTimeField(default=None)),
                ('last_reviewed_date', models.DateTimeField(default=None)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wanikani.BaseCharacter')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_started', models.DateTimeField(default=django.utils.timezone.now)),
                ('session_type', models.CharField(max_length=50, null=True)),
                ('num_correct_pinyin', models.IntegerField(default=0)),
                ('num_correct_definitions', models.IntegerField(default=0)),
                ('num_correct_all', models.IntegerField(default=0)),
                ('total_items', models.IntegerField(default=0)),
                ('complete', models.BooleanField(default=False)),
                ('characters', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=50, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('level', models.CharField(default=0, max_length=50)),
                ('username', models.CharField(max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wanikani.User'),
        ),
        migrations.AddField(
            model_name='levelcharacter',
            name='last_session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wanikani.Session'),
        ),
        migrations.AddField(
            model_name='levelcharacter',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wanikani.User'),
        ),
    ]
