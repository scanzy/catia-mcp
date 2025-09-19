"""MCP server for CATIA 3D."""

# pylint: disable=invalid-name

from fastmcp import FastMCP
from pycatia.product_structure_interfaces.product import Product

from src.show import ShowProduct
from src.core import SearchProducts, GetCatia, GetProduct


mcp = FastMCP(
    name="CATIA 3D MCP Server",
    dependencies=["pycatia"],
)


def ProductToInfo(product: Product) -> dict[str, str]:
    """Converts a product to a dictionary of information."""
    return {
        "name": product.name,
        "part_number": product.part_number,
        "type": product.type,
    }


@mcp.tool
def search(query: str) -> list[dict[str, str]]:
    """Searches for parts/products by name or part number.
    Use * as wildcard for the query. Example: *015*.
    DO NOT use "*" as query. To discover all products use the info tool.
    Returns a list of part numbers, names and types.
    """
    if query == "*":
        raise ValueError("Do not use * as query."
        "To discover all products use the info tool.")

    return [ProductToInfo(product) for product in SearchProducts(query)]


@mcp.tool
def info(name: str = "") -> dict[str, str]:
    """Get info about a part/product by name.
    Leave empty to get info about the main product.
    """
    product = GetProduct(name) if name else GetCatia().active_document.product
    return ProductToInfo(product)


mcp.tool(ShowProduct, name="show")


if __name__ == "__main__":
    mcp.run()
