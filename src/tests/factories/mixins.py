import typing

from factory import Faker
from factory.builder import BuildStep


class UniqueStringMixin(Faker):
    def evaluate(self, instance: typing.Any, step: BuildStep, extra: typing.Any) -> str:
        extra = {"locale": "en_US"}
        value = super().evaluate(instance, step, extra)
        return f"{step.sequence}_{value}"
