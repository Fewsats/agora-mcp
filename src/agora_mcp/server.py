from mcp.server.fastmcp import FastMCP
from agora.client import Agora
import os
from typing import Dict, List, Optional


# Create FastMCP instance
mcp = FastMCP("Fewsats MCP Server")


def get_agora():
    """Get or create an Agora instance. 
    We want to create the class instance inside the tool, 
    so the init errors will bubble up to the tool and hence the MCP client instead of silently failing
    during the server creation.
    """

    return Agora()


def handle_response(response):
    """
    Handle responses from Agora methods.
    """
    if hasattr(response, 'status_code'):
        # This is a raw response object
        try: return response.status_code, response.json()
        except: return response.status_code, response.text
    # This is already processed data (like a dictionary)
    return response


@mcp.tool()
async def search(q: str, count: int = 20, page: int = 1, 
                price_min: int = 0, price_max: Optional[int] = None, 
                sort: Optional[str] = None, order: Optional[str] = None) -> Dict:
    """
    Search for products matching the query.
    
    Args:
        q: The search query.
        count: The number of products to return per page.
        page: The page number.
        price_min: The minimum price.
        price_max: The maximum price.
        sort: The sort field.
        order: The sort order.
        
    Returns:
        The search results.
    """
    response = get_agora().search_products(
        query=q,
        count=count,
        page=page,
        price_min=price_min,
        price_max=price_max,
        sort=sort,
        order=order
    )
    return handle_response(response)



def main():
    mcp.run()
