from mcp.server.fastmcp import FastMCP
import yfinance as yf

# Create the MCP server instance
mcp_server = FastMCP("Stock Price Server")

# Define the tool the AI client can use
@mcp_server.tool()
def get_stock_price(symbol: str) -> float:
    """
    Retrieve the current stock price for a given ticker symbol.
    Returns the latest closing price as a floating-point number.
    """
    try:
        ticker = yf.Ticker(symbol)
        # Fetch the latest closing price
        hist = ticker.history(period="1d")
        return hist["Close"].iloc[0]
    except IndexError:
        raise ValueError(f"Could not retrieve stock price for symbol: {symbol}")

@mcp_server.tool()
def server_hello(input_line: str) -> str:
    try:
        return f"server_hello: {input_line}"
    except IndexError:
        raise ValueError(f"Could not give the simple string")
    
# Start the server when the script is run directly
if __name__ == "__main__":
    print("Starting MCP server...")
    mcp_server.run()

