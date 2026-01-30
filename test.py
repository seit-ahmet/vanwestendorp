import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("my_data.csv")

# Rename columns for convenience (optional but safer)
df = df.rename(columns={
    "Too Cheap": "too_cheap",
    "Cheap": "cheap",
    "Expensive": "expensive",
    "Too Expensive": "too_expensive"
})

# Create a common price range
prices = np.sort(
    np.unique(
        np.concatenate([
            df["too_cheap"],
            df["cheap"],
            df["expensive"],
            df["too_expensive"]
        ])
    )
)

# Cumulative function
def cumulative(series, prices, reverse=False):
    if reverse:
        return np.array([100 * (series >= p).mean() for p in prices])
    else:
        return np.array([100 * (series <= p).mean() for p in prices])

# Van Westendorp curves
too_cheap = cumulative(df["too_cheap"], prices)
cheap = cumulative(df["cheap"], prices)
expensive = cumulative(df["expensive"], prices, reverse=True)
too_expensive = cumulative(df["too_expensive"], prices, reverse=True)

# Helper to find intersection
def intersection_price(curve1, curve2, prices):
    idx = np.argmin(np.abs(curve1 - curve2))
    return prices[idx]

# Van Westendorp points
IPP = intersection_price(cheap, expensive, prices)
OPP = intersection_price(too_cheap, too_expensive, prices)
PMC = intersection_price(too_cheap, expensive, prices)
PME = intersection_price(cheap, too_expensive, prices)

# Plot
plt.figure(figsize=(10, 6))

plt.plot(prices, too_cheap, label="Too Cheap")
plt.plot(prices, cheap, label="Cheap")
plt.plot(prices, expensive, label="Expensive")
plt.plot(prices, too_expensive, label="Too Expensive")

# Vertical markers
plt.axvline(IPP, linestyle="--", linewidth=1, label=f"Indifference Price Point = {IPP}")
plt.axvline(OPP, linestyle="--", linewidth=1, label=f"Optimal Price Point = {OPP}")

# Shade acceptable range
plt.axvspan(PMC, PME, alpha=0.1, color="blue", label="Min-Max Price Range")

plt.xlabel("Price")
plt.ylabel("Percentage of respondents (%)")
plt.title("Van Westendorp Price Sensitivity Meter")
plt.legend()
plt.grid(True)

plt.show()