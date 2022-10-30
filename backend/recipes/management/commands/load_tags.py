from django.core.management import BaseCommand

from recipes.models import Tag

tag = [
    {'name': 'завтрак', 'color': '#CC5500', 'slug': 'breakfast'},
    {'name': 'обед', 'color': '#006633', 'slug': 'lunch'},
    {'name': 'ужин', 'color': '#660099', 'slug': 'dinner'},
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for elem in tag:
            Tag.objects.get_or_create(
                name=elem['name'],
                color=elem['color'],
                slug=elem['slug'],
            )
        self.stdout.write(
            self.style.SUCCESS('Tags added')
        )
