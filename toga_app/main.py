import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime
import sys
import os
import requests

# Ensure finance_utils can be imported when running from this subfolder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_app.finance_utils import fetch_close_prices, calculate_ytd_change

class YTDApp(toga.App):
    def startup(self):
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
        results = []
        for ticker in tickers:
            try:
                resp = requests.get("https://pythonapptickets.onrender.com/ytd", params={"ticker": ticker})
                if resp.status_code == 200:
                    data = resp.json()
                    results.append(f"{ticker}: Close={data['close']:.2f}, YTD % Change={data['ytd_pct_change']:.2f}%")
                else:
                    results.append(f"{ticker}: N/A")
            except Exception:
                results.append(f"{ticker}: ERROR")
        self.result_label.value = "\n".join(results)

def main():
    return YTDApp("YTD Analyzer", "org.example.ytdanalyzer")

if __name__ == "__main__":
    main().main_loop()