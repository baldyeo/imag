import streamlit as st
from google import genai

# Konfigurasi Halaman Web
st.set_page_config(page_title="Imagen Prompt Compiler", page_icon="🎨", layout="centered")

st.title("🌐 Multi-Lingual Imagen Prompt Expander")
st.markdown("Ubah kata sederhana menjadi *highly descriptive prose* untuk Google Imagen.")

# Konfigurasi API
api_key = st.text_input("Masukkan Google Gemini API Key Anda:", type="password")

if api_key:
    # Inisialisasi menggunakan format SDK Baru
    client = genai.Client(api_key=api_key)
    
    # Pengaturan Bahasa
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Bahasa Input:", ["Deteksi Otomatis", "Indonesia", "English", "Chinese"])
    with col2:
        target_lang = st.selectbox("Bahasa Output (Prompt Final):", ["English", "Indonesia", "Chinese"])
    
    st.info("💡 Tip: Imagen paling optimal menerima prompt dalam bahasa **English**.")

    # Input Konsep Sederhana
    user_concept = st.text_area("Masukkan Konsep Sederhana:", placeholder="Contoh: Kucing minum kopi / 喝咖啡的猫 / A cat drinking coffee")

    if st.button("Generate Extended Prompt", type="primary"):
        if not user_concept:
            st.warning("Harap masukkan konsep terlebih dahulu.")
        else:
            with st.spinner("Compiling & Translating..."):
                try:
                    # Core System Directive
                    system_directive = f"""
                    You are the 'Imagen Natural Language Compiler'.
                    1. Translate the user's concept into {target_lang}.
                    2. Expand the simple concept into a highly detailed, natural language prose (60-90 words) optimized for Google's Imagen text-to-image architecture.
                    3. Structure the prose strictly with: Primary Subject details, Dynamic Action, Spatial Environment, Lighting & Mood, Cinematic Medium/Camera specs, and Micro-textural details.
                    4. Output MUST be ONLY the compiled prompt in {target_lang}. No introductions, no bullet points, no technical parameters (like --ar or steps). Just one cohesive paragraph.
                    
                    User Concept: {user_concept}
                    """
                    
                    # Generate Respon dengan format SDK Baru
                    response = client.models.generate_content(
                        model='gemini-1.5-pro-latest',
                        contents=system_directive
                    )
                    
                    # Menampilkan Hasil
                    st.success("✅ Compilation Successful!")
                    st.text_area("Salin Prompt di Bawah Ini:", value=response.text, height=200)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
else:
    st.warning("🔑 Harap masukkan API Key untuk memulai. Anda bisa mendapatkannya secara gratis di Google AI Studio.")
