from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True)
    description = models.TextField(null=True)
    title_en = models.CharField(max_length=200)
    title_jp = models.CharField(max_length=200)
    evolved_from = models.ForeignKey(
                        "self",
                        null=True,
                        blank=True,
                        on_delete=models.SET_NULL
                    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()
