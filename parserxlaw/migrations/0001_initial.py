# Generated by Django 2.0.6 on 2018-06-09 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usertrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steamid', models.CharField(max_length=20)),
                ('ip', models.CharField(max_length=20)),
                ('connections', models.IntegerField()),
                ('lastupdated', models.DateTimeField()),
            ],
            options={
                'db_table': 'usertrack',
                'managed': False,
            },
        ),
    ]
