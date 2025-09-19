"""Functions to control the visibility of a part/product."""

# pylint: disable=invalid-name

from pycatia.enumeration.enumeration_types import cat_vis_property_show
from src.core import GetCatia, UsesSelection


@UsesSelection
def ShowProduct(name: str, visible: bool) -> None:
    """Toggles the visibility of a part/product.
    Set visible to True to show, False to hide.
    """

    # gets string representation of visible/hidden
    prop = 'catVisPropertyShowAttr' if visible else 'catVisPropertyNoShowAttr'

    # searches for the product
    selection = GetCatia().active_document.selection
    selection.search(f"Name={name},all")

    if selection.count == 0:
        raise ValueError(f"Product {name} not found")

    # sets the show property
    selection.vis_properties.set_show(cat_vis_property_show.index(prop))
