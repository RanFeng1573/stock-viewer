import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.title("📈 台股開盤 / 收盤資料下載器（多支股票）")

# 輸入多支股票代碼
stock_codes = st.text_area("輸入股票代碼（多支請以逗號分隔，例如：1101.TW, 2330.TW）", "1101.TW, 2330.TW")

# 日期區間選擇
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("起始日期", datetime.date.today() - datetime.timedelta(days=365 * 10))
with col2:
    end_date = st.date_input("結束日期", datetime.date.today())

# 只保留 CSV 匯出
if st.button("下載資料（開盤 / 收盤）"):
    if start_date >= end_date:
        st.error("❌ 起始日期需早於結束日期！")
    else:
        stock_codes_list = stock_codes.split(",")
        all_data = {}

        for stock_code in stock_codes_list:
            stock_code = stock_code.strip()
            try:
                stock = yf.Ticker(stock_code)
                data = stock.history(start=start_date, end=end_date)

                if data.empty:
                    st.warning(f"找不到 {stock_code} 的資料，請確認股票代碼是否正確。")
                else:
                    selected = data[["Open", "Close"]]
                    all_data[stock_code] = selected

            except Exception as e:
                st.warning(f"處理 {stock_code} 時發生錯誤：{e}")

        if all_data:
            # 合併資料
            combined_data = pd.concat(all_data, axis=1)
            st.success(f"✅ 成功抓取資料，包含 {len(combined_data)} 筆資料")
            st.dataframe(combined_data.tail())

            # 匯出 CSV
            csv = combined_data.to_csv().encode("utf-8-sig")
            st.download_button(
                label="📥 下載 CSV 檔案",
                data=csv,
                file_name=f"Stock_Data_{start_date}_{end_date}.csv",
                mime="text/csv"
            )
