from sqlalchemy import Column, MetaData, Table
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, Text


metadata = MetaData()

MYSQL_DEFAULTS = {
    "mysql_engine": "InnoDB",
    "mysql_charset": "utf8"
}

rooms = Table(
    "rooms", metadata,
    Column("id", Integer, primary_key=True),  # pkgKey
    Column("name", Text, nullable=False),
    UniqueConstraint("name"),
    **MYSQL_DEFAULTS
)

items = Table(
    "items", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("room_id", Integer, ForeignKey("rooms.id"), nullable=False),
    Column("weight", Integer, nullable=False),
    Column("description", Text, nullable=False),
    Column("is_fragile", Boolean, nullable=False),
    **MYSQL_DEFAULTS
)
