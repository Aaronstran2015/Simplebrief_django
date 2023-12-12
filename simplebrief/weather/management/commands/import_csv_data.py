import csv
from django.core.management.base import BaseCommand
from weather.models import Airport
import os

class Command(BaseCommand) :
    help = 'Import data from CSV file'


    def handle(self, *args, **options) :
        csv_file_path = 'weather/data/airports.csv'

        counter = 0

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
        
            for row in csv_reader :
            
                icao_code = row.get('gps_code', '')
                airport_name = row.get('name', '')
                airport_latitude = row.get('latitude_deg', '')
                airport_longitude = row.get('longitude_deg', '')
                airport_elevation = row.get('elevation_ft', '')
                airport_country = row.get('iso_country', '')
                

                if airport_latitude == '':
                    airport_latitude = None
                if airport_longitude == '':
                    airport_longitude = None
                if airport_elevation == '':
                    airport_elevation = None

                Airport.objects.create(
                    icao_code = icao_code,
                    airport_name = airport_name,
                    airport_latitude = airport_latitude,
                    airport_longitude = airport_longitude,
                    airport_elevation = airport_elevation,
                    airport_country = airport_country,
                    
                )
                counter += 1
                print(f'Progress: {counter}')

        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))