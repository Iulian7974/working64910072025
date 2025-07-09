import streamlit as st
import pandas as pd
import random
from sklearn.preprocessing import MinMaxScaler

st.title("🎰 Predicție Loto 6/49 cu Machine Learning")

st.markdown("Această aplicație generează variante de joc pe baza datelor istorice din Loto 6/49 folosind scoruri combinate de **frecvență** și **latență** (ciclul de ~20 extrageri).")

uploaded_file = st.file_uploader("📁 Încarcă fișierul Excel cu extragerile (format .xlsx)", type=["xlsx"])

if not uploaded_file:
    st.warning("🔺 Aștept un fișier Excel cu extragerile pentru a continua.")
    st.stop()

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Fișierul a fost încărcat cu succes!")

    # Extrageri convertite în seturi
    draws = df[['Nr.1', 'Nr.2', 'Nr.3', 'Nr.4', 'Nr.5', 'Nr.6']].values.tolist()
    draws = [set(row) for row in draws]

    # Latență: câte extrageri au trecut de la ultima apariție
    latențe = {n: None for n in range(1, 50)}
    for i in range(len(draws) - 1, -1, -1):
        for n in range(1, 50):
            if latențe[n] is None and n in draws[i]:
                latențe[n] = len(draws) - i - 1

    # Frecvență
    all_numbers = df[['Nr.1', 'Nr.2', 'Nr.3', 'Nr.4', 'Nr.5', 'Nr.6']].values.flatten()
    frequency = pd.Series(all_numbers).value_counts().sort_index()

    # Scor combinat
    combined_df = pd.DataFrame({
        'Număr': range(1, 50),
        'Frecvență': frequency.values,
        'Latență': [latențe[n] for n in range(1, 50)]
    })

    scaler = MinMaxScaler()
    combined_df[['Frecvență_norm', 'Latență_norm']] = scaler.fit_transform(combined_df[['Frecvență', 'Latență']])
    combined_df['Scor'] = 0.6 * combined_df['Frecvență_norm'] + 0.4 * combined_df['Latență_norm']
    combined_df.sort_values(by='Scor', ascending=False, inplace=True)

    # Selectare top 10 numere
    top_10 = combined_df.head(10)['Număr'].tolist()

    # Generare variante
    random.seed(42)
    variante_6 = [sorted(random.sample(top_10, 6)) for _ in range(5)]
    varianta_10 = sorted(top_10)

    # Afișare rezultate
    st.subheader("🔢 Top 10 numere cele mai probabile")
    st.write(varianta_10)

    st.subheader("🎯 5 variante posibile de 6 numere")
    for i, v in enumerate(variante_6, 1):
        st.write(f"**{i}.** {v}")

    st.subheader("📊 Scoruri complete (toate numerele)")
    st.dataframe(combined_df.sort_values(by="Număr"))

else:
    st.info("Te rog încarcă un fișier Excel cu extragerile Loto.")
