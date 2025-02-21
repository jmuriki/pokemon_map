from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(
        verbose_name="Название на русском",
        max_length=200,
    )
    image = models.ImageField(
        verbose_name="Изображение",
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )
    title_en = models.CharField(
        verbose_name="Название на английском",
        blank=True,
        max_length=200,
    )
    title_jp = models.CharField(
        verbose_name="Название на японском",
        blank=True,
        max_length=200,
    )
    previous_evolution = models.ForeignKey(
                        "self",
                        verbose_name="Эволюционный предшественник",
                        null=True,
                        blank=True,
                        on_delete=models.SET_NULL,
                        related_name="next_evolutions",
                    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name="Покемон",
        on_delete=models.CASCADE,
        related_name="entities",
    )
    lat = models.FloatField(
        verbose_name="Широта местонахождения",
        null=True,
    )
    lon = models.FloatField(
        verbose_name="Долгота местонахождения",
        null=True,
    )
    appeared_at = models.DateTimeField(
        verbose_name="Дата появления",
        null=True,
        blank=True,
    )
    disappeared_at = models.DateTimeField(
        verbose_name="Дата исчезновения",
        null=True,
        blank=True,
    )
    level = models.IntegerField(
        verbose_name="Уровень",
        null=True,
        blank=True,
    )
    health = models.IntegerField(
        verbose_name="Здоровье",
        null=True,
        blank=True,
    )
    strength = models.IntegerField(
        verbose_name="Атака",
        null=True,
        blank=True,
    )
    defence = models.IntegerField(
        verbose_name="Защита",
        null=True,
        blank=True,
    )
    stamina = models.IntegerField(
        verbose_name="Выносливость",
        null=True,
        blank=True,
    )
