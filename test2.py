import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Load CSV file
df = pd.read_csv("my_data.csv")

# Define function to plot Van Westendorp graph
def van_westendorp_plot(df_product, product_name='Product', save_path=None):
    too_cheap = df_product.iloc[:, 0]
    cheap = df_product.iloc[:, 1]
    expensive = df_product.iloc[:, 2]
    too_expensive = df_product.iloc[:, 3]

    # x-axis range
    x_min = min(df_product.min())
    x_max = max(df_product.max())
    x = np.linspace(x_min, x_max, 500)

    # CDFs
    cdf_too_cheap = [np.mean(too_cheap <= val) for val in x]
    cdf_cheap = [np.mean(cheap <= val) for val in x]
    cdf_expensive = [np.mean(expensive <= val) for val in x]
    cdf_too_expensive = [np.mean(too_expensive <= val) for val in x]

    # Van Westendorp curves
    too_cheap_curve = 1 - np.array(cdf_too_cheap)        # Too Cheap (inverted)
    cheap_curve = np.array(cdf_cheap)                    # Cheap
    expensive_curve = 1 - np.array(cdf_expensive)        # Expensive (inverted)
    too_expensive_curve = np.array(cdf_too_expensive)    # Too Expensive

    # Plot
    plt.figure(figsize=(8,6))
    plt.plot(x, too_cheap_curve, label='Too Cheap', color='green')
    plt.plot(x, cheap_curve, label='Cheap', color='blue')
    plt.plot(x, expensive_curve, label='Expensive', color='orange')
    plt.plot(x, too_expensive_curve, label='Too Expensive', color='red')
    # plt.scatter(x, too_cheap_curve, label='Too Cheap', color='green')
    # plt.scatter(x, cheap_curve, label='Cheap', color='blue')
    # plt.scatter(x, expensive_curve, label='Expensive', color='orange')
    # plt.scatter(x, too_expensive_curve, label='Too Expensive', color='red')

    # Intersections (IPP, OPP, PMC, PME)
    def find_intersection(y1, y2, x):
        idx = np.argmin(np.abs(np.array(y1) - np.array(y2)))
        return x[idx]

    def find_intersection_coord(y1, y2, x):
        idx = np.argmin(np.abs(np.array(y1) - np.array(y2)))
        return x[idx], y1[idx]

    PMC = find_intersection(too_cheap_curve, cheap_curve, x)
    PME = find_intersection(expensive_curve, too_expensive_curve, x)

    PMC_x, PMC_y = find_intersection_coord(too_cheap_curve, cheap_curve, x)
    PME_x, PME_y = find_intersection_coord(expensive_curve, too_expensive_curve, x)
    IPP_x, IPP_y = find_intersection_coord(cheap_curve, expensive_curve, x)
    OPP_x, OPP_y = find_intersection_coord(too_cheap_curve, too_expensive_curve, x)

    # plt.axvline(IPP, color='purple', linestyle='--', label=f'Indifference Price ≈ {IPP:.2f}')
    # plt.axvline(OPP, color='brown', linestyle='--', label=f'Optimal Price ≈ {OPP:.2f}')
    plt.scatter(IPP_x, IPP_y, color='orange', s=100, zorder=5, label=f'IPP = {IPP_x:.0f}')
    plt.scatter(OPP_x, OPP_y, color='green', s=100, zorder=5, label=f'OPP = {OPP_x:.0f}')

    plt.scatter(PMC_x, PMC_y, color='blue', s=100, zorder=5, label=f'PMC = {PMC_x:.0f}')
    plt.scatter(PME_x, PME_y, color='red', s=100, zorder=5, label=f'PME = {PME_x:.0f}')
    plt.axvspan(PMC, PME, alpha=0.1, color="purple", label="Acceptable Price Range")

    plt.title(f'Van Westendorp - {product_name}')
    plt.xlabel('Price')
    plt.ylabel('% of respondents')
    plt.legend()
    plt.grid(True)
    # plt.show() # uncomment this if you want to see the graph before saving

    #Save graphic to path specified
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

# 3. Loop through all products
num_products = df.shape[1] // 4  # Each product has 4 columns



for i in range(num_products):
    df_product = df.iloc[:, i*4:(i+1)*4]
    output_path = os.path.join(os.getenv("USERPROFILE" if os.name == "nt" else "HOME"), "Downloads", f"Product {i+1}")
    van_westendorp_plot(df_product, product_name=f'Product {i+1}', save_path=output_path)
