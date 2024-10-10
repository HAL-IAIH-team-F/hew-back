from sqlalchemy import types


class UUID(types.TypeDecorator):
    cache_ok = True


def process_bind_param(value, dialect):
