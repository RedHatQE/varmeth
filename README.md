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

Simple library that allows a method to choose dynamically implementation at runtime depending on the
context via decorators.

_Varmeth_ was originally part of [ManageIQ Integration test](https://github.com/ManageIQ/integration_tests) library.

## Installation and usage

### Installation

`varmeth` can be installed by running `pip install varmeth`

### Usage

Below example can show you how to use `varmeth`. You can see a different _method variant_.
You’ll have to decorate _default method_ with `variable` and register it with different _method variant_.
You can also register _variant_ with multiple names.

The following code snippet shows how to use `varmeth` in a real world example:

In this example, the `tiger` method will change it's implementation based on the context at
runtime, so it must be annotated with the `@variable` annotation in order to do so. It will be
the _variable_ method.

The body of this method will be the `default` implementation - the implementation used for this
method when no context is explicitly used.

The `siberian_tiger` and `bengal_tiger` are two different implementations for the `tiger` method,
and need to be annotated with `@tiger.variant("variant-name")` annotations, where `variant-name`
is a string identifier that will be used at runtime to select the required `variant` implementation.
These will be the _variants_.

Note that the _variable_ method can be associated with multiple implementations or _variants_:

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
<br>

To choose between the different _variants_ , the `method` parameter is used to select
the proper context, using the proper _variant-name_ as a value:

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
<br>

You can also add and alias name to the _default_ method using the `alias` parameter, though note
that **only one `default` method is allowed**.

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
<br>

### Using Varmeth against plain Python implementation

The following example shows an _Entity_ class that supports the _delete_ operation for two different contexts, the `UI`
(front-end) and the `REST` (back-end) contexts. As you can infer, each context requires very different implementations
to get the entity removed.

Using vanilla Python implementation you will have to call the proper method for each context,
_explicitly_.

Instead, you can simply call the same method and provide the context, and `Varmeth` will do the
rest.

<table>
<tr>
<th> Plain Python </th>
<th> Varmeth </th>
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

<br>

As you can see, _Varmeth_ provides a very convenient _context switcher_ interface, which some may
find handy when implementing integration tests designed to follow test parametrization patterns,
like [some popular test frameworks such as Pytest](http://doc.pytest.org/en/latest/example/parametrize.html#parametrizing-tests).
offer. The following is an example of how to do exactly that with Pytest using `Varmeth`: we can
easily parametrize the _context under test_ using `UI` and `REST` as parameters:


```python
import pytest

@pytest.mark.parametrize("context", ["ui", "rest"])
def test_delete_entity(context):
   entity = Entity()
   entity.delete(method=context)
```

### Contribute

Feel free to create Issues if you find bugs, or go ahead and submit your own Pull Requests.

**Please note**: When submitting new PRs, ensure your code passes all checks.
