"""Connects to CATIA and gets the tree structure of the main product."""

from pycatia import catia
from pycatia.product_structure_interfaces.product_document import ProductDocument

# obtains active document
caa = catia()
active_document = caa.active_document
print(f"Active document: {active_document.name}")

# gets opened product
assert isinstance(active_document, ProductDocument)
product = active_document.product
print(f"Main product: {product.part_number} ({product.name})")

# gets sub products
for sub_product in product.products:
    print(f"Children ({sub_product.type}): {sub_product.part_number} ({sub_product.name})")
