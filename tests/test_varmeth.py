import sys

import pytest
from varmeth import variable


class AnimalKindom(object):
    @variable
    def tiger(self):
        print("Default Method!")
        print("Tiger")
        return self.call_meth_name

    @tiger.variant("siberian")
    def siberian_tiger(self):
        print("Siberian Tiger")
        return self.call_meth_name

    @tiger.variant("indian", "bengal")
    def bengal_tiger(self):
        print("Bengal Tiger")
        return self.call_meth_name

    @variable(alias="python")
    def snake(self):
        print("Python Snake")
        return self.call_meth_name

    @snake.variant("kobra")
    def kobra_snake(self):
        print("Kobra Snake")
        return self.call_meth_name

    @property
    def call_meth_name(self):
        """return name of caller method"""
        return sys._getframe(1).f_code.co_name


class MultiDefaultA:
    @variable(alias="b")
    @variable
    def foo(self):
        pass


class MultiDefaultB:
    @variable(alias="a")
    @variable(alias="b")
    def foo(self):
        pass


def test_variable_without_alias():
    ak = AnimalKindom()

    # check default call
    assert ak.tiger() == "tiger"

    # check variant method execution
    assert ak.tiger(method="siberian") == "siberian_tiger"
    assert ak.tiger(method="indian") == "bengal_tiger"
    assert ak.tiger(method="bengal") == "bengal_tiger"


def test_variable_with_alias():
    ak = AnimalKindom()

    # check default call
    assert ak.snake() == "snake"
    # python is alias for snake
    assert ak.snake(method="python") == "snake"
    # check variant method execution
    assert ak.snake(method="kobra") == "kobra_snake"


@pytest.mark.parametrize("cls", [MultiDefaultA, MultiDefaultB])
def test_not_allow_multi_default(cls):
    _cls = cls()
    with pytest.raises(ValueError):
        _cls.foo()
