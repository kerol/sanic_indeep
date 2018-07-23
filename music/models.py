# coding: utf-8
import peewee
from common.models import AsyncBaseModel


class Music(AsyncBaseModel):
    name = peewee.CharField(max_length=50)
