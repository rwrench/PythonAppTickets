"""
My first Python app to get Stock Ticker data and show close and YTD% growth
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from datetime import datetime
from .finance_utils import fetch_close_prices, calculate_ytd_change


class StockTickerYTDAnalyzer(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN, margin=10, width=400))

        self.ticker_input = toga.TextInput(
            value="MSFT,AAPL,MSTR",
            placeholder="Tickers (e.g. MSFT,AAPL,MSTR)",
            style=Pack(flex=1, margin_bottom=10)
        )
        self.result_label = toga.MultilineTextInput(
            readonly=True,
            style=Pack(height=200, flex=1, margin_top=10)
        )
        run_button = toga.Button("Calculate", on_press=self.run_analysis, style=Pack(margin_top=10))

        main_box.add(self.ticker_input)
        main_box.add(run_button)
        main_box.add(self.result_label)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def run_analysis(self, widget):
        tickers = [t.strip().upper() for t in self.ticker_input.value.split(',') if t.strip()]
        today = datetime.today().strftime('%Y-%m-%d')
        start_of_year = f'{datetime.today().year}-01-01'
        results = []
        for ticker in tickers:
            try:
                close = fetch_close_prices(ticker, start_of_year, today)
                if close is not None:
                    latest_close, ytd_pct_change = calculate_ytd_change(close)
                    results.append(f"{ticker}: Close={latest_close:.2f}, YTD % Change={ytd_pct_change:.2f}%")
                else:
                    results.append(f"{ticker}: N/A")
            except Exception:
                results.append(f"{ticker}: ERROR")
        self.result_label.value = "\n".join(results)


def main():
    return StockTickerYTDAnalyzer("YTD Analyzer", "org.example.ytdanalyzer")
