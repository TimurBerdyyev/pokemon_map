from django.db import models  


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=150, null=True)
    title_jp = models.CharField(max_length=150, null=True)
    image = models.ImageField(blank=True)
    description = models.TextField(max_length=250, null=True)
    

    def __str__(self):
        return f'{self.title_ru}'
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    Level = models.IntegerField(blank=True, null=True)
    Health = models.IntegerField(blank=True, null=True)
    Attack = models.IntegerField(blank=True, null=True)
    Protection = models.IntegerField(blank=True, null=True)
    Endurance = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.pokemon}'