import typing
from datetime import datetime

import attr
import dateutil.parser

from .links import Links
from .relationships import Relationship


@attr.dataclass
class NicknamesAttributes:
    lastQuit: str
    lastRealHost: str
    lastSeen: datetime = attr.ib(converter=dateutil.parser.parse)
    lastRealName: str
    lastUserMask: str
    display: str
    nick: str
    createdAt: datetime = attr.ib(converter=dateutil.parser.parse)
    updatedAt: typing.Optional[datetime] = attr.ib(
        converter=attr.converters.optional(dateutil.parser.parse)
    )
    vhost: str
    email: str
    score: int
    """ edit distance from API match """


@attr.dataclass
class NicknamesRelationships:
    user: Relationship = attr.ib(
        validator=attr.validators.instance_of(Relationship)
    )
    rat: Relationship = attr.ib(
        validator=attr.validators.instance_of(Relationship)
    )


@attr.dataclass
class Nicknames:
    id: int
    attributes: NicknamesAttributes = attr.ib(
        validator=attr.validators.instance_of(NicknamesAttributes)
    )
    relationships: NicknamesRelationships = attr.ib(
        validator=attr.validators.instance_of(NicknamesRelationships)
    )
    links: Links = attr.ib(
        validator=attr.validators.instance_of(dict)
    )
    type: str = "nicknames"
