import random

import factory
import factory.fuzzy

from ordo_fast.enums import Classes, Origins, Ranks, UserRoles
from ordo_fast.models import Task, TaskState, User


class UserFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = User

    username = factory.Sequence(lambda n: f'test{n}')  # type: ignore
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')  # type: ignore
    password = factory.LazyAttribute(lambda obj: f'{obj.username}1301')  # type: ignore
    role = factory.fuzzy.FuzzyChoice(UserRoles)


class TaskFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Task

    title = factory.faker.Faker('text')
    description = factory.faker.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TaskState)
    user_id = 1


class CharacterFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = dict

    name = factory.faker.Faker('name')
    age = factory.LazyFunction(lambda: random.randint(1, 999))  # type: ignore
    origin = factory.Iterator([e.value for e in Origins])  # type: ignore
    character_class = factory.Iterator([e.value for e in Classes])  # type: ignore
    rank = factory.Iterator([e.value for e in Ranks])  # type: ignore
    nex_total = factory.LazyFunction(lambda: random.randint(0, 100))  # type: ignore
    nex_class = factory.LazyFunction(lambda: random.randint(0, 100))  # type: ignore
    nex_subclass = factory.LazyFunction(lambda: random.randint(0, 100))  # type: ignore
    healthy_points = factory.LazyFunction(lambda: random.randint(1, 999))  # type: ignore
    sanity_points = factory.LazyFunction(lambda: random.randint(1, 999))  # type: ignore
    effort_points = factory.LazyFunction(lambda: random.randint(1, 999))  # type: ignore
    atrib_agility = factory.LazyFunction(lambda: random.randint(0, 5))  # type: ignore
    atrib_intellect = factory.LazyFunction(lambda: random.randint(0, 5))  # type: ignore
    atrib_vitallity = factory.LazyFunction(lambda: random.randint(0, 5))  # type: ignore
    atrib_presence = factory.LazyFunction(lambda: random.randint(0, 5))  # type: ignore
    atrib_strength = factory.LazyFunction(lambda: random.randint(0, 5))  # type: ignore
