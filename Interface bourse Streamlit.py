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

#Barre lattérale
st.sidebar.title("Options")
secteur = st.sidebar.selectbox("Secteur :", list(tickers.keys()))
ticker = st.sidebar.selectbox("Ticker :", tickers[secteur])
affichage = st.sidebar.radio("Affichage :", ["Infos", "Graphique 1 mois", "Graphique 2 ans", "Tableau 2 ans"])

# Interface Streamlit
st.title("Interface bourse")
st.write(f"**Secteur sélectionné** : {secteur}")
st.write(f"**Description du secteur** : {descriptions.get(secteur)}")
st.write(f"**Cours sélectionné** : {ticker}")
st.write(f"**Description du cours** : {descriptions_tick.get(ticker)}")

action=yf.Ticker(ticker)

# Affichage selon l’option choisie
if affichage == "Infos":
    try:
        data = action.history(period="1d")
        open_price = data["Open"].iloc[-1]
        close_price = data["Close"].iloc[-1]
        variation_pct = ((close_price - open_price) / open_price) * 100
        dividende = action.info.get("dividendRate", None)

        st.metric("Cours actuel", f"{close_price:.2f} €", f"{variation_pct:.2f} %")
        st.write(f"**Dividende annuel** : {dividende:.2f} €" if dividende else "Pas de dividende")
    except Exception as e:
        st.error(f"Erreur : {str(e)}")

elif affichage == "Graphique 1 mois":
    historique = action.history(period="1mo")
    if not historique.empty:
        fig, ax = plt.subplots()
        ax.plot(historique.index, historique["Close"], color="blue")
        ax.set_title(f"{ticker} – 1 mois")
        ax.set_xlabel("Date")
        ax.set_ylabel("Cours (€)")
        ax.grid(True)
        st.pyplot(fig)

elif affichage == "Graphique 2 ans":
    historique = action.history(period="2y")
    if not historique.empty:
        historique["Moyenne mobile 50j"] = historique["Close"].rolling(window=50).mean()
        fig, ax = plt.subplots()
        ax.plot(historique.index, historique["Close"], label="Cours", color="green")
        ax.plot(historique.index, historique["Moyenne mobile 50j"], label="MM 50j", color="orange")
        ax.set_title(f"{ticker} – 2 ans")
        ax.set_xlabel("Date")
        ax.set_ylabel("Cours (€)")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

elif affichage == "Tableau 2 ans":
    historique = action.history(period="2y")
    st.dataframe(historique[["Close"]].rename(columns={"Close": "Cours de clôture"}))
    st.download_button(
        label="📥 Télécharger les données (CSV)",
        data=historique.to_csv().encode("utf-8"),
        file_name=f"{ticker}_2ans.csv",
        mime="text/csv"
    )

