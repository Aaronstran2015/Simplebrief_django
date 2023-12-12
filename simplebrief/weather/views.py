from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import urllib
import folium
from weather.models import Airport
from weather.scripts.api_calls import *

def index(request) :
    return render(request, 'template.html')

def metar(request) :
    if request.method == 'POST': 

        icao_code = request.POST.get('icaoID').replace(' ', '')
        metar = get_metar(icao_code)

        return render(request, 'metar.html', {
            'metar': metar,
        })
        
    return render(request, 'metar.html')

def taf(request) :

    if request.method == 'POST' :

        icao_code = request.POST.get('icaoID')
        taf = get_taf(icao_code)
        
        return render(request, 'taf.html', {
            'taf' : taf,
        })

    return render(request, 'taf.html')

def brief(request) :
    
    if request.method == 'POST' :

        dep = request.POST.get('dep').upper()
        arr = request.POST.get('arr').upper()

        #accesses the airport objects so the class data can be used.
        airport_one = get_object_or_404(Airport, icao_code = dep)
        airport_two = get_object_or_404(Airport, icao_code = arr)


        airport_icaos = [airport_one.icao_code, airport_two.icao_code]
        airport_names = [airport_one.airport_name, airport_two.airport_name]
        airport_country = [airport_one.airport_country, airport_two.airport_country]
        #airport_coordinates list contains lat and long for both airports airport one lat an long are index [0] and airport two lat and long are index [1].
        airport_coordinates = ((airport_one.airport_latitude, airport_one.airport_longitude), (airport_two.airport_latitude, airport_two.airport_longitude))
        airport_elevations = [airport_one.airport_elevation, airport_two.airport_elevation]
        
        # Map Creation
        
        #Finds the midpoint between the two airports for the centerpoint of the map view.
        center_latitude = (airport_coordinates[0][0] + airport_coordinates[1][0]) / 2
        center_longitude = (airport_coordinates[0][1] + airport_coordinates[1][1]) / 2

        m = folium.Map(location=(center_latitude, center_longitude), zoom_start=10, tiles='OPNVKarte')

        folium.Marker(airport_coordinates[0], popup=dep).add_to(m)
        folium.Marker(airport_coordinates[1], popup=arr).add_to(m)

        line = folium.PolyLine([airport_coordinates[0] ,airport_coordinates[1]], color='red', weight=2.5, opacity=1).add_to(m)

        #Adjusts the zoom level of the map in order to keep all points in view.
        m.fit_bounds(airport_coordinates)

        #Converts the map object into a template friendly html output.
        map_html = m._repr_html_()
        # End of Map Creation


        #METAR API Requests
        
        departure_metar = get_metar(dep)
        arrival_metar = get_metar(arr)

        #TAF API Requests
        departure_taf = get_taf(dep)
        arrival_taf = get_taf(arr)

        #NOTAMS API Request

        departure_notams = get_notams(dep)
        arrival_notams = get_notams(arr)

        return render(request, 'brief.html', {
            'map_html' : map_html,

            'airports' : 'Airport Info',
            'departure' : 'Departure Airport',
            'arrival' : 'Arrival Airport',

            'a1_icao' : f'ICAO Code: {airport_icaos[0]}',
            'a1_name' : f'Name: {airport_names[0]}',
            'a1_country' : f'Country: {airport_country[0]}',
            'a1_latitude' : f'Latitude: {airport_coordinates[0][0]}',
            'a1_longitude' : f'Longitude: {airport_coordinates[0][1]}',
            'a1_elevation' : f'Elevation: {airport_elevations[0]}',
           
            'a2_icao' : f'ICAO Code: {airport_icaos[1]}',
            'a2_name' : f'Name: {airport_names[1]}',
            'a2_country' : f'Country: {airport_country[1]}',
            'a2_latitude' : f'Latitude: {airport_coordinates[1][0]}',
            'a2_longitude' : f'Longitude: {airport_coordinates[1][1]}',
            'a2_elevation' : f'Elevation: {airport_elevations[1]}',

            'metar' : 'METAR',

            'departure_metar' : departure_metar,
            'arrival_metar' : arrival_metar,

            'taf' : 'TAF',

            'departure_taf' : departure_taf,
            'arrival_taf' : arrival_taf,

            'notams' : 'NOTAM\'s',

            'airport_diagrams' : 'Airport Diagrams',

            
        })

    return render(request, 'brief.html')