import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import PokemonEntity
from django.utils import timezone


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
    current_time = timezone.localtime(timezone.now())
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lt=current_time,
        disappeared_at__gt=current_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon_entitie in pokemon_entities:
        pokemons_on_page.append({
            'pokemon_id': pokemon_entitie.pokemon.id,
            'img_url': request.build_absolute_uri(pokemon_entitie.pokemon.image.url),
            'title_ru': pokemon_entitie.pokemon.title_ru
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon_entity = PokemonEntity.objects.filter(pokemon_id=pokemon_id).first()
        if not pokemon_entity:
            return PokemonEntity.DoesNotExist
    except PokemonEntity.DoesNotExist:
        return HttpResponseNotFound('<h1> ДАННОГО ПОКЕМОНА НЕ НАЙДЕННО </h1>')
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=13)
    add_pokemon(
        folium_map, pokemon_entity.lat,
        pokemon_entity.lon,
        request.build_absolute_uri(pokemon_entity.pokemon.image.url)
    )

    pokemon_info = {
        'img_url': request.build_absolute_uri(pokemon_entity.pokemon.image.url),
        'title_ru': pokemon_entity.pokemon.title_ru
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 
        'pokemon': pokemon_info
    })
