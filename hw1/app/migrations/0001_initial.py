# Generated by Django 5.0.6 on 2024-07-01 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Context_text', models.CharField(max_length=200)),
                ('Created_date', models.DateTimeField(verbose_name='date_created')),
            ],
        ),
    ]