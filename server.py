"""MCP server for CATIA 3D."""

# pylint: disable=invalid-name

from fastmcp import FastMCP

from src.core import SearchProducts
from src.info import GetProductInfo, ProductToInfo
from src.show import ShowProduct


mcp = FastMCP(
    name="CATIA 3D MCP Server",
    dependencies=["pycatia"],
)

mcp.tool(GetProductInfo, name="info")
mcp.tool(ShowProduct, name="show")


@mcp.tool
def search(query: str) -> list[dict[str, str]]:
    """Searches for parts/products by name or part number.
    Use * as wildcard for the query. Example: *015*.
    DO NOT use "*" as query. To discover all products use the info tool.
    Returns a list of part numbers, names and types.
    """

    if not query:
        raise ValueError("Please specify a query.")

    if query == "*":
        raise ValueError("Do not use * as query."
        "To discover the main product (and its children) use the info tool.")

    return [ProductToInfo(product) for product in SearchProducts(query)]


if __name__ == "__main__":
    mcp.run()
