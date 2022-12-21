from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(
        verbose_name="Название на русском",
        max_length=200,
    )
    image = models.ImageField(
        verbose_name="Изображение",
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        null=True,
    )
    title_en = models.CharField(
        verbose_name="Название на английском",
        max_length=200,
    )
    title_jp = models.CharField(
        verbose_name="Название на японском",
        max_length=200,
    )
    evolved_from = models.ForeignKey(
                        "self",
                        verbose_name="Эволюционный предшественник",
                        null=True,
                        blank=True,
                        on_delete=models.SET_NULL,
                        related_name="evolve_into",
                    )

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name="Покемон",
        on_delete=models.CASCADE,
    )
    lat = models.FloatField(verbose_name="Широта местонахождения")
    lon = models.FloatField(verbose_name="Долгота местонахождения")
    appeared_at = models.DateTimeField(verbose_name="Дата появления")
    disappeared_at = models.DateTimeField(verbose_name="Дата исчезновения")
    level = models.IntegerField(verbose_name="Уровень")
    health = models.IntegerField(verbose_name="Здоровье")
    strength = models.IntegerField(verbose_name="Атака")
    defence = models.IntegerField(verbose_name="Защита")
    stamina = models.IntegerField(verbose_name="Выносливость")
