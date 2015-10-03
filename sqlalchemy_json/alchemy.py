from sqlalchemy.ext.mutable import (
    Mutable,
    MutableDict)
from sqlalchemy_utils.types.json import JSONType

from . track import (
    TrackedDict,
    TrackedList)


class NestedMutableDict(TrackedDict, Mutable):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return cls(value)
        return super(cls).coerce(key, value)


class NestedMutableList(TrackedList, Mutable):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, list):
            return cls(value)
        return super(cls).coerce(key, value)


class NestedMutable(Mutable):
    """SQLAlchemy `mutable` extension with nested change tracking."""
    @classmethod
    def coerce(cls, key, value):
        """Convert plain dictionary to NestedMutable."""
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return NestedMutableDict.coerce(key, value)
        if isinstance(value, list):
            return NestedMutableList.coerce(key, value)
        return super(cls).coerce(key, value)


class JsonObject(JSONType):
  """JSON object type for SQLAlchemy with change tracking as base level."""


class NestedJsonObject(JSONType):
  """JSON object type for SQLAlchemy with nested change tracking."""


MutableDict.associate_with(JsonObject)
NestedMutable.associate_with(NestedJsonObject)
