"""Functions to get info about a part/product."""

# pylint: disable=invalid-name

import typing as t
from pycatia.product_structure_interfaces.product import Product
from pycatia.enumeration.enumeration_types import cat_vis_property_show
from pycatia.product_structure_interfaces.product_document import ProductDocument

from src.core import GetCatia, UsesSelection


def ProductToInfo(product: Product) -> dict[str, str]:
    """Converts a product to a dictionary of information."""
    info = {}
    for field in ["name", "type", "part_number"]:
        try:
            info[field] = getattr(product, field)
        except AttributeError:
            pass
    return info


@UsesSelection
def GetProductInfo(name: str = "", includeChildren: bool = False) -> dict[str, t.Any]:
    """Get info about a part/product by name, with its
    Leave empty to get info about the main product.
    """

    if "*" in name:
        raise ValueError("Please specify a full name, not a * wildcard.")

    # selects the product, finding by name if provided
    document = GetCatia().active_document
    selection = document.selection
    if name:
        selection.search(f"Name={name},all")

    # or the main product
    else:
        assert isinstance(document, ProductDocument)
        assert isinstance(document.product, Product)
        selection.add(document.product)

    # gets the results
    if selection.count2 == 0:
        raise ValueError(f"Product {name} not found")

    # gets info
    product = Product(selection.item2(1).value.com_object)
    itemInfo: dict[str, t.Any] = ProductToInfo(product)

    # checks visibility
    itemInfo["visible"] = {
        cat_vis_property_show.index('catVisPropertyShowAttr'): True,
        cat_vis_property_show.index('catVisPropertyNoShowAttr'): False,
    }[selection.vis_properties.get_show()] # type: ignore

    # builds product
    if includeChildren:
        itemInfo["children"] = [ProductToInfo(child) for child in product.products]

    return itemInfo
