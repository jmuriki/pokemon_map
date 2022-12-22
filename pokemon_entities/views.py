import folium

from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime, now


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    moment = localtime(now())
    for entity in PokemonEntity.objects.filter(
            appeared_at__lt=moment,
            disappeared_at__gt=moment,
            ):
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            request.build_absolute_uri(entity.pokemon.image.url),
        )
    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemon_on_page = {
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title,
        }
        if pokemon.image:
            pokemon_on_page['img_url'] = \
                request.build_absolute_uri(pokemon.image.url)
        pokemons_on_page.append(pokemon_on_page)
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon = {
        "pokemon_id": int(pokemon_id),
        "title_ru": requested_pokemon.title,
        "img_url": request.build_absolute_uri(requested_pokemon.image.url),
        "description": requested_pokemon.description,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "entities": [],
    }
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    for entity in pokemon_entities:
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            request.build_absolute_uri(requested_pokemon.image.url),
        )
        pokemon["entities"].append(
            {
                "level": entity.level,
                "lat": entity.lat,
                "lon": entity.lon,
            }
        )
    if requested_pokemon.previous_evolution:
        pokemon["previous_evolution"] = {
            "title_ru": requested_pokemon.previous_evolution.title,
            "pokemon_id": requested_pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(
                requested_pokemon.previous_evolution.image.url
            ),
        }
    if requested_pokemon.next_evolution.first():
        pokemon["next_evolution"] = {
            "title_ru": requested_pokemon.next_evolution.all().first().title,
            "pokemon_id": requested_pokemon.next_evolution.all().first().id,
            "img_url": request.build_absolute_uri(
                requested_pokemon.next_evolution.all().first().image.url
            ),
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
