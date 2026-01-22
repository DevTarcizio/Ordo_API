from datetime import datetime

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from ordo_fast.enums import TaskState, UserRoles, Origins, Classes, Trails, Ranks

table_registry = registry()




@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[UserRoles] = mapped_column(
        SQLEnum(UserRoles, name='userroles', native_enum=True),
        nullable=False,
        default=UserRoles.player,
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    tasks: Mapped[list['Task']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )
    characters: Mapped[list['Character']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin'
    )


@table_registry.mapped_as_dataclass
class Task:
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TaskState]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

@table_registry.mapped_as_dataclass
class Character:
    __tablename__ = 'characters'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    nex: Mapped[int]
    origin: Mapped[Origins] = mapped_column(
        SQLEnum(Origins, name='charactersorigins', native_enum=True),
        nullable=False
    )
    character_class: Mapped[Classes] = mapped_column(
        SQLEnum(Classes, name='charactersclasses', native_enum=True),
        nullable=False
    )
    trail: Mapped[Trails] = mapped_column(
        SQLEnum(Trails, name='characterstrails', native_enum=True),
        nullable=False
    )
    rank: Mapped[Ranks] = mapped_column(
        SQLEnum(Ranks, name='charactersRanks', native_enum=True),
        nullable=False
    )
    healty_points: Mapped[int]
    sanity_points: Mapped[int]
    effort_points: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))