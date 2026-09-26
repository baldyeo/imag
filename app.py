import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman Web
st.set_page_config(page_title="Imagen Prompt Compiler", page_icon="🎨", layout="centered")

st.title("🌐 Multi-Lingual Imagen Prompt Expander")
st.markdown("Ubah kata sederhana menjadi *highly descriptive prose* untuk Google Imagen.")

# Konfigurasi API
api_key = st.text_input("Masukkan Google Gemini API Key Anda:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Bahasa Input:", ["Deteksi Otomatis", "Indonesia", "English", "Chinese"])
    with col2:
        target_lang = st.selectbox("Bahasa Output (Prompt Final):", ["English", "Indonesia", "Chinese"])
    
    st.info("💡 Tip: Imagen paling optimal menerima prompt dalam bahasa **English**.")

    user_concept = st.text_area("Masukkan Konsep Sederhana:", placeholder="Contoh: Kucing minum kopi / 喝咖啡的猫 / A cat drinking coffee")

    if st.button("Generate Extended Prompt", type="primary"):
        if not user_concept:
            st.warning("Harap masukkan konsep terlebih dahulu.")
        else:
            with st.spinner("Mencari model yang tersedia & Compiling..."):
                try:
                    # 1. AUTO-DISCOVERY: Tanya Google model apa yang bisa dipakai API Key ini
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    
                    # 2. Filter hanya untuk model Gemini
                    gemini_models = [name for name in available_models if 'gemini' in name]
                    
                    if not gemini_models:
                        st.error("API Key valid, tetapi tidak ada model teks Gemini yang diizinkan untuk akun/region ini.")
                    else:
                        # 3. Pilih otomatis (Prioritaskan Flash atau Pro, ambil opsi paling akhir/terbaru)
                        selected_model = gemini_models[-1]
                        for m in gemini_models:
                            if 'flash' in m:
                                selected_model = m
                                break
                                
                        st.success(f"Berhasil terhubung secara otomatis ke model: `{selected_model}`")
                        
                        system_directive = f"""
                        You are the 'Imagen Natural Language Compiler'.
                        1. Translate the user's concept into {target_lang}.
                        2. Expand the simple concept into a highly detailed, natural language prose (60-90 words) optimized for Google's Imagen text-to-image architecture.
                        3. Structure the prose strictly with: Primary Subject details, Dynamic Action, Spatial Environment, Lighting & Mood, Cinematic Medium/Camera specs, and Micro-textural details.
                        4. Output MUST be ONLY the compiled prompt in {target_lang}. No introductions, no bullet points, no technical parameters. Just one cohesive paragraph.
                        
                        User Concept: {user_concept}
                        """
                        
                        # Inisialisasi model hasil temuan otomatis
                        model = genai.GenerativeModel(selected_model)
                        
                        # Eksekusi Prompt
                        response = model.generate_content(system_directive)
                        
                        # Menampilkan Hasil
                        st.text_area("Salin Prompt di Bawah Ini:", value=response.text, height=200)
                        
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis: {e}")
else:
    st.warning("🔑 Harap masukkan API Key untuk memulai. Anda bisa mendapatkannya secara gratis di Google AI Studio.")
