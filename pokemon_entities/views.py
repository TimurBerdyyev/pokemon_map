import folium

from django.shortcuts import render
from .models import PokemonEntity
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import get_object_or_404



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
    for pokemon_entity in pokemon_entities:
        pokemons_on_page.append({
            'pokemon_id': pokemon_entity.pokemon.id,
            'img_url': request.build_absolute_uri(pokemon_entity.pokemon.image.url),
            'title_ru': pokemon_entity.pokemon.title_ru
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_entity = get_object_or_404(PokemonEntity, pk=pokemon_id)

    folium_map = folium.Map(location=[pokemon_entity.lat, pokemon_entity.lon], zoom_start=13)
    folium.Marker([pokemon_entity.lat, pokemon_entity.lon], popup=pokemon_entity.pokemon.title_ru).add_to(folium_map)

    pokemon_info = {
        'img_url': request.build_absolute_uri(pokemon_entity.pokemon.image.url),
        'title_ru': pokemon_entity.pokemon.title_ru,
        'title_en': pokemon_entity.pokemon.title_en,
        'title_jp': pokemon_entity.pokemon.title_jp,
        'description': pokemon_entity.pokemon.description
    }

    evolution_info = {}
    previous_evolution = pokemon_entity.pokemon.previous_evolutions.first()
    if previous_evolution:
        evolution_info['previous_evolution'] = {
            'title_ru': previous_evolution.title_ru,
            'img_url': request.build_absolute_uri(previous_evolution.image.url),
            'url': reverse('pokemon', args=[previous_evolution.id]),
        }
    if pokemon_entity.pokemon.next_evolution:
        next_evolution = pokemon_entity.pokemon.next_evolution
        evolution_info['next_evolution'] = {
            'title_ru': next_evolution.title_ru,
            'img_url': request.build_absolute_uri(next_evolution.image.url),
            'url': reverse('pokemon', args=[next_evolution.id]),
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_info,
        'evolution_info': evolution_info,
    })