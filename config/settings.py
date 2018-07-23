# coding: utf-8
import importlib

from .env import env
settings = importlib.import_module('config.{}'.format(env))
