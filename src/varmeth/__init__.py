""" Method variant decorator. You specify the desired method variant by a kwarg.

.. code-block:: python
    from varmeth import variable

    class AnimalKingdom(object):
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

        @variable(alias="python")
        def snake(self):
            print("Python Snake")

        @snake.variant("kobra")
        def kobra_snake(self):
            print("Kobra Snake")

        ak = AnimalKindom()
        ak.tiger()                      # >> Default Method!    Tiger
        ak.tiger(method="siberian")     # >> Siberian Tiger
        ak.tiger(method="indian")       # >> Bengal Tiger
        ak.tiger(method="bengal")       # >> Bengal Tiger

        ak.snake()                      # >> Python Snake
        ak.snake(method="python")       # >> Python Snake
        ak.snake(method="kobra")        # >> Kobra Snake
"""


class _default:
    pass


class variable(object):
    """Create a new variable method

    .. code-block:: python
        class FooClass(object):
            @variable
            def foo(self):
                pass
            @foo.variant("bar")
            def foo_variant(self):
                pass
    """

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            # Decorator without parameters
            f = args[0]
            self._name = f.__name__
            self._mapping = {_default: f}
            self._alias = None
        else:
            # Decorator with parameters, the default function comes later in __call__
            self._name = None
            self._mapping = {}
            self._alias = kwargs.get("alias")

    def __call__(self, f):
        if _default in self._mapping:
            raise ValueError("You cannot set the default twice!")
        self._mapping[_default] = f
        if self._alias is not None:
            self._mapping[self._alias] = f
        return self

    def __get__(self, obj, objtype):
        def caller(*args, **kwargs):
            method = kwargs.pop("method", _default)
            if not method:
                method = _default
            try:
                method = self._mapping[method]
            except KeyError:
                raise AttributeError(
                    f"Method {self._name} does not have a variant for {method},"
                    f"valid variants are {', '.join(map(str, list(self._mapping.keys())))}"
                )
            return method(obj, *args, **kwargs)

        return caller

    def variant(self, *names):
        """Register a new variant of a method under a name."""

        def g(f):
            for name in names:
                self._mapping[name] = f

        return g
