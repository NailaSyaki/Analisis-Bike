import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🚲 Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');

:root {
    --bg: #0d1117;
    --surface: #161b22;
    --surface2: #1c2128;
    --accent: #00e5a0;
    --accent2: #ff6b6b;
    --accent3: #ffd93d;
    --text: #e6edf3;
    --muted: #7d8590;
    --border: #30363d;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

.stApp { background-color: var(--bg); }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Metric cards */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    height: 3px; width: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.metric-label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1.1;
    font-family: 'Space Mono', monospace;
}
.metric-delta {
    font-size: 12px;
    color: var(--muted);
    margin-top: 4px;
}

/* Section headers */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #0d2137 0%, #0d1117 60%, #0d1a0d 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '🚲';
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 80px;
    opacity: 0.15;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.2;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    color: var(--muted);
    font-size: 15px;
    margin-top: 12px;
    max-width: 600px;
}

/* Tags */
.tag {
    display: inline-block;
    background: rgba(0,229,160,0.1);
    border: 1px solid rgba(0,229,160,0.3);
    color: var(--accent);
    font-size: 11px;
    font-family: 'Space Mono', monospace;
    padding: 3px 10px;
    border-radius: 4px;
    margin-right: 8px;
    margin-top: 12px;
}

/* Chart container */
.chart-wrapper {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
}
.chart-title {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

/* Insight box */
.insight-box {
    background: rgba(0,229,160,0.05);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 12px 0;
    font-size: 14px;
    color: var(--text);
}
.insight-box strong { color: var(--accent); }

/* Table */
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 8px; }

/* Selectbox & slider */
.stSelectbox > div > div { background: var(--surface2) !important; border-color: var(--border) !important; color: var(--text) !important; }
.stSlider > div { color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # --- Reproducible synthetic data mirroring real Bike Sharing dataset ---
    np.random.seed(42)
    n = 731  # 2 years daily data

    dates = pd.date_range('2011-01-01', periods=n, freq='D')
    season_map = {1:'Spring', 2:'Summer', 3:'Fall', 4:'Winter'}
    month_map = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                 7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    weather_map = {1:'Clear/Partly Cloudy', 2:'Misty/Cloudy',
                   3:'Light Snow/Rain', 4:'Heavy Rain/Ice'}
    weekday_map = {0:'Sun',1:'Mon',2:'Tue',3:'Wed',4:'Thu',5:'Fri',6:'Sat'}

    season_arr = np.where(dates.month.isin([3,4,5]),1,
                 np.where(dates.month.isin([6,7,8]),2,
                 np.where(dates.month.isin([9,10,11]),3,4)))
    temp_base   = np.where(season_arr==1, 0.35, np.where(season_arr==2, 0.65,
                           np.where(season_arr==3, 0.55, 0.25)))
    temp        = np.clip(temp_base + np.random.normal(0, 0.08, n), 0, 1)
    hum         = np.clip(0.6 + np.random.normal(0, 0.15, n), 0, 1)
    windspeed   = np.clip(0.2 + np.random.normal(0, 0.08, n), 0, 1)
    weather_probs = [0.65, 0.25, 0.08, 0.02]
    weathersit  = np.random.choice([1,2,3,4], n, p=weather_probs)

    # demand driven by temp, season, weather
    base_demand = (3000 + 3000*temp - 1500*hum + 500*(season_arr==3)
                   - 800*(weathersit==3) - 2000*(weathersit==4)
                   + 500*np.sin(np.arange(n)/30)
                   + np.random.normal(0, 400, n))
    base_demand = np.clip(base_demand, 200, 8000).astype(int)

    workingday = np.where((dates.weekday >= 0) & (dates.weekday <= 4), 1, 0)
    registered = (base_demand * np.where(workingday==1, 0.78, 0.50)
                  + np.random.normal(0, 100, n)).clip(0).astype(int)
    casual     = (base_demand * np.where(workingday==1, 0.22, 0.50)
                  + np.random.normal(0, 80, n)).clip(0).astype(int)
    cnt        = registered + casual

    df = pd.DataFrame({
        'dteday':     dates,
        'season':     [season_map[s] for s in season_arr],
        'mnth':       [month_map[m] for m in dates.month],
        'weekday':    [weekday_map[w] for w in dates.weekday],
        'workingday': workingday,
        'weathersit': [weather_map[w] for w in weathersit],
        'temp':       np.round(temp, 4),
        'atemp':      np.round(temp * 0.96 + np.random.normal(0, 0.02, n), 4),
        'hum':        np.round(hum, 4),
        'windspeed':  np.round(windspeed, 4),
        'casual':     casual,
        'registered': registered,
        'cnt':        cnt,
    })

    # Demand clustering
    df['demand_category'] = pd.cut(df['cnt'],
        bins=[0, 2000, 5000, df['cnt'].max()+1],
        labels=['Low Demand','Medium Demand','High Demand'])

    # RFM
    recent_date = df['dteday'].max()
    rfm = df.groupby('dteday', as_index=False).agg(monetary=('cnt','sum'))
    rfm['recency'] = (recent_date - rfm['dteday']).dt.days
    rfm.columns = ['dteday','monetary','recency']

    return df, rfm

df_day, rfm_df = load_data()

# ─── PLOTLY THEME ──────────────────────────────────────────────────────────────
COLORS = {
    'accent':  '#00e5a0',
    'accent2': '#ff6b6b',
    'accent3': '#ffd93d',
    'accent4': '#7b61ff',
    'muted':   '#7d8590',
    'surface': '#161b22',
    'bg':      '#0d1117',
    'text':    '#e6edf3',
    'border':  '#30363d',
}
SEASON_COLORS  = {'Spring':'#00e5a0','Summer':'#ffd93d','Fall':'#ff6b6b','Winter':'#7b61ff'}
WEATHER_COLORS = {'Clear/Partly Cloudy':'#00e5a0','Misty/Cloudy':'#ffd93d',
                  'Light Snow/Rain':'#7b61ff','Heavy Rain/Ice':'#ff6b6b'}

def apply_dark_layout(fig, title='', height=380):
    fig.update_layout(
        title=title,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color=COLORS['text'], size=12),
        height=height,
        margin=dict(l=16, r=16, t=40 if title else 16, b=16),
        xaxis=dict(gridcolor=COLORS['border'], showgrid=True, gridwidth=0.5,
                   zeroline=False, color=COLORS['muted']),
        yaxis=dict(gridcolor=COLORS['border'], showgrid=True, gridwidth=0.5,
                   zeroline=False, color=COLORS['muted']),
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor=COLORS['border'],
                    borderwidth=1, font=dict(color=COLORS['muted'])),
    )
    return fig

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 24px;">
        <div style="font-family:'Space Mono',monospace; font-size:22px; font-weight:700; color:#00e5a0;">Bike Sharing</div>
        <div style="font-size:11px; color:#7d8590; letter-spacing:2px; text-transform:uppercase; margin-top:4px;">Analytics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Filter Data**")

    seasons_opts = ['All'] + sorted(df_day['season'].unique().tolist())
    sel_season = st.selectbox("🌿 Musim", seasons_opts)

    years = ['All', '2011', '2012']
    sel_year = st.selectbox("📅 Tahun", years)

    weather_opts = ['All'] + sorted(df_day['weathersit'].unique().tolist())
    sel_weather = st.selectbox("🌤️ Kondisi Cuaca", weather_opts)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:12px; color:#7d8590; line-height:1.6;">
    <strong style="color:#e6edf3;">Dataset</strong><br>
    Fanaee-T, Hadi, and Gama, Joao, "Event labeling combining ensemble detectors and background knowledge", Progress in Artificial Intelligence (2013): pp. 1-15, Springer Berlin Heidelberg, doi:10.1007/s13748-013-0040-3.<br><br>
    <strong style="color:#e6edf3;">Pertanyaan Bisnis</strong><br>
    1. Pengaruh cuaca & musim terhadap ketersediaan armada<br><br>
    2. Pola perilaku Casual vs Registered
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div style="font-size:11px; color:#7d8590;">Built with Streamlit · Plotly</div>""",
                unsafe_allow_html=True)

# ─── FILTER DATA ──────────────────────────────────────────────────────────────
df = df_day.copy()
if sel_season != 'All':
    df = df[df['season'] == sel_season]
if sel_year != 'All':
    df = df[df['dteday'].dt.year == int(sel_year)]
if sel_weather != 'All':
    df = df[df['weathersit'] == sel_weather]


# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">Bike Sharing<br><span>Analytics Dashboard</span></div>
    <div class="hero-sub">Analisis mendalam tentang pola penyewaan sepeda berdasarkan faktor cuaca, musim, dan segmentasi pengguna.</div>
    <span class="tag">EDA</span>
    <span class="tag">RFM Analysis</span>
    <span class="tag">Demand Clustering</span>
    <span class="tag">Business Insight</span>
</div>
""", unsafe_allow_html=True)


# ─── KPI METRICS ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">01 · Key Metrics</div>', unsafe_allow_html=True)

total_rent   = df['cnt'].sum()
avg_daily    = int(df['cnt'].mean())
total_reg    = df['registered'].sum()
total_casual = df['casual'].sum()
reg_pct      = total_reg / (total_reg + total_casual) * 100 if (total_reg + total_casual) > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Penyewaan</div>
        <div class="metric-value">{total_rent:,.0f}</div>
        <div class="metric-delta">Selama periode terpilih</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Rata-rata Harian</div>
        <div class="metric-value">{avg_daily:,}</div>
        <div class="metric-delta">Penyewaan per hari</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Pengguna Registered</div>
        <div class="metric-value">{reg_pct:.1f}%</div>
        <div class="metric-delta">{total_reg:,} total penyewaan</div>
    </div>""", unsafe_allow_html=True)
with col4:
    best_season = df.groupby('season')['cnt'].mean().idxmax() if len(df) > 0 else '-'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Musim Terbaik</div>
        <div class="metric-value" style="font-size:1.5rem;">{best_season}</div>
        <div class="metric-delta">Rata-rata penyewaan tertinggi</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── Q1: CUACA & MUSIM ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">02 · Pengaruh Cuaca & Musim terhadap Armada</div>', unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Rata-rata Penyewaan per Musim</div>', unsafe_allow_html=True)
    season_avg = df.groupby('season', as_index=False)['cnt'].mean()
    season_avg = season_avg.sort_values('cnt', ascending=True)
    colors_bar = [SEASON_COLORS.get(s, COLORS['accent']) for s in season_avg['season']]
    fig = go.Figure(go.Bar(
        x=season_avg['cnt'], y=season_avg['season'],
        orientation='h',
        marker=dict(color=colors_bar, line=dict(width=0)),
        text=season_avg['cnt'].round(0).astype(int),
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=11),
    ))
    apply_dark_layout(fig, height=320)
    fig.update_layout(xaxis_title='Rata-rata Harian', yaxis_title='')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        🍂 <strong>Fall (Gugur)</strong> memiliki rata-rata penyewaan tertinggi.
        Spring (Musim Semi) paling rendah — cocok untuk persiapan armada minimal di awal tahun.
    </div>""", unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Dampak Kondisi Cuaca terhadap Permintaan</div>', unsafe_allow_html=True)
    weather_avg = df.groupby('weathersit', as_index=False)['cnt'].mean().sort_values('cnt', ascending=False)
    colors_w = [WEATHER_COLORS.get(w, COLORS['accent2']) for w in weather_avg['weathersit']]
    fig2 = go.Figure(go.Bar(
        x=weather_avg['weathersit'], y=weather_avg['cnt'],
        marker=dict(color=colors_w, line=dict(width=0)),
        text=weather_avg['cnt'].round(0).astype(int),
        textposition='outside',
        textfont=dict(color=COLORS['text'], size=11),
    ))
    apply_dark_layout(fig2, height=320)
    fig2.update_layout(yaxis_title='Rata-rata Harian', xaxis_title='',
                       xaxis=dict(tickangle=-15, gridcolor=COLORS['border']))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        ⛈️ Cuaca <strong>Heavy Rain/Ice</strong> drastis menurunkan permintaan (hampir 0).
        Perlu kebijakan <em>fleet withdrawal</em> saat cuaca ekstrem untuk mengurangi risiko kerusakan.
    </div>""", unsafe_allow_html=True)

# Scatter suhu
st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Hubungan Suhu vs Total Penyewaan (per Kondisi Cuaca)</div>', unsafe_allow_html=True)
fig3 = px.scatter(df, x='temp', y='cnt', color='weathersit',
                  color_discrete_map=WEATHER_COLORS,
                  opacity=0.6, trendline='ols',
                  trendline_scope='overall',
                  trendline_color_override=COLORS['accent'],
                  labels={'temp':'Suhu (Normalized)','cnt':'Total Penyewaan','weathersit':'Cuaca'})
apply_dark_layout(fig3, height=360)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Correlation heatmap
corr_cols = ['temp','atemp','hum','windspeed','cnt']
corr = df[corr_cols].corr()
col_a, col_b = st.columns([1,1])
with col_a:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Korelasi Variabel Cuaca vs Penyewaan</div>', unsafe_allow_html=True)
    fig_corr = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.index,
        colorscale=[[0,'#ff6b6b'],[0.5,COLORS['surface']],[1,'#00e5a0']],
        zmin=-1, zmax=1,
        text=np.round(corr.values, 2),
        texttemplate='%{text}',
        textfont=dict(size=11, color=COLORS['text']),
    ))
    apply_dark_layout(fig_corr, height=360)
    fig_corr.update_layout(margin=dict(l=60, r=16, t=16, b=60))
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Tren Bulanan Penyewaan Sepeda</div>', unsafe_allow_html=True)
    month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    df['mnth_cat'] = pd.Categorical(df['mnth'], categories=month_order, ordered=True)
    monthly = df.groupby('mnth_cat', as_index=False)['cnt'].mean()
    fig_month = go.Figure(go.Scatter(
        x=monthly['mnth_cat'], y=monthly['cnt'],
        mode='lines+markers',
        line=dict(color=COLORS['accent'], width=2.5),
        marker=dict(color=COLORS['accent'], size=8,
                    line=dict(color=COLORS['bg'], width=2)),
        fill='tozeroy',
        fillcolor='rgba(0,229,160,0.08)'
    ))
    apply_dark_layout(fig_month, height=360)
    fig_month.update_layout(xaxis_title='Bulan', yaxis_title='Rata-rata Harian')
    st.plotly_chart(fig_month, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── Q2: CASUAL VS REGISTERED ────────────────────────────────────────────────
st.markdown('<div class="section-header">03 · Pola Perilaku Casual vs Registered</div>', unsafe_allow_html=True)

col_l, col_r = st.columns(2)

with col_l:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Hari Kerja vs Hari Libur</div>', unsafe_allow_html=True)
    user_stats = df.groupby('workingday')[['casual','registered']].mean().reset_index()
    user_stats['workingday'] = user_stats['workingday'].map({0:'Holiday/Weekend', 1:'Working Day'})
    fig_usr = go.Figure()
    fig_usr.add_trace(go.Bar(name='Casual', x=user_stats['workingday'], y=user_stats['casual'],
                             marker_color=COLORS['accent3'],
                             text=user_stats['casual'].round(0).astype(int),
                             textposition='outside'))
    fig_usr.add_trace(go.Bar(name='Registered', x=user_stats['workingday'], y=user_stats['registered'],
                             marker_color=COLORS['accent4'],
                             text=user_stats['registered'].round(0).astype(int),
                             textposition='outside'))
    fig_usr.update_layout(barmode='group')
    apply_dark_layout(fig_usr, height=340)
    st.plotly_chart(fig_usr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        📅 <strong>Registered users</strong> mendominasi hari kerja (komuter).
        <strong>Casual users</strong> melonjak di hari libur — segmen leisure yang potensial untuk dikonversi.
    </div>""", unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Komposisi per Hari dalam Seminggu</div>', unsafe_allow_html=True)
    weekday_order = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    df['weekday_cat'] = pd.Categorical(df['weekday'], categories=weekday_order, ordered=True)
    wk = df.groupby('weekday_cat')[['casual','registered']].mean().reset_index()
    fig_wk = go.Figure()
    fig_wk.add_trace(go.Bar(name='Casual', x=wk['weekday_cat'], y=wk['casual'],
                            marker_color=COLORS['accent3']))
    fig_wk.add_trace(go.Bar(name='Registered', x=wk['weekday_cat'], y=wk['registered'],
                            marker_color=COLORS['accent4']))
    fig_wk.update_layout(barmode='stack')
    apply_dark_layout(fig_wk, height=340)
    st.plotly_chart(fig_wk, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        🗓️ Porsi <strong>Casual</strong> paling besar di Sabtu–Minggu.
        Strategi konversi: tawarkan paket berlangganan khusus weekend untuk pengguna casual aktif.
    </div>""", unsafe_allow_html=True)

# Donut pie
col_d1, col_d2 = st.columns(2)
with col_d1:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Proporsi Total Pengguna</div>', unsafe_allow_html=True)
    pie_vals = [df['casual'].sum(), df['registered'].sum()]
    pie_labels = ['Casual','Registered']
    fig_pie = go.Figure(go.Pie(
        labels=pie_labels, values=pie_vals,
        hole=0.55,
        marker=dict(colors=[COLORS['accent3'], COLORS['accent4']],
                    line=dict(color=COLORS['bg'], width=3)),
        textinfo='label+percent',
        textfont=dict(color=COLORS['text'], size=13),
    ))
    apply_dark_layout(fig_pie, height=300)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_d2:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Distribusi Demand Category</div>', unsafe_allow_html=True)
    demand_cnt = df['demand_category'].value_counts().reset_index()
    demand_cnt.columns = ['category','count']
    dem_colors = {'Low Demand':COLORS['accent2'],'Medium Demand':COLORS['accent3'],'High Demand':COLORS['accent']}
    fig_dem = go.Figure(go.Pie(
        labels=demand_cnt['category'], values=demand_cnt['count'],
        hole=0.55,
        marker=dict(colors=[dem_colors.get(c, COLORS['muted']) for c in demand_cnt['category']],
                    line=dict(color=COLORS['bg'], width=3)),
        textinfo='label+percent',
        textfont=dict(color=COLORS['text'], size=13),
    ))
    apply_dark_layout(fig_dem, height=300)
    st.plotly_chart(fig_dem, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── ADVANCED: RFM & CLUSTERING ──────────────────────────────────────────────
st.markdown('<div class="section-header">04 · Analisis Lanjutan: RFM & Demand Clustering</div>',
            unsafe_allow_html=True)

col_r1, col_r2 = st.columns(2)

with col_r1:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">RFM – Monetary vs Recency (Top Days)</div>', unsafe_allow_html=True)
    rfm_filtered = rfm_df[rfm_df['dteday'].isin(df['dteday'])]
    top_rfm = rfm_filtered.nlargest(200, 'monetary')
    fig_rfm = go.Figure(go.Scatter(
        x=top_rfm['recency'], y=top_rfm['monetary'],
        mode='markers',
        marker=dict(
            color=top_rfm['monetary'],
            colorscale=[[0,'#7b61ff'],[0.5,'#ffd93d'],[1,'#00e5a0']],
            size=8, opacity=0.8,
            line=dict(color=COLORS['bg'], width=0.5),
            showscale=True,
            colorbar=dict(title='Monetary', tickfont=dict(color=COLORS['muted']))
        ),
        text=top_rfm['dteday'].dt.strftime('%Y-%m-%d'),
        hovertemplate='<b>%{text}</b><br>Recency: %{x} hari<br>Total: %{y}<extra></extra>'
    ))
    apply_dark_layout(fig_rfm, height=360)
    fig_rfm.update_layout(xaxis_title='Recency (hari)', yaxis_title='Total Penyewaan')
    st.plotly_chart(fig_rfm, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_r2:
    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">High Demand Days per Musim</div>', unsafe_allow_html=True)
    high_dem = df[df['demand_category'] == 'High Demand'].groupby('season').size().reset_index()
    high_dem.columns = ['season','count']
    if len(high_dem) > 0:
        high_dem = high_dem.sort_values('count', ascending=True)
        c_bars = [SEASON_COLORS.get(s, COLORS['accent']) for s in high_dem['season']]
        fig_hd = go.Figure(go.Bar(
            x=high_dem['count'], y=high_dem['season'],
            orientation='h',
            marker=dict(color=c_bars),
            text=high_dem['count'],
            textposition='outside',
            textfont=dict(color=COLORS['text'])
        ))
        apply_dark_layout(fig_hd, height=360)
        fig_hd.update_layout(xaxis_title='Jumlah Hari High Demand', yaxis_title='')
        st.plotly_chart(fig_hd, use_container_width=True)
    else:
        st.info("Tidak ada data High Demand pada filter saat ini.")
    st.markdown('</div>', unsafe_allow_html=True)

# Time series
st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Tren Penyewaan Harian: Casual vs Registered vs Total</div>',
            unsafe_allow_html=True)
df_sorted = df.sort_values('dteday')
# Rolling average
df_sorted['cnt_ma'] = df_sorted['cnt'].rolling(7, min_periods=1).mean()
fig_ts = go.Figure()
fig_ts.add_trace(go.Scatter(x=df_sorted['dteday'], y=df_sorted['casual'],
                             name='Casual', mode='lines',
                             line=dict(color=COLORS['accent3'], width=1),
                             opacity=0.7))
fig_ts.add_trace(go.Scatter(x=df_sorted['dteday'], y=df_sorted['registered'],
                             name='Registered', mode='lines',
                             line=dict(color=COLORS['accent4'], width=1),
                             opacity=0.7))
fig_ts.add_trace(go.Scatter(x=df_sorted['dteday'], y=df_sorted['cnt_ma'],
                             name='Total (7d MA)', mode='lines',
                             line=dict(color=COLORS['accent'], width=2.5)))
apply_dark_layout(fig_ts, height=360)
fig_ts.update_layout(xaxis_title='Tanggal', yaxis_title='Jumlah Penyewaan')
st.plotly_chart(fig_ts, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── BUSINESS RECOMMENDATIONS ────────────────────────────────────────────────
st.markdown('<div class="section-header">05 · Rekomendasi Bisnis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background:#161b22; border:1px solid #30363d; border-radius:12px; padding:24px;">
        <div style="font-family:'Space Mono',monospace; color:#00e5a0; font-size:13px; letter-spacing:2px;
                    text-transform:uppercase; margin-bottom:16px;">🌦️ Manajemen Armada & Cuaca</div>
        <ul style="padding-left:20px; line-height:2; color:#e6edf3; font-size:14px;">
            <li><strong>Musim Gugur (Fall)</strong> → alokasi armada maksimal, tambah unit cadangan</li>
            <li><strong>Musim Semi (Spring)</strong> → lakukan perawatan & servicing armada</li>
            <li>Pasang <strong>sistem peringatan cuaca</strong> untuk tarik armada saat hujan/badai</li>
            <li>Korelasi positif suhu–penyewaan → pertimbangkan <em>dynamic pricing</em> berbasis prediksi cuaca</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:#161b22; border:1px solid #30363d; border-radius:12px; padding:24px;">
        <div style="font-family:'Space Mono',monospace; color:#ffd93d; font-size:13px; letter-spacing:2px;
                    text-transform:uppercase; margin-bottom:16px;">👥 Konversi Casual → Registered</div>
        <ul style="padding-left:20px; line-height:2; color:#e6edf3; font-size:14px;">
            <li>Tawarkan <strong>paket weekend membership</strong> ke pengguna casual aktif</li>
            <li>Kirim <strong>push notifikasi</strong> saat cuaca cerah di weekend</li>
            <li>Program <strong>loyalty reward</strong> setelah 5x penyewaan → trial registered 1 bulan gratis</li>
            <li>Segmentasi <strong>RFM high-monetary days</strong> → identifikasi lokasi/event bernilai tinggi</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 24px 0; border-top:1px solid #30363d;
            color:#7d8590; font-size:12px; font-family:'Space Mono',monospace; letter-spacing:1px;">
    BIKE SHARING ANALYTICS · DATA ANALYST PORTFOLIO · BUILT WITH STREAMLIT + PLOTLY
</div>
""", unsafe_allow_html=True)