# Generated by Django 5.1.6 on 2025-03-14 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_diary_one_user_per_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='date',
            field=models.DateField(verbose_name='日付'),
        ),
    ]
