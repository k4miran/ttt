import requests
import talib
import numpy as np
import time

def get_doge_usdt_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT"
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def generate_rsi_signal(prices):
    rsi = talib.RSI(np.array(prices), timeperiod=14)
    
    if rsi[-1] < 30:
        return "Buy Signal"
    elif rsi[-1] > 70:
        return "Sell Signal"
    else:
        return "No Signal"

def main():
    prices = []

    # Fiyat verilerini topluyoruz
    for _ in range(14):
        price = get_doge_usdt_price()
        prices.append(price)
        print(f"Toplanan Fiyat: {price}")
        time.sleep(1)  # Binance API'sini aşırı yüklememek için kısa bir gecikme

    # RSI sinyalini oluşturuyoruz
    signal = generate_rsi_signal(prices)
    print(f"Sinyal: {signal}")

    # Sinyali sürekli olarak izlemek için bir döngü oluşturuyoruz
    while True:
        new_price = get_doge_usdt_price()
        prices.append(new_price)
        prices.pop(0)  # İlk fiyatı çıkarıyoruz, sadece son 14 fiyatı saklıyoruz
        
        signal = generate_rsi_signal(prices)
        print(f"Güncel Fiyat: {new_price} | Sinyal: {signal}")

        time.sleep(300)  # Her 5 dakikada bir sinyal kontrol ediliyor

if __name__ == "__main__":
    main()
