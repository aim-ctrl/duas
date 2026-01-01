import streamlit as st
import pandas as pd

# 1. Konfigurera sidan
st.set_page_config(
    page_title="Min Dua Samling",
    page_icon="🤲",
    layout="centered"
)

# 2. Funktion för att ladda data
# Vi använder cachen så att appen inte behöver ladda om filen varje gång man klickar
# @st.cache_data
def load_data():
    try:
        # Om du kör lokalt: "data.csv"
        # Vi lägger till encoding='utf-8' för arabiska tecken och skipinitialspace=True för formateringen
        df = pd.read_csv("data.csv", encoding='utf-8', skipinitialspace=True)
        return df
    except FileNotFoundError:
        st.error("Kunde inte hitta filen 'data.csv'. Se till att den ligger i samma mapp.")
        return pd.DataFrame()

df = load_data()

# 3. Lägg till CSS för styling (Kort och Arabisk Font)
st.markdown("""
<style>
    /* Importera arabiskt typsnitt (Amiri) */
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

    /* Design för själva kortet */
    .dua-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #333333; /* Mörk text för läsbarhet */
    }
    
    /* Mörkare bakgrund om användaren har dark mode (frivilligt) */
    @media (prefers-color-scheme: dark) {
        .dua-card {
            background-color: #262730;
            border: 1px solid #41424C;
            color: #ffffff;
        }
    }

    /* Titel stil */
    .dua-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
        color: #4CAF50; /* En grön nyans */
    }

    /* Arabisk text stil */
    .dua-arabic {
        font-family: 'Amiri', serif;
        font-size: 2rem;
        direction: rtl; /* Höger till vänster */
        text-align: right;
        margin: 15px 0;
        line-height: 1.6;
    }

    /* Beskrivning stil */
    .dua-desc {
        font-style: italic;
        margin-bottom: 15px;
        font-size: 1rem;
    }

    /* Meta-taggar (Källa och Kategori) */
    .meta-tags {
        display: flex;
        gap: 10px;
        font-size: 0.8rem;
    }
    
    .tag {
        background-color: #f0f2f6;
        padding: 5px 10px;
        border-radius: 15px;
        color: #555;
    }
    
    /* Dark mode justering för taggar */
    @media (prefers-color-scheme: dark) {
        .tag {
            background-color: #41424C;
            color: #eee;
        }
    }

</style>
""", unsafe_allow_html=True)

# 4. Huvudrubrik
st.title("🤲 Dua & Dhikr Samling")

# 5. Filtrering (Valfritt men användbart)
if not df.empty:
    kategorier = ["Alla"] + list(df['kategori'].unique())
    vald_kategori = st.selectbox("Filtrera på kategori:", kategorier)

    # Filtrera data baserat på val
    if vald_kategori != "Alla":
        df_visning = df[df['kategori'] == vald_kategori]
    else:
        df_visning = df

    # 6. Loopa igenom data och skapa korten
    for index, row in df_visning.iterrows():
        # Vi skapar HTML-strukturen för varje kort
        html_card = f"""
        <div class="dua-card">
            <div class="dua-title">{row['titel']}</div>
            <div class="dua-arabic">{row['arabisk_text']}</div>
            <div class="dua-desc">{row['beskrivning']}</div>
            <div class="meta-tags">
                <span class="tag">📂 {row['kategori']}</span>
                <span class="tag">📖 {row['kalla']}</span>
            </div>
        </div>
        """
        st.markdown(html_card, unsafe_allow_html=True)

else:
    st.info("Ingen data hittades. Lägg till rader i data.csv.")
