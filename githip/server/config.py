import os
import warnings
import logging

from functools import partial
from uuid import uuid4

MISSING = uuid4().hex


class Env:
    def __init__(self, name, type_func=str, required=False, default=MISSING):
        self.name = name
        self.type = type_func
        self.required = required
        self.default = default

        if self.required and self.default is not MISSING:
            raise RuntimeError('required with a default doesnt make sense')

    def validate(self, value):
        if value is MISSING:
            if self.required:
                raise RuntimeError('No value for config %s' % self.name)
            elif self.default is not MISSING:
                return self.default
            else:
                warnings.warn('No value for config %s' % self.name)
                return None

        if self.type is bool:
            return str(value).lower() in ('1', 'yes', 'on', 'true')

        if self.type is list or self.type is set:
            if isinstance(value, str):
                value = value.split(',')

        try:
            return self.type(value)
        except (ValueError, TypeError):
            raise RuntimeError(
                'Invalid type for config %s: %s' % (self.name, value)
            )

    def get(self):
        value = os.getenv(self.name, MISSING)
        value = self.validate(value)
        return value


class Config:  # pylint: disable=too-few-public-methods
    def __init__(self):
        for attr in dir(self):
            attr_val = getattr(self, attr)
            if isinstance(attr_val, Env):
                # Validate the attr
                attr_val.get()

    def __getattribute__(self, name):
        """
        This overide allows config attrs to be accessed like:
            config.MY_VALUE
        This is how Sanic is able to copy the config over
        """
        attr = object.__getattribute__(self, name)
        if isinstance(attr, Env):
            attr = attr.get()
        return attr


class Dev(Config):  # pylint: disable=too-few-public-methods
    # Server vars
    DEBUG = True
    LOG_LEVEL = Env('LOG_LEVEL', type_func=partial(getattr, logging),
                    default=logging.INFO)
    PORT = Env('PORT', type_func=int, default=5000)
    KEEP_ALIVE = Env('KEEP_ALIVE', type_func=bool, default=False)
    PRETTY_PRINT_LOGS = Env('PRETTY_PRINT_LOGS', type_func=bool, default=True)
    WORKER_COUNT = 1


class Prod(Dev):  # pylint: disable=too-few-public-methods
    # Server config
    DEBUG = False
    PORT = Env('PORT', type_func=int, required=True)
    WORKER_COUNT = Env('WORKER_COUNT', type_func=int, required=True)

    # These are automatically picked up by sanic because
    # they have the `SANIC_` prefix, but we have them
    # here to be explicit, and to give them types


config_cls = Env('CONFIG_CLS', default='Dev').get()

if config_cls == 'Prod':
    config = Prod()
else:
    if config_cls != 'Dev':
        warnings.warn('Incorrect config_cls specified %s' % config_cls)
    config = Dev()


def get(name, default=None):
    return getattr(config, name, default)
