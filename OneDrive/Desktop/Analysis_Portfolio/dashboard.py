import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Customer Shopping Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] { background-color: #111318; }
[data-testid="stSidebar"] { background-color: #1a1d27; border-right: 1px solid #2d3142; }
[data-testid="stSidebar"] * { color: #e0e0e0; }
.block-container { padding: 1rem 2rem; }
div[data-testid="metric-container"] {
    background: #1e2130;
    border: 1px solid #2d3142;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
div[data-testid="metric-container"] label { color: #8b8fa8 !important; font-size: 13px !important; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 28px !important; font-weight: 700 !important; }
div[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 13px !important; }
.chart-card {
    background: #1e2130;
    border: 1px solid #2d3142;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}
.stDataFrame { border-radius: 12px; overflow: hidden; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("customer_shopping_behavior.csv")

# Sidebar
st.sidebar.markdown("## 🛍️ Shopping Analytics")
st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")
gender = st.sidebar.multiselect("👫 Gender", df['Gender'].unique(), default=list(df['Gender'].unique()))
season = st.sidebar.multiselect("🌦️ Season", df['Season'].unique(), default=list(df['Season'].unique()))
category = st.sidebar.multiselect("📦 Category", df['Category'].unique(), default=list(df['Category'].unique()))
sub = st.sidebar.multiselect("⭐ Subscription", df['Subscription Status'].unique(), default=list(df['Subscription Status'].unique()))

filtered = df[
    df['Gender'].isin(gender) &
    df['Season'].isin(season) &
    df['Category'].isin(category) &
    df['Subscription Status'].isin(sub)
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing:** {len(filtered):,} of {len(df):,} records")
st.sidebar.markdown("---")
st.sidebar.markdown("© Ritesh Kumar Singh")

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #1e2130 0%, #2d3142 100%);
border-radius: 16px; padding: 24px 32px; margin-bottom: 24px;
border: 1px solid #3d4166; display: flex; justify-content: space-between; align-items: center;'>
<div>
<h1 style='color: #ffffff; margin: 0; font-size: 28px; font-weight: 700;'>
🛍️ Customer Shopping Behaviour
</h1>
<p style='color: #8b8fa8; margin: 4px 0 0 0; font-size: 14px;'>
Real-time Analytics Dashboard • © Ritesh Kumar Singh
</p>
</div>
<div style='text-align: right;'>
<span style='background: #00c853; color: white; padding: 6px 14px;
border-radius: 20px; font-size: 12px; font-weight: 600;'>● LIVE</span>
</div>
</div>
""", unsafe_allow_html=True)

# KPI Cards
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👥 Customers", f"{len(filtered):,}", f"+{len(filtered) - len(df)//2:,}")
c2.metric("💰 Total Revenue", f"${filtered['Purchase Amount (USD)'].sum():,.0f}", "+12.5%")
c3.metric("📊 Avg Purchase", f"${filtered['Purchase Amount (USD)'].mean():.2f}", "+3.2%")
c4.metric("⭐ Avg Rating", f"{filtered['Review Rating'].mean():.2f}/5", "+0.3")
c5.metric("🔄 Prev Purchases", f"{filtered['Previous Purchases'].mean():.1f}", "+5.1%")

st.markdown("<br>", unsafe_allow_html=True)

# Row 1 Charts
col1, col2, col3 = st.columns([2, 1.5, 1.5])

with col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### 📈 Revenue Trend by Season & Category")
    sea_cat = filtered.groupby(['Season', 'Category'])['Purchase Amount (USD)'].sum().reset_index()
    fig1 = px.bar(sea_cat, x='Season', y='Purchase Amount (USD)', color='Category',
        barmode='group',
        color_discrete_sequence=['#4361ee', '#7209b7', '#f72585', '#4cc9f0'],
        template='plotly_dark')
    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        font=dict(color='#8b8fa8')
    )
    fig1.update_xaxes(gridcolor='#2d3142', showgrid=True)
    fig1.update_yaxes(gridcolor='#2d3142', showgrid=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### 👫 Gender Split")
    gen = filtered['Gender'].value_counts().reset_index()
    fig2 = px.pie(gen, values='count', names='Gender',
        color_discrete_sequence=['#4361ee', '#f72585'],
        template='plotly_dark', hole=0.65)
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(l=0, r=0, t=10, b=0),
        showlegend=True, font=dict(color='#8b8fa8'),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    fig2.update_traces(textposition='outside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### 🔔 Subscription")
    sub_data = filtered['Subscription Status'].value_counts().reset_index()
    fig3 = px.pie(sub_data, values='count', names='Subscription Status',
        color_discrete_sequence=['#00c853', '#ff1744'],
        template='plotly_dark', hole=0.65)
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(l=0, r=0, t=10, b=0),
        showlegend=True, font=dict(color='#8b8fa8'),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    fig3.update_traces(textposition='outside', textinfo='percent+label')
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2
col4, col5 = st.columns([1.5, 2])

with col4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### 🏆 Top 10 Items by Revenue")
    top_items = filtered.groupby('Item Purchased')['Purchase Amount (USD)'].sum().nlargest(10).reset_index()
    fig4 = px.bar(top_items, x='Purchase Amount (USD)', y='Item Purchased',
        orientation='h',
        color='Purchase Amount (USD)',
        color_continuous_scale=['#1a1d27', '#4361ee', '#f72585'],
        template='plotly_dark')
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=350, margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_showscale=False, font=dict(color='#8b8fa8'),
        yaxis=dict(categoryorder='total ascending')
    )
    fig4.update_xaxes(gridcolor='#2d3142')
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### 💳 Payment Method vs Revenue")
    pay = filtered.groupby(['Payment Method', 'Category'])['Purchase Amount (USD)'].sum().reset_index()
    fig5 = px.bar(pay, x='Payment Method', y='Purchase Amount (USD)', color='Category',
        color_discrete_sequence=['#4361ee', '#7209b7', '#f72585', '#4cc9f0'],
        template='plotly_dark')
    fig5.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=350, margin=dict(l=0, r=0, t=10, b=0),
        font=dict(color='#8b8fa8'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    fig5.update_xaxes(gridcolor='#2d3142')
    fig5.update_yaxes(gridcolor='#2d3142')
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 3
col6, col7 = st.columns(2)

with col6:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### 📦 Category Revenue Share")
    cat_rev = filtered.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
    fig6 = px.bar(cat_rev, x='Category', y='Purchase Amount (USD)',
        color='Category',
        color_discrete_sequence=['#4361ee', '#7209b7', '#f72585', '#4cc9f0'],
        template='plotly_dark')
    fig6.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(l=0, r=0, t=10, b=0),
        font=dict(color='#8b8fa8'), showlegend=False
    )
    fig6.update_xaxes(gridcolor='#2d3142')
    fig6.update_yaxes(gridcolor='#2d3142')
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col7:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("#### 🚚 Shipping Type Distribution")
    ship = filtered['Shipping Type'].value_counts().reset_index()
    fig7 = px.bar(ship, x='Shipping Type', y='count',
        color='count',
        color_continuous_scale=['#1a1d27', '#4361ee'],
        template='plotly_dark')
    fig7.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(l=0, r=0, t=10, b=0),
        coloraxis_showscale=False, font=dict(color='#8b8fa8')
    )
    fig7.update_xaxes(gridcolor='#2d3142')
    fig7.update_yaxes(gridcolor='#2d3142')
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Raw Data
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown("#### 📋 Detailed Data View")
search = st.text_input("🔍 Search", placeholder="Search any value...")
if search:
    filtered = filtered[filtered.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
st.dataframe(filtered, use_container_width=True, height=300)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 20px; color: #4a4f6a; font-size: 13px; margin-top: 20px;
border-top: 1px solid #2d3142;'>
© 2026 Ritesh Kumar Singh | Customer Shopping Behaviour Analysis Dashboard |
Built with Python & Streamlit
</div>
""", unsafe_allow_html=True)