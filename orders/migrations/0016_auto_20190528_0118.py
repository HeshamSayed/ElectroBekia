# Generated by Django 2.2.1 on 2019-05-28 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20190528_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(default=('a','في الانتظار'),choices=[('r', 'تم رفض اللسعر'), ('a', 'تم قبول السعر')], max_length=5),
        ),
    ]