from prettytable import PrettyTable


def table_recipes(ingredients):
    table = PrettyTable()
    table.field_names = [
        'Ингридиенты', 'Единицы измерения', 'Количество',
    ]
    for i in ingredients:
        table.add_row([
            i['ingredient__name'],
            i['ingredient__measurement_unit'],
            i['amount__sum'],
        ])
    return table.get_string()
