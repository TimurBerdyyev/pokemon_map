# Generated by Django 3.1.14 on 2024-05-25 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0013_auto_20240525_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='element_type',
        ),
        migrations.AddField(
            model_name='pokemonentity',
            name='element_type',
            field=models.ManyToManyField(to='pokemon_entities.PokemonElementType', verbose_name='Стихия'),
        ),
    ]
