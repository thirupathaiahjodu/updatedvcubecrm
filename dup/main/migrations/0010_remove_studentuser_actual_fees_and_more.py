# Generated by Django 4.2.5 on 2024-01-05 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_test_present'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentuser',
            name='actual_fees',
        ),
        migrations.RemoveField(
            model_name='studentuser',
            name='fees_paid',
        ),
        migrations.AlterField(
            model_name='test',
            name='present',
            field=models.BooleanField(default=False),
        ),
    ]
