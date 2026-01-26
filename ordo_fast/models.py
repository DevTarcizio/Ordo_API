from datetime import datetime

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from ordo_fast.enums import Classes, Origins, Ranks, UserRoles

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
    characters: Mapped[list['Character']] = relationship(
        init=False, cascade='all, delete-orphan', lazy='selectin'
    )


@table_registry.mapped_as_dataclass
class Character:
    __tablename__ = 'characters'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    age: Mapped[int]

    origin: Mapped[Origins] = mapped_column(
        SQLEnum(Origins, name='origins', native_enum=False), nullable=False
    )
    character_class: Mapped[Classes] = mapped_column(
        SQLEnum(Classes, name='classes', native_enum=False), nullable=False
    )
    rank: Mapped[Ranks] = mapped_column(
        SQLEnum(Ranks, name='ranks', native_enum=False), nullable=False
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    nex_total: Mapped[int] = mapped_column(default=0)
    nex_class: Mapped[int] = mapped_column(default=0)
    nex_subclass: Mapped[int] = mapped_column(default=0)

    healthy_points: Mapped[int] = mapped_column(default=0)
    sanity_points: Mapped[int] = mapped_column(default=0)
    effort_points: Mapped[int] = mapped_column(default=0)

    atrib_agility: Mapped[int] = mapped_column(default=0)
    atrib_intellect: Mapped[int] = mapped_column(default=0)
    atrib_vitallity: Mapped[int] = mapped_column(default=0)
    atrib_presence: Mapped[int] = mapped_column(default=0)
    atrib_strength: Mapped[int] = mapped_column(default=0)
