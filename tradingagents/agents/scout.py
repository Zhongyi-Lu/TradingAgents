import yfinance as yf
import pandas as pd
from rich.console import Console

console = Console()

def run_scan(verbose: bool = False):
    """
    Scans a predefined list of stocks to find potential trading opportunities.

    The current MVP logic identifies stocks trading above their 200-day
    Simple Moving Average (SMA), which is often considered a bullish signal.

    Args:
        verbose (bool): If True, prints detailed progress during the scan.

    Returns:
        list: A list of stock tickers that meet the scan criteria.
    """
    # MVP: Use a hardcoded list of stocks. Future versions could read this from a file.
    stock_pool = ["AAPL", "GOOGL", "MSFT", "AMZN", "NVDA", "TSLA", "META", "JPM", "V", "JNJ"]
    bullish_stocks = []

    if verbose:
        console.print(f"[bold blue]Scout is scanning {len(stock_pool)} stocks...[/bold blue]")

    for ticker in stock_pool:
        try:
            if verbose:
                console.print(f"  - Analyzing [yellow]{ticker}[/yellow]...")
            
            # Download historical data for the last year
            stock_data = yf.download(ticker, period="1y", progress=False)

            if stock_data.empty:
                if verbose:
                    console.print(f"    [red]Could not download data for {ticker}. Skipping.[/red]")
                continue

            # Calculate 200-day SMA. Use .values[-1] to get the raw numpy value.
            sma_200 = stock_data['Close'].rolling(window=200).mean().values[-1]
            
            # Get the last closing price. Use .values[-1] to get the raw numpy value.
            last_price = stock_data['Close'].values[-1]

            # The screening logic
            if last_price > sma_200:
                bullish_stocks.append(ticker)
                if verbose:
                    console.print(f"    [green]Bullish signal found for {ticker}! (Price: ${float(last_price):.2f}, 200-SMA: ${float(sma_200):.2f})[/green]")

        except Exception as e:
            if verbose:
                console.print(f"    [red]An error occurred while processing {ticker}: {e}[/red]")

    if verbose:
        console.print(f"[bold blue]Scout finished scanning.[/bold blue]")

    return bullish_stocks

if __name__ == '__main__':
    # For direct testing of the module
    console.print("[bold]Running Scout module directly for testing...[/bold]")
    found_stocks = run_scan(verbose=True)
    console.print(f"[bold]Test complete.[/bold] Found stocks: {found_stocks}")
