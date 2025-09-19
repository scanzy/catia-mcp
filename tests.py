"""Tests for the CATIA 3D MCP Server."""

# pylint: disable=invalid-name

from src.core import SearchProducts, GetProduct
from src.show import ShowProduct

# object to test
PRODUCT_NAME = "C3_015_100.1"


def TestInfo()-> None:
    """Tests the info tool."""
    product = GetProduct(PRODUCT_NAME)
    print(f"Product: {product.name}")
    assert product.name == PRODUCT_NAME


def TestSearch()-> None:
    """Tests the search tool."""

    print(f"Searching for {PRODUCT_NAME}")
    results = SearchProducts(PRODUCT_NAME)
    print(f"Results: {results}")
    assert len(results) == 1
    assert results[0].name == PRODUCT_NAME


def TestShow()-> None:
    """Tests the search tool."""
    ShowProduct(PRODUCT_NAME, True)
    ShowProduct(PRODUCT_NAME, False)


if __name__ == "__main__":
    TestInfo()
    TestSearch()
    TestShow()
