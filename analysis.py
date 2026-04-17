import pandas as pd

# Load data (CSV file in same folder)
df = pd.read_csv("nykaa_campaign_data.csv")

# Keep only required columns
df = df[["Impressions", "Clicks", "Leads", "Conversions", "Revenue"]]

# Handle missing values
df.fillna(0, inplace=True)

# Create funnel metrics
df["CTR"] = df["Clicks"] / df["Impressions"]
df["Lead_Rate"] = df["Leads"] / df["Clicks"]
df["Conversion_Rate"] = df["Conversions"] / df["Leads"]

# Replace infinity values (if division by 0 happens)
df.replace([float('inf'), -float('inf')], 0, inplace=True)

# Calculate total funnel values
funnel = df.sum()

# Print results
print("\n📊 Funnel Summary:\n")
print(funnel)

# Calculate overall rates
ctr = funnel["Clicks"] / funnel["Impressions"]
lead_rate = funnel["Leads"] / funnel["Clicks"]
conversion_rate = funnel["Conversions"] / funnel["Leads"]

print("\n📈 Overall Metrics:\n")
print(f"CTR: {ctr:.2f}")
print(f"Lead Rate: {lead_rate:.2f}")
print(f"Conversion Rate: {conversion_rate:.2f}")