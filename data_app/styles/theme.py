"""
Sistema de tema e estilos para Data Driven Bearings
Design System Professional
"""

# ============================================================================
# CORES CORPORATIVAS
# ============================================================================

COLORS = {
    # Primárias
    'primary': '#0066CC',          # Azul profissional
    'primary_light': '#E6F2FF',    # Azul muito claro
    'primary_dark': '#003D99',     # Azul escuro
    
    # Secundárias
    'secondary': '#00B4D8',        # Ciano moderno
    'secondary_light': '#E0F7FF',  # Ciano claro
    
    # Status
    'success': '#10B981',          # Verde sucesso
    'success_light': '#D1FAE5',    # Verde claro
    'warning': '#F59E0B',          # Âmbar alerta
    'warning_light': '#FEF3C7',    # Âmbar claro
    'error': '#EF4444',            # Vermelho erro
    'error_light': '#FEE2E2',      # Vermelho claro
    'info': '#3B82F6',             # Azul info
    
    # Neutras
    'dark': '#0F172A',             # Fundo escuro
    'darker': '#0A0F1F',           # Fundo mais escuro
    'light': '#F8FAFC',            # Fundo claro
    'white': '#FFFFFF',            # Branco puro
    'gray_100': '#F1F5F9',
    'gray_200': '#E2E8F0',
    'gray_300': '#CBD5E1',
    'gray_400': '#94A3B8',
    'gray_500': '#64748B',
    'gray_600': '#475569',
    'gray_700': '#334155',
    'gray_800': '#1E293B',
    'gray_900': '#0F172A',
    
    # Gradientes
    'gradient_primary': 'linear-gradient(135deg, #0066CC 0%, #00B4D8 100%)',
    'gradient_success': 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
}

# ============================================================================
# TYPOGRAPHY
# ============================================================================

FONTS = {
    'family_primary': "'Inter', 'Segoe UI', sans-serif",
    'family_mono': "'Fira Code', 'Courier New', monospace",
    
    # Tamanhos
    'h1': {'size': '32px', 'weight': 700, 'line_height': '1.2'},
    'h2': {'size': '24px', 'weight': 600, 'line_height': '1.3'},
    'h3': {'size': '20px', 'weight': 600, 'line_height': '1.4'},
    'h4': {'size': '18px', 'weight': 600, 'line_height': '1.5'},
    'body_lg': {'size': '16px', 'weight': 400, 'line_height': '1.6'},
    'body': {'size': '14px', 'weight': 400, 'line_height': '1.5'},
    'body_sm': {'size': '12px', 'weight': 400, 'line_height': '1.5'},
    'button': {'size': '14px', 'weight': 600, 'line_height': '1.5'},
}

# ============================================================================
# ESPAÇAMENTO
# ============================================================================

SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '16px',
    'lg': '24px',
    'xl': '32px',
    'xxl': '48px',
}

# ============================================================================
# BORDER RADIUS
# ============================================================================

RADIUS = {
    'none': '0px',
    'sm': '4px',
    'base': '8px',
    'md': '12px',
    'lg': '16px',
    'full': '9999px',
}

# ============================================================================
# SOMBRAS
# ============================================================================

SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    'base': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
}

# ============================================================================
# TRANSIÇÕES
# ============================================================================

TRANSITIONS = {
    'fast': '150ms ease-in-out',
    'base': '250ms ease-in-out',
    'slow': '350ms ease-in-out',
}
