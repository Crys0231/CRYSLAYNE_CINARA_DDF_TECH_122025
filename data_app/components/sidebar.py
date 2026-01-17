"""
Componente de Sidebar Consistente para Data Driven Bearings
Sidebar unificada com seções de Contato e Documentação
"""
import streamlit as st
from datetime import datetime

def render_sidebar():
    """Renderiza sidebar profissional com Contato e Documentação"""
    
    with st.sidebar:
        # Logo e Título
        
        st.markdown("### ⚙️ **Data Driven Bearings**")
        st.markdown("*DDF Tech 2025*")
        st.divider()
        
        # Status do Sistema
        if 'engine' in st.session_state and st.session_state.engine:
            st.success("**Sistema Online**", icon="✅")
        else:
            st.error("Sistema Offline", icon="❌")
        
        st.divider()
        
        # Seção de Contato
        st.markdown("### 📞 **Suporte Técnico**")
        st.caption("📧 Email: cryslaynecinara0231@gmail.com")
        st.caption("📱 WhatsApp: +55 11 99859-0590")
        st.caption("🕐 Seg-Sex: 08h-18h (Brasília)")
        
        st.divider()
        
        # Seção de Documentação
        st.markdown("### 📚 **Documentação**")
        st.caption("[📖 Repo GitHub](https://github.com/Crys0231/CRYSLAYNE_CINARA_DDF_TECH_122025)")
        st.caption("[🎥 Vídeo Tutorial](https://youtube.com/@ddftech)")
        st.caption("🐛 [Reportar Bug](mailto:cryslaynecinara0231@gmail.com?subject=Bug%20Report%20-%20Data%20Driven%20Bearings)") 
        
        st.divider()
        
        # Footer
        st.caption("Data Driven Bearings • v3.2")
        st.caption(f"*Atualizado em {datetime.now().strftime('%d/%m/%Y')}*")
