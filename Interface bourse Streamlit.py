import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# Dictionnaires de tickers et descriptions
tickers = {
    "Tech": ["STM", "SOI.PA", "MSFT", "NVDA", "ARM"],
    "Défense": ["HO.PA", "NATO", "ALNSE.PA"],
    "Énergie": ["ALHRS.PA", "TTE", "ALO.PA", "ORA.PA", "SLB", "EDF"]
}

descriptions = {
    "Tech": "Tech – Technologies avancées, semi-conducteurs, intelligence artificielle...",
    "Défense": "Défense – Matériel militaire, cybersécurité, télécoms, infrastructures critiques...",
    "Énergie": "Énergies – Hydrogène, nucléaire, renouvelables, pétrole..."
}
descriptions_tick = {
    "STM": "STMicroelectronics - semi-conducteurs pour auto, IoT, industrie",
    "SOI.PA": "Soitec - matériaux avancés pour semi-conducteurs",
    "MSFT": "Microsoft - logiciels, cloud Azure, IA",
    "NVDA": "NVIDIA Corporation - entreprise tech américaine",
    "ARM": "Arm Holdings plc - conception de microprocesseurs (CPU, GPU, NPU)",
    "HO.PA": "Thales - défense, sécurité, électronique embarquée",
    "NATO": "Themes Transatlantic Defense ETF - fonds indiciel d'entreprises (défense et aérospatial)",
    "ALNSE.PA": "NSE Group - systèmes embarqués, électronique critique",
    "ALHRS.PA": "Hydrogen Refueling Solutions (HRS) - fabricant français de stations hydrogène",
    "TTE": "TotalEnergies - énergie, pétrole, transition verte",
    "ALO.PA": "Alstom S.A. - transport ferroviaire mondial",
    "ORA.PA": "Orange S.A. - opérateur télécom majeur en Europe",
    "SLB": "Schlumberger - services pétroliers mondiaux",
    "EDF": "EDF - électricité, nucléaire, renouvelables"
}

# Interface Streamlit
st.title("Interface bourse")

# Sélection du secteur
secteur = st.selectbox("Choisis un secteur :", list(tickers.keys()))
st.write(f"**Description du secteur** : {descriptions.get(secteur)}")

# Sélection du ticker
ticker = st.selectbox("Choisis un ticker :", tickers[secteur])
st.write(f"**Description du ticker** : {descriptions_tick.get(ticker)}")

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


#Récupération des données sur 1 mois
historique=action.history(period="1mo")

if not historique.empty:
    fig, ax = plt.subplots()
    ax.plot(historique.index, historique["Close"], marker="o", linestyle="-", color="blue")
    ax.set_title(f"Évolution du cours de {ticker} – 1 mois")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cours de clôture (€)")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("Pas de données disponibles pour ce ticker sur 1 mois.")

#Récupération des données
st.dataframe(historique[["Close"]])
st.download_button(
    label="📥 Télécharger les données (CSV)",
    data=historique.to_csv().encode("utf-8"),
    file_name=f"{ticker}_1mo.csv",
    mime="text/csv"
)


