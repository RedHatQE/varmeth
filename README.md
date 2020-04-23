<h1 align="center"> varmeth </h1>
<h2 align="center"> Method Variant Decorator </h2>

<p align="center">
    <a href="https://pypi.org/project/varmeth">
    <img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/varmeth.svg?style=flat">
    </a>
    <a href="https://pypi.org/project/varmeth/#history">
    <img alt="PyPI version" src="https://badge.fury.io/py/varmeth.svg">
    </a>
    <a href="https://codecov.io/gh/digitronik/varmeth">
    <img src="https://codecov.io/gh/digitronik/varmeth/branch/master/graph/badge.svg" />
    </a>
    <a href="https://github.com/digitronik/varmeth/actions">
    <img alt="github actions" src="https://github.com/digitronik/varmeth/workflows/Tests/badge.svg?branch=master">
    </a>
    <a href="https://github.com/digitronik/varmeth/blob/master/LICENSE">
    <img alt="License: GPLv3" src="https://img.shields.io/pypi/l/varmeth.svg?version=latest">
    </a>
    <a href="https://pypi.org/project/black">
    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
</p>


This is simple library providing decorator to invoke different variant of class methods.

## Installation and usage

### Installation

`varmeth` can be installed by running `pip install varmeth`


### Usage

Below example can show you how to use `varmeth`. You can see a different _method variant_.
You’ll have to decorate _default method_ with `variable` and register it with different _method variant_.
You can also register _variant_ with multiple names.

```python
from varmeth import variable

class CatFamily(object):
   @variable
   def tiger(self):
       print("Default Method!")
       print("Tiger")

   @tiger.variant("siberian")
   def siberian_tiger(self):
       print("Siberian Tiger")

   @tiger.variant("indian", "bengal")
   def bengal_tiger(self):
       print("Bengal Tiger")
```

To access different _method variant_; you need to pass the `method` argument as a registered _variant’s name_.

```shell script
In [1]: cat = CatFamily()

In [2]: cat.tiger()
Default Method!
Tiger

In [3]: cat.tiger(method="siberian")
Siberian Tiger

In [4]: cat.tiger(method="indian")
Bengal Tiger

In [5]: cat.tiger(method="bengal")
Bengal Tiger
```

You can add `alias` to the _default method_ but multiple default methods are not allowed.

```python
from varmeth import variable

class Reptiles(object):
   @variable(alias="python")
   def snake(self):
       print("Python Snake")

   @snake.variant("kobra")
   def kobra_snake(self):
       print("Kobra Snake")
```
```shell script
In [1]: rep = Reptiles()

In [2]: rep.snake()
Python Snake

In [3]: rep.snake(method="python")
Python Snake

In [4]: rep.snake(method="kobra")
Kobra Snake
```
- _varmeth_ was part of [ManageIQ Integration test](https://github.com/ManageIQ/integration_tests).
Let's take an example from it. Suppose we have _Entity_ which supports _deletion_ operation with `UI` and `REST`.

<table>
<tr>
<th> Normal Approach </th>
<th> varmeth Approach </th>
</tr>
<tr>
<td>

```python
class Entity(object):
    def delete_ui(self):
        print("Delete with UI!")

    def delete_rest(self):
        print("Delete with REST!")

entity = Entity()
entity.delete_ui()      # >> Delete with UI!
entity.delete_rest()    # >> Delete with REST!
```
</td>

<td>

```python
from varmeth import variable

class Entity(object):
    @variable(alias="ui")
    def delete(self):
        print("Delete with UI!")

    @delete.variant("rest")
    def delete_rest(self):
        print("Delete with REST!")

entity = Entity()
entity.delete()                 # >> Delete with UI!
entity.delete(method="ui")      # >> Delete with UI!
entity.delete(method="rest")    # >> Delete with REST!
```
</td>
</tr>
</table>

- The _varmeth approach_ will help you in `context` switching.
That will be helpful in test parameterization. In above example,
We can easily parametrize tests for `UI` and `REST`.

```python
import pytest

@pytest.mark.parametrize("context", ["ui", "rest"])
def test_delete_entity(context):
   entity = Entity()
   entity.delete(method=context)
```

### Contribute

- Install in the development mode `pip install -e .`
- Test your changes
    - Install _nox_ `pip install nox`
    - Run _pre-commit_ and _tests_ `nox`
- Send a pull request
