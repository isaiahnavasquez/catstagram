# Generated by Django 2.0.5 on 2018-06-01 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0012_auto_20180601_0149'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('post', models.ManyToManyField(to='cats.Post')),
            ],
        ),
    ]
