import streamlit as st
from google import genai

st.set_page_config(page_title="Imagen Prompt Compiler", page_icon="🎨", layout="centered")
st.title("🌐 Multi-Lingual Imagen Prompt Expander")
st.markdown("Ubah kata sederhana menjadi *highly descriptive prose* untuk Google Imagen.")

api_key = st.text_input("Masukkan Google Gemini API Key Anda:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    
    try:
        available_models = []
        for m in client.models.list():
            model_name = m.name.replace('models/', '') if m.name.startswith('models/') else m.name
            
            # Filter ketat: Hindari model 2.5 yang sudah error, ambil versi terbaru
            if "gemini" in model_name and "2.5-flash" not in model_name:
                available_models.append(model_name)
                
        if not available_models:
            st.error("Tidak ada model AI yang kompatibel ditemukan.")
        else:
            # Coba jadikan gemini-3.8-flash sebagai pilihan default jika tersedia
            default_index = 0
            if "gemini-3.8-flash" in available_models:
                default_index = available_models.index("gemini-3.8-flash")
            
            st.markdown("### Konfigurasi Sistem")
            selected_model = st.selectbox(
                "Pilih Model AI (Direkomendasikan: gemini-3.8-flash):", 
                available_models,
                index=default_index
            )
            
            col1, col2 = st.columns(2)
            with col1:
                source_lang = st.selectbox("Bahasa Input:", ["Deteksi Otomatis", "Indonesia", "English", "Chinese"])
            with col2:
                target_lang = st.selectbox("Bahasa Output (Prompt Final):", ["English", "Indonesia", "Chinese"])
            
            st.info("💡 Tip: Imagen paling optimal menerima prompt dalam bahasa **English**.")
        
            user_concept = st.text_area("Masukkan Konsep Sederhana:", placeholder="Contoh: Kucing minum kopi")
        
            if st.button("Generate Extended Prompt", type="primary"):
                if not user_concept:
                    st.warning("Harap masukkan konsep terlebih dahulu.")
                else:
                    with st.spinner(f"Compiling menggunakan {selected_model}..."):
                        try:
                            system_directive = f"""
                            You are the 'Imagen Natural Language Compiler'.
                            1. Translate the user's concept into {target_lang}.
                            2. Expand the simple concept into a highly detailed, natural language prose (60-90 words) optimized for Google's Imagen text-to-image architecture.
                            3. Structure the prose strictly with: Primary Subject details, Dynamic Action, Spatial Environment, Lighting & Mood, Cinematic Medium/Camera specs, and Micro-textural details.
                            4. Output MUST be ONLY the compiled prompt in {target_lang}. No introductions, no bullet points.
                            """
                            
                            response = client.models.generate_content(
                                model=selected_model,
                                contents=[system_directive, user_concept]
                            )
                            
                            st.success("✅ Compilation Successful!")
                            st.text_area("Salin Prompt di Bawah Ini:", value=response.text, height=200)
                            
                        except Exception as e:
                            st.error(f"Terjadi kesalahan saat proses generasi: {e}")
                            
    except Exception as e:
        st.error(f"Gagal mengambil daftar model: {e}")
else:
    st.warning("🔑 Harap masukkan API Key untuk memulai.")