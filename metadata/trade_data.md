# Binance Trade Columns Explanation

- **info**  
  - Type: `dict`  
  - Raw JSON returned by the exchange for this trade. Useful for debugging or accessing extra fields.

- **timestamp**  
  - Type: `int` (milliseconds since Unix epoch)  
  - Exact time the trade occurred. Essential for time-based aggregation (1-min, 5-min).

- **datetime**  
  - Type: `string` (ISO 8601)  
  - Human-readable version of `timestamp`. Convenient for plotting and filtering.

- **symbol**  
  - Type: `string`  
  - Trading pair, e.g., `BTC/USDT`. Useful when filtering trades.

- **id**  
  - Type: `string` or `int`  
  - Unique trade identifier. Ensures no duplicates.

- **order**  
  - Type: `string` or `None`  
  - Order ID associated with the trade. Often `None` for market trades.

- **type**  
  - Type: `string` (`'limit'` or `'market'`)  
  - Type of order that generated the trade. Optional for trade count modeling.

- **side**  
  - Type: `string` (`'buy'` or `'sell'`)  
  - Indicates trade direction. Can be used to distinguish buy vs sell counts.

- **takerOrMaker**  
  - Type: `string` (`'taker'` or `'maker'`)  
  - Taker: executed against existing order (removes liquidity)  
  - Maker: added liquidity to the order book. Optional for basic counts.

- **price**  
  - Type: `float`  
  - Execution price of the trade. Optional for count modeling, but useful for volume analysis.

- **amount**  
  - Type: `float`  
  - Units traded (e.g., BTC). Can be summed for total volume per interval.

- **cost**  
  - Type: `float`  
  - `price * amount`, total value in quote currency. Useful for weighted analysis.

- **fee**  
  - Type: `dict` (`cost`, `currency`, `rate`)  
  - Fee charged for this trade. Often optional for trade count analysis.

- **fees**  
  - Type: `list` of dicts  
  - Multiple fees per trade (e.g., maker/taker, network fees). Usually optional.

---

### **Essential Columns for Trade Count Modeling**
- `timestamp` or `datetime` → for interval aggregation  
- `symbol` → if filtering by trading pair  
- `amount` or `cost` → for total volume  
- `side` → if distinguishing buy vs sell counts
