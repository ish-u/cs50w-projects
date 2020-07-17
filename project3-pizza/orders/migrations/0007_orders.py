# Generated by Django 3.0.7 on 2020-06-26 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0006_pizza_special'),
    ]

    operations = [
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Price', models.FloatField(default=0)),
                ('Pasta', models.ManyToManyField(blank=True, to='orders.Pasta_Order')),
                ('Pizza', models.ManyToManyField(blank=True, to='orders.Pizza_Order')),
                ('Platter', models.ManyToManyField(blank=True, to='orders.Platter_Order')),
                ('Salad', models.ManyToManyField(blank=True, to='orders.Salad_Order')),
                ('Subs', models.ManyToManyField(blank=True, to='orders.Subs_Order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
