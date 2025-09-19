"""Tests for the CATIA 3D MCP Server."""

# pylint: disable=invalid-name
# pylint: disable=missing-docstring

import json
from src.core import SearchProducts
from src.info import GetProductInfo, ProductToInfo
from src.show import ShowProduct


# CATIA 3D object name to test
PRODUCT_NAME = "C3_015_100.1"
SEARCH_TERM = "C3_0*"


def PrettyJson(data) -> str:
    return json.dumps(data, indent=2)


def TestInfo()-> None:

    mainProduct = GetProductInfo()
    print(f"Main Product: {PrettyJson(mainProduct)}")

    product = GetProductInfo(PRODUCT_NAME)
    print(f"Target product: {PrettyJson(product)}")
    assert product['name'] == PRODUCT_NAME


def TestSearchSingle()-> None:

    print(f"Searching for {PRODUCT_NAME}")
    results = SearchProducts(PRODUCT_NAME)

    assert len(results) == 1, "More than one product found"
    assert results[0].name == PRODUCT_NAME, "Product name does not match"
    print(f"Result: {PrettyJson(ProductToInfo(results[0]))}")


def TestSearchMultiple()-> None:

    print(f"Searching for {SEARCH_TERM}")
    results = SearchProducts(SEARCH_TERM)
    print(f"Results: {PrettyJson(list(map(ProductToInfo, results)))}")


def TestShow()-> None:
    ShowProduct(PRODUCT_NAME, True)
    ShowProduct(PRODUCT_NAME, False)


if __name__ == "__main__":
    TestInfo()
    TestSearchSingle()
    TestSearchMultiple()
    TestShow()
