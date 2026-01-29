import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

def clean_price(price_str):
    """
    Converts '₹ 15,000 / Piece' to float 15000.0
    Returns None if 'Ask for Price'
    """
    if pd.isna(price_str) or "Ask" in str(price_str):
        return None
    
    # Remove currency symbols and text (keep digits and dots)
    clean_str = re.sub(r'[^\d.]', '', str(price_str))
    try:
        return float(clean_str)
    except ValueError:
        return None

def perform_eda(file_path="data/raw_data.csv"):
    print("📊 Starting EDA...")
    
    # 1. Load Data
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("File not found. Please run the scraper first.")
        return

    # 2. Data Cleaning
    df['Price_Clean'] = df['Price'].apply(clean_price)
    
    # Normalize location (remove "New Delhi", "Delhi" inconsistencies usually)
    df['Location'] = df['Location'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) else x)

    # 3. Summary Statistics
    print("\n--- Summary Statistics ---")
    print(f"Total Products Scraped: {len(df)}")
    print(f"Products with transparent pricing: {df['Price_Clean'].count()}")
    print(f"Unique Suppliers: {df['Supplier'].nunique()}")
    print(f"Top 5 Locations:\n{df['Location'].value_counts().head(5)}")

    # 4. Visualizations
    sns.set_theme(style="whitegrid")
    
    # Plot A: Supplier Distribution by City
    plt.figure(figsize=(10, 6))
    top_cities = df['Location'].value_counts().head(10).index
    sns.countplot(y='Location', data=df[df['Location'].isin(top_cities)], order=top_cities, palette='viridis')
    plt.title('Top 10 Supplier Hubs')
    plt.xlabel('Number of Suppliers')
    plt.tight_layout()
    plt.savefig('data/location_distribution.png')
    print("\n✅ Saved chart: data/location_distribution.png")

    # Plot B: Price Distribution (for items with prices)
    plt.figure(figsize=(10, 6))
    price_data = df.dropna(subset=['Price_Clean'])
    # Filtering outliers for visualization (e.g., removing top 5%)
    q_high = price_data['Price_Clean'].quantile(0.95)
    filtered_price = price_data[price_data['Price_Clean'] < q_high]
    
    sns.histplot(filtered_price['Price_Clean'], bins=30, kde=True, color='blue')
    plt.title('Price Distribution (Excluding top 5% outliers)')
    plt.xlabel('Price (INR)')
    plt.tight_layout()
    plt.savefig('data/price_distribution.png')
    print("✅ Saved chart: data/price_distribution.png")

    # 5. Insights
    print("\n--- Key Insights ---")
    if not df.empty:
        most_common_loc = df['Location'].mode()[0]
        avg_price = df['Price_Clean'].mean()
        print(f"1. The major hub for this category is **{most_common_loc}**.")
        print(f"2. The average market price (observable) is approx **₹{avg_price:,.2f}**.")
        print("3. 'Ask for Price' is common, indicating a highly negotiable B2B market structure.")

if __name__ == "__main__":
    perform_eda()