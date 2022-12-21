import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
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
    for pokemon in PokemonEntity.objects.filter(
            appeared_at__lt=localtime(now()),
            disappeared_at__gt=localtime(now()),
            ):
        add_pokemon(
            folium_map,
            pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.image.url),
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
    for pokemon in Pokemon.objects.all():
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entity = PokemonEntity.objects.get(pokemon=requested_pokemon)
    add_pokemon(
        folium_map,
        pokemon_entity.lat,
        pokemon_entity.lon,
        request.build_absolute_uri(requested_pokemon.image.url),
    )
    pokemon = {
        "pokemon_id": int(pokemon_id),
        "title_ru": requested_pokemon.title,
        "img_url": request.build_absolute_uri(requested_pokemon.image.url),
        "description": requested_pokemon.description,
        "title_en": requested_pokemon.title_en,
        "entities": [
            {
                "level": pokemon_entity.level,
                "lat": pokemon_entity.lat,
                "lon": pokemon_entity.lon
            }
        ],
    }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
