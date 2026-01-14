import factory
import factory.fuzzy

from ordo_fast.models import Task, TaskState, User


class UserFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = User

    username = factory.Sequence(lambda n: f'test{n}')  # type: ignore
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')  # type: ignore
    password = factory.LazyAttribute(lambda obj: f'{obj.username}1301')  # type: ignore


class TaskFactory(factory.Factory):  # type: ignore
    class Meta:  # type: ignore
        model = Task

    title = factory.faker.Faker('text')
    description = factory.faker.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TaskState)
    user_id = 1
