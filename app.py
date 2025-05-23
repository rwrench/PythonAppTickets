from flask import Flask, render_template_string, request
from datetime import datetime
from finance_utils import fetch_close_prices, calculate_ytd_change

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        tickers = request.form.get('tickers', 'MSFT,AAPL,MSTR').split(',')
        today = datetime.today().strftime('%Y-%m-%d')
        start_of_year = f'{datetime.today().year}-01-01'
        results = []
        for ticker in [t.strip().upper() for t in tickers if t.strip()]:
            try:
                close = fetch_close_prices(ticker, start_of_year, today)
                if close is not None:
                    latest_close, ytd_pct_change = calculate_ytd_change(close)
                    results.append((ticker, latest_close, ytd_pct_change))
                else:
                    results.append((ticker, None, None))
            except Exception as e:
                results.append((ticker, 'ERROR', None))
        result = results
    return render_template_string('''
        <h2>YTD % Change Calculator</h2>
        <form method="post">
            Tickers (comma separated): <input name="tickers" value="MSFT,AAPL,MSTR">
            <input type="submit" value="Calculate">
        </form>
        {% if result %}
            <table border="1" cellpadding="5">
                <tr><th>Ticker</th><th>Close</th><th>YTD % Change</th></tr>
                {% for ticker, close, ytd in result %}
                    <tr>
                        <td>{{ ticker }}</td>
                        <td>
                            {% if close is none %}
                                N/A
                            {% elif close == 'ERROR' %}
                                ERROR
                            {% else %}
                                {{ "%.2f"|format(close) }}
                            {% endif %}
                        </td>
                        <td>
                            {% if ytd is none %}
                                N/A
                            {% else %}
                                {{ "%.2f"|format(ytd) }}%
                            {% endif %}
                        </td>
                    </tr>
                {% endfor %}
            </table>
        {% endif %}
        {% if error %}
            <p style="color:red;">{{ error }}</p>
        {% endif %}
    ''', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)

from app import app as application  # noqa
