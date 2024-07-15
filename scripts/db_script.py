from part_app.models import Mark, Model, Part
import random


def mark_create() -> None:
    name = ['BMW', 'Audi', 'Mercedes', 'Honda', 'Volkswagen']
    country = ['Germany', 'USA', 'Japan', 'UK', 'Russia']

    for i in range(5):
        mark = Mark.objects.create(name=name[i], producer_country_name=country[i],
                                   is_visible=True)
        mark.save()


def model_create() -> None:
    name = ['X5', 'A4', 'C-class', 'Accord', 'Passat']

    for i in range(1, 6):
        model = Model.objects.create(name=name[i-1], mark_id=Mark.objects.get(id=i), is_visible=True)
        model.save()


def part_create() -> None:
    name = ['Tire', 'Engine', 'Brake', 'Wheel', 'Seat']
    colors = ['red', 'blue', 'green', 'black', 'white', 'yellow']
    for i in range(10_000):
        part = Part.objects.create(name=random.choice(name),
                                   mark_id=Mark.objects.get(id=random.randrange(1, 5)),
                                   model_id=Model.objects.get(id=random.randrange(1, 5)),
                                   price=random.randint(1000, 10000),
                                   json_data={"color": random.choice(colors),
                                              "is_new_part": random.choice([True, False]),
                                              "count": random.randint(1, 10)},
                                   is_visible=True)
        part.save()


def main():
    mark_create()
    model_create()
    part_create()


main()