# Generated by Django 5.0.3 on 2024-03-19 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.CharField(choices=[('В обработке', 'В обработке'), ('Подписан', 'Подписан'), ('В исполнении', 'В исполнении'), ('Завершен', 'Завершен')], max_length=20),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
