"""Connects to CATIA and searches for a product by name."""

from pycatia import catia
from pycatia.product_structure_interfaces.product_document import ProductDocument


# use wildcard
SEARCH_TERM="*C3_015*"


# obtains active document
caa = catia()
active_document = caa.active_document
assert isinstance(active_document, ProductDocument)
selection = active_document.selection

# clears the current selection
selection.clear()

# searches for a product by name
selection.search(f"Name={SEARCH_TERM},all")

results = []
for i in range(1, selection.count2 + 1):
    element = selection.item2(i)
    value = element.value

    # extract part number, name and type
    itemData ={
        'name': value.name if hasattr(value, 'name') else str(value),
        'type': element.type
    }
    results.append(itemData)
    print(itemData)

selection.clear()
