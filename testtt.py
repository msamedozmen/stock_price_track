import yfinance as yf
import matplotlib.pyplot as plt

# Fetch Apple stock data for the last 3 days with 1-minute interval
apple_data = yf.download("AAPL", period="3d", interval="1m")

# Plot the stock data
plt.figure(figsize=(10, 6))
plt.plot(apple_data.index, apple_data['Close'], label='Close Price', color='blue')
plt.xlabel('Date')
plt.ylabel('Close Price (USD)')
plt.title('Apple Stock Price for the Last 3 Days')

# Convert datetime index to string format and use it as labels
date_labels = [str(date) for date in apple_data.index]
plt.xticks(apple_data.index, date_labels, rotation=45)

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
