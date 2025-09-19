"""Core functions for the CATIA 3D MCP Server."""

# pylint: disable=invalid-name

from functools import wraps
from typing import Callable

from pycatia import catia
from pycatia.in_interfaces.application import Application
from pycatia.product_structure_interfaces.product import Product


# lazy-loaded CATIA instance
CATIA = None

def GetCatia() -> Application:
    """Gets the CATIA 3D instance."""

    global CATIA # pylint: disable=global-statement
    if CATIA is None:
        CATIA = catia()
    return CATIA


def UsesSelection(func: Callable) -> Callable:
    """Wraps a function to store, then restore the selection, after the function is called.
    This is useful for pycatia tools that modify the selection.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        # store the selection
        selection = GetCatia().active_document.selection
        items = [item.value for item in selection.items()]

        # runs the function with the selection cleared
        selection.clear()
        result = func(*args, **kwargs)

        # restores the selection
        selection.clear()
        for item in items:
            selection.add(item)
        return result

    return wrapper


@UsesSelection
def SearchProducts(query: str) -> list[Product]:
    """Searches for products by name.
    Use * as wildcard for the query. Example: *015*.
    """

    selection = GetCatia().active_document.selection
    selection.search(f"Name={query},all")
    return [item.value for item in selection.items()]


def GetProduct(name: str) -> Product:
    """Gets a product by name, raising ValueError if not found."""

    try:
        return next(product for product in SearchProducts(name) if product.name == name)
    except StopIteration:
        raise ValueError(f"Product {name} not found") # pylint: disable=raise-missing-from
