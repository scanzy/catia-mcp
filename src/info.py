"""Functions to get info about a part/product."""

# pylint: disable=invalid-name

from pycatia.product_structure_interfaces.product import Product
from pycatia.enumeration.enumeration_types import cat_vis_property_show

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
def GetProductInfo(name: str = "") -> dict[str, str]:
    """Get info about a part/product by name.
    Leave empty to get info about the main product.
    """

    if "*" in name:
        raise ValueError("Please specify a full name, not a * wildcard.")

    # selects the product, finding by name if provided
    document = GetCatia().active_document
    selection = document.selection
    if name:
        selection.search(f"Name={name},all")
    else:
        assert isinstance(document.product, Product)
        selection.add(document.product)

    # gets the results
    results = selection.items()
    if results.count == 0:
        raise ValueError(f"Product {name} not found")

    # gets info
    itemInfo = ProductToInfo(results[0].value)

    # checks visibility
    itemInfo["visible"] = {
        cat_vis_property_show.index('catVisPropertyShowAttr'): True,
        cat_vis_property_show.index('catVisPropertyNoShowAttr'): False,
    }[selection.vis_properties.get_show()]

    return itemInfo
