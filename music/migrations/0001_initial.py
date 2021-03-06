# Generated by Django 2.2.4 on 2019-09-01 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField()),
                ('artist', models.CharField(max_length=255, null=True)),
                ('album', models.CharField(max_length=255, null=True)),
                ('song', models.CharField(max_length=255, null=True)),
                ('track', models.IntegerField(null=True)),
                ('comment', models.TextField(null=True)),
                ('year', models.CharField(max_length=255, null=True)),
                ('genre', models.CharField(max_length=255, null=True)),
                ('band', models.CharField(max_length=255, null=True)),
                ('composer', models.CharField(max_length=255, null=True)),
                ('copyright', models.CharField(max_length=255, null=True)),
                ('url', models.URLField(null=True)),
                ('publisher', models.TextField()),
            ],
            options={
                'verbose_name': 'Song',
                'verbose_name_plural': 'Songs',
                'db_table': 'song',
            },
        ),
    ]
