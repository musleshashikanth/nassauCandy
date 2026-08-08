# Research Paper: Factory-to-Customer Shipping Route Efficiency Analysis

## 1. Abstract
This paper details an Exploratory Data Analysis (EDA) of the logistics operations for Nassau Candy Distributor. By evaluating shipping lead times, geographic bottlenecks, and route efficiencies, we identified actionable insights to optimize the supply chain, reduce delays, and improve customer satisfaction.

## 2. Methodology
The analysis utilized a dataset of 5,000 shipments containing records of order dates, ship dates, origins (factories), destinations (states), and shipping methods.
- **Data Cleaning**: Dates were parsed and validated. Lead times were calculated as `Ship Date - Order Date`.
- **Feature Engineering**: Routes were defined as `Factory -> Customer State`.
- **Benchmarking**: Routes were ranked based on average shipping lead time.

## 3. Findings
### 3.1 Overall Performance
The overall average lead time across the network varies significantly by shipping mode:
- **Standard Shipping**: Averages ~4.5 days.
- **Expedited Shipping**: Averages ~1.8 days.

### 3.2 Geographic Bottlenecks
Significant congestion was observed in specific states:
- **New York and California**: These states consistently exhibit higher average lead times, regardless of the factory origin. This indicates localized final-mile delivery congestion or warehouse processing bottlenecks for coastal deliveries.
- **Sugar Shack to the South**: The route originating from the "Sugar Shack" factory to Southern states showed anomalous delays (average lead time > 6 days for standard shipping).

### 3.3 Route Efficiency Score
- **Most Efficient Routes**: Shorter intra-regional routes (e.g., Wicked Choccy's to GA/FL) perform well.
- **Least Efficient Routes**: Cross-country routes and routes hitting the CA/NY bottlenecks rank at the bottom.

## 4. Recommendations
1. **Reroute High-Volume Congested Paths**: Consider utilizing alternative carriers or adjusting warehouse dispatch priorities for shipments bound for California and New York.
2. **Investigate Sugar Shack Operations**: The specific delay from Sugar Shack to the Southern region warrants a deep dive into that facility's outbound logistics processes.
3. **Dynamic Shipping Mode Allocation**: Subsidize expedited shipping for historically slow routes to maintain a consistent customer experience nationwide.
