
import robin_stocks.robinhood as r
import pandas as pd
import plotly.graph_objects as go


def main_holdings():
    holdings = r.build_holdings()
    hold_list = [{"symbol": k, **v} for k, v in holdings.items()]
    df = pd.DataFrame(hold_list)
    df = df[
        [
            "name",
            "symbol",
            "equity",
            "price",
            "quantity",
            "average_buy_price",
            "equity_change",
            "pe_ratio",
            "percentage",
        ]
    ]
    return df.to_dict("records")


def l2_data(symbol: str):
    data = r.get_pricebook_by_symbol(symbol)
    to_insert = []
    for key in ("asks", "bids"):
        _data = data[key]
        for row in _data:
            to_insert.append(
                {
                    "side": row["side"],
                    "currency": row["price"]["currency_code"],
                    "price": float(row["price"]["amount"]),
                    "quantity": float(row["quantity"]),
                }
            )
    return to_insert


def l2_chart(
    symbol: str, min_price: float | None = None, max_price: float | None = None
):
    df = pd.DataFrame(l2_data(symbol))
    # Separate and sort ask and bid orders
    ask_orders = df[df["side"] == "ask"].sort_values("price")
    bid_orders = df[df["side"] == "bid"].sort_values("price", ascending=False)

    # Calculate cumulative quantities
    ask_orders["cumulative_quantity"] = ask_orders["quantity"].cumsum()
    bid_orders["cumulative_quantity"] = bid_orders["quantity"].cumsum()

    # Calculate the current price (midpoint between highest bid and lowest ask)
    current_price = (bid_orders["price"].max() + ask_orders["price"].min()) / 2

    # Define the price range to display
    min_price = min_price or (current_price * 0.5)
    max_price = max_price or (current_price * 1.5)

    # Filter the data to the specified range
    ask_orders_filtered = ask_orders[
        (ask_orders["price"] >= min_price) & (ask_orders["price"] <= max_price)
    ]
    bid_orders_filtered = bid_orders[
        (bid_orders["price"] >= min_price) & (bid_orders["price"] <= max_price)
    ]

    # Create the figure
    fig = go.Figure()

    # Add ask orders (sell orders)
    fig.add_trace(
        go.Scatter(
            x=ask_orders_filtered["price"],
            y=ask_orders_filtered["cumulative_quantity"],
            name="Ask",
            line=dict(color="red", width=2),
            fill="tozeroy",
            mode="lines",
        )
    )

    # Add bid orders (buy orders)
    fig.add_trace(
        go.Scatter(
            x=bid_orders_filtered["price"],
            y=bid_orders_filtered["cumulative_quantity"],
            name="Bid",
            line=dict(color="green", width=2),
            fill="tozeroy",
            mode="lines",
        )
    )

    # Add a line for the current price
    fig.add_shape(
        type="line",
        x0=current_price,
        y0=0,
        x1=current_price,
        y1=1,
        yref="paper",
        line=dict(color="black", width=2, dash="dash"),
    )

    # Customize the layout
    fig.update_layout(
        title=f"{symbol} Order Book Depth Chart",
        xaxis_title="Price (USD)",
        yaxis_title="Cumulative Quantity",
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        xaxis=dict(range=[min_price, max_price]),
    )

    # Customize hover information
    fig.update_traces(
        hovertemplate="Price: $%{x:.2f}<br>Cumulative Quantity: %{y}<extra></extra>"
    )

    return fig.to_json()
