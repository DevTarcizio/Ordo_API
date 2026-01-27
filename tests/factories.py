import random

import factory
import factory.fuzzy

from ordo_fast.enums import Classes, Origins, Ranks, Subclasses, Trails, UserRoles
from ordo_fast.models import User

CLASS_TRAIL_MAP = {
    Classes.mundano: [Trails.none],
    Classes.transformado: [Trails.none],
    Classes.combatente: [
        Trails.aniquilador,
        Trails.comandante_de_campo,
        Trails.guerreiro,
        Trails.operacoes_especiais,
        Trails.tropa_de_choque,
    ],
    Classes.especialista: [
        Trails.atirador_de_elite,
        Trails.infiltrador,
        Trails.medico_de_campo,
        Trails.negociador,
        Trails.tecnico,
    ],
    Classes.ocultista: [
        Trails.conduite,
        Trails.flagelador,
        Trails.graduado,
        Trails.intuitivo,
        Trails.lamina_paranormal,
    ],
}

CLASS_SUBCLASS_MAP = {
    Classes.mundano: [Subclasses.none],
    Classes.transformado: [
        Subclasses.combatente,
        Subclasses.especialista,
        Subclasses.ocultista,
        Subclasses.none,
    ],
    Classes.ocultista: [
        Subclasses.combatente,
        Subclasses.especialista,
        Subclasses.transformado,
        Subclasses.none,
    ],
    Classes.combatente: [
        Subclasses.ocultista,
        Subclasses.especialista,
        Subclasses.transformado,
        Subclasses.none,
    ],
    Classes.especialista: [
        Subclasses.combatente,
        Subclasses.ocultista,
        Subclasses.transformado,
        Subclasses.none,
    ],
}


class UserFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = User

    username = factory.Sequence(lambda n: f'test{n}')  # type: ignore
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')  # type: ignore
    password = factory.LazyAttribute(lambda obj: f'{obj.username}1301')  # type: ignore
    role = factory.fuzzy.FuzzyChoice(UserRoles)


class CharacterFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = dict

    name = factory.faker.Faker('name')
    age = factory.LazyFunction(lambda: random.randint(1, 999))  # type: ignore
    origin = factory.Iterator(list(Origins))  # type: ignore
    character_class = factory.Iterator(list(Classes))  # type: ignore
    rank = factory.Iterator(list(Ranks))  # type: ignore
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

    @factory.lazy_attribute  # type: ignore
    def subclass(self):
        valid_subclass = CLASS_SUBCLASS_MAP[self.character_class]  # type: ignore
        return random.choice(valid_subclass).value

    @factory.lazy_attribute  # type: ignore
    def trail(self):
        valid_trails = CLASS_TRAIL_MAP[self.character_class]  # type: ignore
        return random.choice(valid_trails).value
