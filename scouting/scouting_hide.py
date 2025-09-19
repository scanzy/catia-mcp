"""Connects to CATIA and hides the main product."""

import time
from pycatia import catia  
from pycatia.enumeration.enumeration_types import cat_vis_property_show
from pycatia.product_structure_interfaces.product_document import ProductDocument


# gets show and hide properties
visible = cat_vis_property_show.index('catVisPropertyShowAttr')
hidden = cat_vis_property_show.index('catVisPropertyNoShowAttr')

# obtains active document and product
caa = catia()
active_document = caa.active_document
assert isinstance(active_document, ProductDocument)
product = active_document.product

# selects the product
selection = caa.active_document.selection
selection.clear()
selection.add(product)

# hides the main product, waits, then shows it
selection.vis_properties.set_show(hidden)
time.sleep(1)
selection.vis_properties.set_show(visible)
selection.clear()
