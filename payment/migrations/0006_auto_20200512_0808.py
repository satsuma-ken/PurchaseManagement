# Generated by Django 3.0.4 on 2020-05-11 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_auto_20200512_0708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bills_detail',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='bills_detail',
            name='update_date',
        ),
        migrations.RemoveField(
            model_name='bills_header',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='bills_header',
            name='update_date',
        ),
        migrations.RemoveField(
            model_name='company',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='company',
            name='update_date',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='update_date',
        ),
        migrations.RemoveField(
            model_name='department',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='department',
            name='update_date',
        ),
        migrations.AddField(
            model_name='bills_detail',
            name='create_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bills_detail',
            name='update_datetime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='bills_header',
            name='create_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bills_header',
            name='update_datetime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='create_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='update_datetime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='currency',
            name='create_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='currency',
            name='update_datetime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='create_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='update_datetime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]