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
        img_url = entity.pokemon.image.url if entity.pokemon.image \
            else DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            request.build_absolute_uri(img_url),
        )
    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        img_url = request.build_absolute_uri(pokemon.image.url) \
            if pokemon.image else DEFAULT_IMAGE_URL
        pokemon_on_page = {
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title,
            'img_url': img_url,
        }
        pokemons_on_page.append(pokemon_on_page)
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    img_url = requested_pokemon.image.url if requested_pokemon.image \
        else DEFAULT_IMAGE_URL
    pokemon = {
        "pokemon_id": int(pokemon_id),
        "title_ru": requested_pokemon.title,
        "img_url": request.build_absolute_uri(img_url),
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
            request.build_absolute_uri(img_url),
        )
        pokemon["entities"].append(
            {
                "level": entity.level,
                "lat": entity.lat,
                "lon": entity.lon,
            }
        )
    if requested_pokemon.previous_evolution:
        prev_evo = requested_pokemon.previous_evolution
        prev_evo_img_url = prev_evo.image.url if prev_evo.image \
            else DEFAULT_IMAGE_URL
        pokemon["previous_evolution"] = {
            "title_ru": prev_evo.title,
            "pokemon_id": prev_evo.id,
            "img_url": request.build_absolute_uri(prev_evo_img_url),
        }
    if requested_pokemon.next_evolutions.first():
        next_evo = requested_pokemon.next_evolutions.first()
        next_evo_img_url = next_evo.image.url if next_evo.image \
            else DEFAULT_IMAGE_URL
        pokemon["next_evolution"] = {
            "title_ru": next_evo.title,
            "pokemon_id": next_evo.id,
            "img_url": request.build_absolute_uri(next_evo_img_url),
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
