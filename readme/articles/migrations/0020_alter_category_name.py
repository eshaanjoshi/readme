# Generated by Django 5.0.6 on 2024-06-17 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0019_remove_post_issues_post_issues'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]