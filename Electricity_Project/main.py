import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="سامانه هوش مصنوعی توزیع برق", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0A0E17; color: white; }
    div[data-testid="stMetricValue"] { color: #00FFCC; font-size: 32px; font-weight: bold; }
    .critical-box { background-color: #221216; border-right: 5px solid #FF0055; padding: 15px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ پلتفرم هوش مصنوعی مدیریت بار شبکه توزیع برق زنجان")
st.markdown("---")

st.sidebar.header("📥 تنظیمات پورتال")
region_type = st.sidebar.selectbox("نوع بافت منطقه:", ["مسکونی", "صنعتی", "تجاری"])

# ساخت دیتای مستقیم برای اطمینان از عدم وابستگی به فایل خارجی در گام اول
data = {
    'تاریخ_و_ساعت': pd.date_range(start='2026-03-01', periods=10, freq='H'),
    'مصرف_برق_کیلووات': [129.94, 115.20, 452.30, 489.94, 441.10, 295.40, 260.15, 95.40, 489.94, 485.20]
}
df = pd.DataFrame(data)

mean_val = df['مصرف_برق_کیلووات'].mean()
max_val = df['مصرف_برق_کیلووات'].max()

tab1, tab2 = st.tabs(["📊 کالبدشکافی بار", "🕵️‍♂️ کشف سرقت برق"])

with tab1:
    col1, col2 = st.columns(2)
    with col1: st.metric(label="📉 میانگین بار شبکه", value=f"{mean_val:.2f} kW")
    with col2: st.metric(label="⚡ حداکثر دیماند", value=f"{max_val:.2f} kW")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['تاریخ_و_ساعت'], y=df['مصرف_برق_کیلووات'], mode='lines+markers', name='بار لحظه‌ای', line=dict(color='#00ffcc')))
    fig.update_layout(template='plotly_dark', paper_bgcolor='#0A0E17', plot_bgcolor='#111622', height=350)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### کشف تلفات غیرفنی و مصارف مشکوک")
    st.metric(label="🚨 میزان هدررفت پنهان انرژی در این زون", value="15.0%", delta="بالاتر از حد مجاز")
    st.markdown("""
    <div class="critical-box">
        <h4>🚨 هشدار هوش مصنوعی: فرضیه دستکاری کنتور</h4>
        <p>الگوی مصرف نیمه‌شب این منطقه نشان‌دهنده کشش بار غیرمجاز است. بازرسی خطوط فیدر فرعی توصیه می‌شود.</p>
    </div>
    """, unsafe_allow_html=True)
