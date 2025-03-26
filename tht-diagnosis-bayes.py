import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objs as go

# Page Configuration
st.set_page_config(
    page_title="Sistem Pakar Diagnosis Penyakit THT",
    layout="wide"
)

# Define Symptoms and Diseases
SYMPTOMS = [
    'Badan panas', 'Bersin', 'Telinga berdengung', 'Hidung buntu', 'Ingus darah',
    'Iritasi hidung', 'Tenggorokan kering', 'Leher kaku', 'Mata juling', 'Nyeri kepala',
    'Nyeri leher', 'Nyeri waktu menelan', 'Tenggorokan panas', 'Leher bengkak',
    'Penciuman terganggu', 'Pendengaran menurun', 'Pusing', 'Pilek menahun',
    'Sakit kepala', 'Sesak nafas', 'Sulit buka mulut', 'Telinga terasa penuh cairan'
]

DISEASES = [
    'Otitis Media Serosa', 'Polip Hidung', 'Faringitis Akut',
    'Infeksi Leher Dalam', 'Abses Retrofaring', 'Karsinoma Nafosaring'
]

DISEASE_DESCRIPTIONS = {
    'Otitis Media Serosa': 'Kondisi cairan di telinga tengah yang dapat memengaruhi pendengaran.',
    'Polip Hidung': 'Pertumbuhan berlebih di lapisan mukosa hidung yang dapat menghambat pernafasan.',
    'Faringitis Akut': 'Peradangan pada tenggorokan yang biasanya disebabkan oleh infeksi virus.',
    'Infeksi Leher Dalam': 'Infeksi serius pada struktur leher yang memerlukan perhatian medis.',
    'Abses Retrofaring': 'Kantong nanah di belakang tenggorokan yang dapat menyebabkan kesulitan menelan.',
    'Karsinoma Nafosaring': 'Kanker pada bagian atas tenggorokan yang memerlukan pemeriksaan mendalam.'
}

# Create Training Data
def create_training_data():
    return {
        'Otitis Media Serosa': {'total_cases': 7, 'symptoms': {'Telinga berdengung': 3, 'Telinga terasa penuh cairan': 4, 'Pendengaran menurun': 5}},
        'Polip Hidung': {'total_cases': 13, 'symptoms': {'Hidung buntu': 7, 'Iritasi hidung': 8, 'Penciuman terganggu': 7}},
        'Faringitis Akut': {'total_cases': 14, 'symptoms': {'Tenggorokan kering': 6, 'Nyeri kepala': 5, 'Nyeri waktu menelan': 7, 'Tenggorokan panas': 6}},
        'Infeksi Leher Dalam': {'total_cases': 30, 'symptoms': {'Badan panas': 10, 'Sesak nafas': 8, 'Nyeri leher': 7, 'Leher bengkak': 9, 'Sulit buka mulut': 6}},
        'Abses Retrofaring': {'total_cases': 30, 'symptoms': {'Badan panas': 8, 'Leher kaku': 7, 'Nyeri waktu menelan': 6, 'Pusing': 5, 'Sesak nafas': 4}},
        'Karsinoma Nafosaring': {'total_cases': 28, 'symptoms': {'Hidung buntu': 14, 'Ingus darah': 8, 'Mata juling': 6, 'Pusing': 7, 'Pilek menahun': 5}}
    }

# Naive Bayes Calculation
def calculate_naive_bayes(selected_symptoms, training_data):
    total_cases = sum(disease['total_cases'] for disease in training_data.values())
    posterior_probs = {}

    for disease, data in training_data.items():
        prior_prob = data['total_cases'] / total_cases
        likelihood = 1.0
        for symptom in selected_symptoms:
            symptom_count = data['symptoms'].get(symptom, 0)
            likelihood *= (symptom_count + 1) / (data['total_cases'] + len(SYMPTOMS))
        posterior_probs[disease] = prior_prob * likelihood
    
    return posterior_probs

# Visualization of Probabilities
def plot_disease_probabilities(probabilities):
    diseases = list(probabilities.keys())
    probs = list(probabilities.values())
    
    fig = go.Figure(data=[go.Bar(
        x=diseases, 
        y=probs, 
        marker_color='skyblue',
        text=[f'{p:.4f}' for p in probs],
        textposition='auto'
    )])
    
    fig.update_layout(
        title='Probabilitas Diagnosis Penyakit',
        xaxis_title='Penyakit',
        yaxis_title='Probabilitas',
        template='plotly_white'
    )
    
    return fig

# Recommend Further Actions
def get_recommendations(top_disease):
    recommendations = {
        'Otitis Media Serosa': [
            'Konsultasi dengan dokter THT',
            'Cek pendengaran secara berkala',
            'Hindari paparan suara keras'
        ],
        'Polip Hidung': [
            'Lakukan tes alergi',
            'Konsultasi bedah THT',
            'Pertimbangkan pembedahan'
        ],
        'Faringitis Akut': [
            'Istirahat yang cukup',
            'Minum air putih banyak',
            'Konsumsi obat pereda nyeri'
        ],
        'Infeksi Leher Dalam': [
            'Segera konsultasi dokter',
            'Terapi antibiotik',
            'Istirahat total'
        ],
        'Abses Retrofaring': [
            'Segera ke rumah sakit',
            'Terapi antibiotik',
            'Rawat inap mungkin diperlukan'
        ],
        'Karsinoma Nafosaring': [
            'Pemeriksaan onkologi menyeluruh',
            'CT Scan dan pemeriksaan lanjutan',
            'Konsultasi ahli kanker'
        ]
    }
    return recommendations.get(top_disease, [])

# Sidebar Menu
with st.sidebar:
    selected = option_menu(
        "Menu", ["Home", "Diagnosis", "Tentang"],
        icons=["house", "stethoscope", "info-circle"],
        menu_icon="cast",
        default_index=0
    )

# Home Page
if selected == "Home":
    st.title("Sistem Pakar Diagnosis Penyakit THT")
    st.write("Selamat datang di sistem pakar untuk mendiagnosis penyakit THT. Pilih menu 'Diagnosis' untuk memulai.")

# Diagnosis Page
elif selected == "Diagnosis":
    st.title("Diagnosis Penyakit THT")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Pilih gejala yang Anda alami:")
        selected_symptoms = st.multiselect('Gejala', SYMPTOMS)

    with col2:
        st.write("Filter Gejala:")
        min_symptoms = st.slider('Minimal Gejala', 1, 5, 1)

    if st.button("Diagnosa"):
        if len(selected_symptoms) < min_symptoms:
            st.warning(f"Silakan pilih minimal {min_symptoms} gejala.")
        else:
            training_data = create_training_data()
            probabilities = calculate_naive_bayes(selected_symptoms, training_data)
            sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

            st.subheader("Hasil Diagnosis")
            
            # Visualization of Probabilities
            fig = plot_disease_probabilities(probabilities)
            st.plotly_chart(fig)

            # Display Probabilities
            for disease, prob in sorted_probs:
                st.write(f"{disease}: {prob:.4f}")

            top_disease = sorted_probs[0][0]
            st.success(f"Penyakit yang paling mungkin: {top_disease}")
            
            # Disease Description
            st.info(f"Deskripsi: {DISEASE_DESCRIPTIONS[top_disease]}")

            # Recommendations
            st.subheader("Rekomendasi Tindakan")
            recommendations = get_recommendations(top_disease)
            for rec in recommendations:
                st.write(f"• {rec}")

            st.warning("PERHATIAN: Ini adalah sistem diagnosis otomatis. Selalu konsultasikan dengan profesional medis.")

# About Page
elif selected == "Tentang":
    st.title("Tentang Aplikasi")
    st.write("Aplikasi ini dikembangkan untuk membantu mendiagnosis penyakit THT berdasarkan gejala yang dialami.")
    
    st.subheader("Metodologi")
    st.write("Aplikasi menggunakan algoritma Naive Bayes untuk menghitung probabilitas penyakit berdasarkan gejala yang dipilih.")
    
    st.subheader("Batasan")
    st.write("""
    - Sistem ini tidak menggantikan diagnosis profesional medis
    - Akurasi bergantung pada data pelatihan yang terbatas
    - Selalu konsultasikan dengan dokter ahli
    """)

    st.subheader("Tentang Pengembang")
    st.write("Sistem pakar ini dikembangkan untuk membantu masyarakat mendapatkan informasi awal tentang potensi penyakit THT.")