import requests
import json
import sqlite3
import pandas as pd
import numpy as np

def pull_vietnam_housing_demo():
    print("================================================================================")
    print("      DEMO: PULLING LIVE VIETNAM REAL ESTATE DATA (CHỢ TỐT NHÀ TP.HCM)          ")
    print("================================================================================\n")

    # 1. KÉO DỮ LIỆU LIVE TỪ CHỢ TỐT (TP.HCM: region_v2=13000, BĐS: cg=1000)
    print(">>> 1. Đang kết nối Chợ Tốt Gateway API kéo 20 tin Bất động sản mới nhất tại TP.HCM...")
    url = "https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&cg=1000&limit=20"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()
        ads = data.get('ads', [])
        print(f" [+] Kéo thành công {len(ads)} tin đăng thực tế từ Chợ Tốt!")
    except Exception as e:
        print(f" [!] Lỗi kéo dữ liệu: {e}")
        return

    # 2. XỬ LÝ & ĐƯA VÀO PANDAS DATAFRAME
    housing_list = []
    for ad in ads:
        price = ad.get('price', 0)
        size = ad.get('size', 0)
        if price and size and size > 0:
            price_per_m2 = round(price / size, 2)
        else:
            price_per_m2 = 0
            
        housing_list.append({
            'ad_id': ad.get('list_id'),
            'title': ad.get('subject', ''),
            'price': price,
            'price_string': ad.get('price_string', ''),
            'size_m2': size,
            'price_per_m2': price_per_m2,
            'district': ad.get('area_name', 'Chưa rõ'),
            'ward': ad.get('ward_name', 'Chưa rõ'),
            'street': ad.get('street_name', ''),
            'lat': ad.get('latitude', 0.0),
            'lon': ad.get('longitude', 0.0),
            'phone': ad.get('phone', 'Hidden'),
            'body_sample': ad.get('body', '')[:120].replace('\n', ' ') + '...'
        })
        
    df_housing = pd.DataFrame(housing_list)
    print(f" [+] Đã đưa vào Pandas DataFrame ({df_housing.shape[0]} dòng, {df_housing.shape[1]} cột).")
    print("\nMẫu 3 tin đăng tiêu biểu:")
    print(df_housing[['title', 'price_string', 'size_m2', 'district', 'ward']].head(3))
    print()

    # 3. LƯU TRỮ VÀO CSDL SQLITE
    print(">>> 2. [CHƯƠNG 5: SQL] Lưu trữ vào CSDL SQLite 'vietnam_housing.db'...")
    conn = sqlite3.connect('vietnam_housing.db')
    df_housing.to_sql('Properties', conn, if_exists='replace', index=False)

    # Truy vấn SQL GROUP BY & AVG đơn giá theo Quận
    query = """
    SELECT district, 
           COUNT(*) as total_listings, 
           ROUND(AVG(price), 0) as avg_price_vnd, 
           ROUND(AVG(size_m2), 1) as avg_size_m2, 
           ROUND(AVG(price_per_m2), 0) as avg_price_per_m2
    FROM Properties
    GROUP BY district
    ORDER BY total_listings DESC
    """
    df_sql = pd.read_sql_query(query, conn)
    print(" [SQL Query Output]: Thống kê giá theo Quận:")
    print(df_sql)
    print()

    # 4. TÍNH KHOẢNG CÁCH TỚI TRUNG TÂM QUẬN 1 (CHỢ BẾN THÀNH) BẰNG HAVERSINE
    print(">>> 3. [CHƯƠNG 1: TOÁN CƠ SỞ] Tính khoảng cách địa lý đến Chợ Bến Thành (10.7725, 106.6980)...")
    BEN_THANH_LAT, BEN_THANH_LON = 10.7725, 106.6980
    
    def haversine_km(lat1, lon1, lat2, lon2):
        if lat1 == 0 or lon1 == 0:
            return np.nan
        R = 6371.0 # Bán kính Trái Đất (km)
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = np.sin(dlat / 2.0)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2.0)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        return round(R * c, 2)
        
    df_housing['dist_to_center_km'] = df_housing.apply(
        lambda row: haversine_km(row['lat'], row['lon'], BEN_THANH_LAT, BEN_THANH_LON), axis=1
    )
    print(df_housing[['district', 'street', 'size_m2', 'price_string', 'dist_to_center_km']].dropna().head(5))

    print("\n================================================================================")
    print("   THỬ NGHIỆM KÉO DỮ LIỆU BĐS VIỆT NAM THÀNH CÔNG: SẠCH ĐẸP, ĐẦY ĐỦ TOẠ ĐỘ & GIÁ!   ")
    print("================================================================================")

if __name__ == "__main__":
    pull_vietnam_housing_demo()
