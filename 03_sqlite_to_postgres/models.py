import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class FilmWork:
    title: str
    description: str
    creation_date: datetime.date
    type: str
    file_path: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmWork:
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmWork:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
