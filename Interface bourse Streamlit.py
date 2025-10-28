import streamlit as st
import yfinance as yf

# Dictionnaires de tickers et descriptions
tickers = {
    "Tech": ["TSLA", "SOFI.PA", "MSFT", "NVDA", "ARM"],
    "Défense": ["HO.PA", "TXT", "A1E", "ALO.PA", "ORA.PA", "SU", "EDF.PA"],
    "Énergies": ["ALHRS.PA", "TTE", "ALB.PA"]
}

descriptions = {
    "Tech": "Tech – Technologies avancées, semi-conducteurs, intelligence artificielle...",
    "Défense": "Défense – Matériel militaire, cybersécurité, télécoms, infrastructures critiques...",
    "Énergies": "Énergies – Hydrogène, nucléaire, renouvelables, pétrole..."
}

# Interface Streamlit
st.title("📊 Interface bourse – version Streamlit")

# Sélection du secteur
secteur = st.selectbox("Choisis un secteur :", list(tickers.keys()))
st.write(f"**Description du secteur** : {descriptions.get(secteur)}")

# Sélection du ticker
ticker = st.selectbox("Choisis un ticker :", tickers[secteur])

# Affichage des infos
if st.button("Afficher les infos"):
    try:
        action = yf.Ticker(ticker)
        data = action.history(period="1d")
        open_price = data["Open"].iloc[-1]
        close_price = data["Close"].iloc[-1]
        variation_pct = ((close_price - open_price) / open_price) * 100
        dividende = action.info.get("dividendRate", None)

        st.metric(label="Cours actuel", value=f"{close_price:.2f} €", delta=f"{variation_pct:.2f} %")
        st.write(f"**Dividende annuel** : {dividende:.2f} €" if dividende else "Pas de dividende")
    except Exception as e:
        st.error(f"Erreur : {str(e)}")