from django.db import models  

class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Название на русском")
    title_en = models.CharField(max_length=150, null=True, blank=True, verbose_name="Название на английском")
    title_jp = models.CharField(max_length=150, null=True, blank=True, verbose_name="Название на японском")
    image = models.ImageField(blank=True, verbose_name="Изображение")
    description = models.TextField(max_length=250, null=True, verbose_name="Описание")
    next_evolution = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='evolutions', verbose_name="Следующая эволиция")

    def __str__(self):
        return self.title_ru
     
    
    
    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True,  related_name='entities', verbose_name="Покемон")
    lat = models.FloatField(null=True, verbose_name="Широта")
    lon = models.FloatField(null=True, verbose_name="Долгота")
    appeared_at = models.DateTimeField(null=True, verbose_name="Появился")
    disappeared_at = models.DateTimeField(null=True, verbose_name="Исчез")
    level = models.IntegerField(blank=True, null=True, verbose_name="Уровень")
    health = models.IntegerField(blank=True, null=True, verbose_name="Здоровье")
    attack = models.IntegerField(blank=True, null=True, verbose_name="Атака")
    protection = models.IntegerField(blank=True, null=True, verbose_name="Защита")
    endurance = models.IntegerField(blank=True, null=True, verbose_name="Выносливость")

    def __str__(self):
        return str(self.pokemon)
    
    class Meta:
        verbose_name = "Экземпляр покемона"
        verbose_name_plural = "Экземпляры покемонов"
