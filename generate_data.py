import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# Factories & Products
factories = {
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036},
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371},
    "Sugar Shack": {"lat": 48.11914, "lon": -96.18115},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487},
    "The Other Factory": {"lat": 35.1175, "lon": -89.971107}
}

products = [
    {"Division": "Chocolate", "Product Name": "Wonka Bar - Nutty Crunch Surprise", "Factory": "Lot's O' Nuts", "Base Cost": 1.5, "Base Price": 3.0},
    {"Division": "Chocolate", "Product Name": "Wonka Bar - Fudge Mallows", "Factory": "Lot's O' Nuts", "Base Cost": 1.6, "Base Price": 3.2},
    {"Division": "Chocolate", "Product Name": "Wonka Bar - Scrumdiddlyumptious", "Factory": "Lot's O' Nuts", "Base Cost": 2.0, "Base Price": 4.5},
    {"Division": "Chocolate", "Product Name": "Wonka Bar - Milk Chocolate", "Factory": "Wicked Choccy's", "Base Cost": 1.2, "Base Price": 2.5},
    {"Division": "Chocolate", "Product Name": "Wonka Bar - Triple Dazzle Caramel", "Factory": "Wicked Choccy's", "Base Cost": 1.8, "Base Price": 3.5},
    {"Division": "Sugar", "Product Name": "Laffy Taffy", "Factory": "Sugar Shack", "Base Cost": 0.5, "Base Price": 1.5},
    {"Division": "Sugar", "Product Name": "SweeTARTS", "Factory": "Sugar Shack", "Base Cost": 0.6, "Base Price": 1.8},
    {"Division": "Sugar", "Product Name": "Nerds", "Factory": "Sugar Shack", "Base Cost": 0.8, "Base Price": 2.0},
    {"Division": "Sugar", "Product Name": "Fun Dip", "Factory": "Sugar Shack", "Base Cost": 0.7, "Base Price": 1.9},
    {"Division": "Other", "Product Name": "Fizzy Lifting Drinks", "Factory": "Sugar Shack", "Base Cost": 1.5, "Base Price": 5.0},
    {"Division": "Sugar", "Product Name": "Everlasting Gobstopper", "Factory": "Secret Factory", "Base Cost": 1.0, "Base Price": 2.5},
    {"Division": "Other", "Product Name": "Lickable Wallpaper", "Factory": "Secret Factory", "Base Cost": 3.0, "Base Price": 10.0},
    {"Division": "Other", "Product Name": "Wonka Gum", "Factory": "Secret Factory", "Base Cost": 0.2, "Base Price": 1.0},
    {"Division": "Sugar", "Product Name": "Hair Toffee", "Factory": "The Other Factory", "Base Cost": 0.9, "Base Price": 2.2},
    {"Division": "Other", "Product Name": "Kazookles", "Factory": "The Other Factory", "Base Cost": 1.1, "Base Price": 2.8},
]

# Geographies
regions = {
    "West": ["CA", "WA", "OR", "NV", "AZ"],
    "Midwest": ["IL", "OH", "MI", "IN", "WI"],
    "South": ["TX", "FL", "GA", "NC", "VA"],
    "Northeast": ["NY", "PA", "MA", "NJ", "CT"]
}
states_cities = {
    "CA": ["Los Angeles", "San Francisco"], "WA": ["Seattle"], "OR": ["Portland"], "NV": ["Las Vegas"], "AZ": ["Phoenix"],
    "IL": ["Chicago"], "OH": ["Columbus"], "MI": ["Detroit"], "IN": ["Indianapolis"], "WI": ["Milwaukee"],
    "TX": ["Houston", "Dallas"], "FL": ["Miami", "Orlando"], "GA": ["Atlanta"], "NC": ["Charlotte"], "VA": ["Richmond"],
    "NY": ["New York"], "PA": ["Philadelphia"], "MA": ["Boston"], "NJ": ["Newark"], "CT": ["Hartford"]
}

ship_modes = ["Standard", "Expedited"]
num_records = 5000

data = []
start_date = datetime(2023, 1, 1)

for i in range(num_records):
    order_id = f"ORD-{10000 + i}"
    # Generate dates
    order_date = start_date + timedelta(days=random.randint(0, 365))
    
    # Pick product
    prod = random.choice(products)
    
    # Pick location
    region = random.choice(list(regions.keys()))
    state = random.choice(regions[region])
    city = random.choice(states_cities[state])
    postal_code = f"{random.randint(10000, 99999)}"
    
    ship_mode = random.choices(ship_modes, weights=[0.7, 0.3])[0]
    
    # Calculate Lead Time (simulated based on logic)
    # Give some regions bottlenecks
    base_lead = 3 if ship_mode == "Standard" else 1
    if state in ["CA", "NY"]:  # Congestion states
        base_lead += random.randint(1, 4)
    if prod["Factory"] == "Sugar Shack" and region == "South": # specific route bottleneck
        base_lead += random.randint(2, 5)
        
    lead_time = base_lead + random.randint(0, 3)
    ship_date = order_date + timedelta(days=lead_time)
    
    units = random.randint(10, 500)
    cost = round(prod["Base Cost"] * units, 2)
    sales = round(prod["Base Price"] * units * random.uniform(0.9, 1.1), 2)
    gross_profit = round(sales - cost, 2)
    
    data.append({
        "Row ID": i + 1,
        "Order ID": order_id,
        "Order Date": order_date.strftime("%Y-%m-%d"),
        "Ship Date": ship_date.strftime("%Y-%m-%d"),
        "Ship Mode": ship_mode,
        "Customer ID": f"CUST-{random.randint(100, 999)}",
        "Country/Region": "United States",
        "City": city,
        "State/Province": state,
        "Postal Code": postal_code,
        "Division": prod["Division"],
        "Region": region,
        "Product ID": f"PRD-{random.randint(10, 99)}",
        "Product Name": prod["Product Name"],
        "Factory": prod["Factory"],
        "Sales": sales,
        "Units": units,
        "Gross Profit": gross_profit,
        "Cost": cost
    })

df = pd.DataFrame(data)
df.to_csv("nassau_candy_sales.csv", index=False)
print("Dataset generated: nassau_candy_sales.csv")
