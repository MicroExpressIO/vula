# File: stock_client.py (corrected)
import asyncio
from fastmcp import Client
from stock_server import mcp_server  # Import the server instance

async def main():
    print("Connecting to in-memory MCP server...")
    # Use the in-memory transport to connect directly to the server object
    async with Client(mcp_server) as client:
        # List all available tools on the server
        print("Listing available tools...")
        # CORRECT: The client.list_tools() method returns a list directly.
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]
        print(f"Available tools: {tool_names}")

        
        # Call the get_stock_price tool
        #symbol = "AAPL"
        #print(f"\nCalling get_stock_price tool for symbol: {symbol}")
        #result = await client.call_tool("get_stock_price", {"symbol": symbol})

        words = "TSLA"
        print(f"\n Calling ...worlds: {words}")
        ret_mcp = await client.call_tool("server_hello", {"input_line": words})
        """
        # Process the result from the server
        if result.structuredContent:
            # The result is nested under the 'result' key
            stock_price = result.structuredContent.get("result")
        else:
            print(f"Received unstructured content: {result.content.text}")
        """

        if ret_mcp.structured_content:
            ret = ret_mcp.structured_content.get("result")
            #print(f"\n ret: {ret_mcp.structured_content}")
            print(f"\n. ret : {ret}")
        else:
            print("\n in else")
            print(f"Received unstrucuted context: {ret_mcp.content.text}")

        """
        # Example of an invalid symbol
        invalid_symbol = "INVALID"
        print(f"\nCalling get_stock_price tool for invalid symbol: {invalid_symbol}")
        try:
            await client.call_tool("get_stock_price", {"symbol": invalid_symbol})
        except ValueError as e:
            print(f"Caught expected error: {e}")
        """    

if __name__ == "__main__":
    asyncio.run(main())
