import json

from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('../data/ingredients.json', 'r', encoding='utf-8') as file:
            json_ingredient = json.load(file)
            for elem in json_ingredient:
                Ingredient.objects.get_or_create(
                    name=elem['name'],
                    measurement_unit=elem['measurement_unit']
                )
        self.stdout.write(
            self.style.SUCCESS('Ingredients added')
        )
