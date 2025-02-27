# Generated by Django 2.2.8 on 2023-06-21 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('email_sent', models.BooleanField()),
                ('received_reply', models.BooleanField()),
                ('assessment_scheduled', models.BooleanField()),
                ('assessment_graded', models.BooleanField()),
                ('schedule_interview', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('students', models.ManyToManyField(null=True, to='recruit.Student')),
            ],
        ),
    ]
