# Generated by Django 3.1.14 on 2024-05-15 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0009_auto_20240511_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon'),
        ),
    ]
