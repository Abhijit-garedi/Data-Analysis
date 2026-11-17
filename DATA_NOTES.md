# Data notes

## campaign_transactions.csv
Extracted from the supplied two-page PDF. Each row is one campaign order record.
- `order_id`: source campaign order ID
- `date`: transaction date in ISO format
- `product`: product name
- `category`: source category
- `purchases`: purchase quantity in that record

## reported_product_revenue.csv and reported_dashboard_kpis.json
Manually transcribed from the supplied dashboard screenshots. These are reported summary values, not values calculated from the transaction PDF.

## Validation
- Transaction rows: 35
- Total purchases: 200
- Free Fire Diamonds: 168
- PUBG UC: 31
- Mobile Legends: 1
