"""
Funções para matplotlib com tema escuro padronizado
Elimina 100+ linhas de duplicação
"""
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict

# Paleta de cores do projeto
DARK_COLORS = {
    'bg': '#0F172A',
    'surface': '#1A1F3A',
    'border': '#334155',
    'text': '#E2E8F0',
    'tick': '#94A3B8',
    'grid': '#334155',
    'primary': '#0066CC',
    'secondary': '#00B4D8',
    'success': '#10B981',
    'warning': '#F59E0B',
    'error': '#EF4444'
}

def setup_dark_figure(figsize=(12, 5)) -> Tuple[plt.Figure, plt.Axes]:
    """
    Cria figura com tema escuro padronizado
    Substitui: fig.patch.set_facecolor() + ax.set_facecolor() em 3 lugares
    """
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(DARK_COLORS['bg'])
    ax.set_facecolor(DARK_COLORS['surface'])
    apply_dark_style(fig, ax)
    return fig, ax

def apply_dark_style(fig: plt.Figure, ax: plt.Axes) -> None:
    """Aplica tema escuro a figura existente"""
    for spine in ax.spines.values():
        spine.set_color(DARK_COLORS['border'])
        spine.set_linewidth(1)
    
    ax.tick_params(colors=DARK_COLORS['tick'], labelsize=9)
    ax.xaxis.label.set_color(DARK_COLORS['text'])
    ax.yaxis.label.set_color(DARK_COLORS['text'])
    ax.title.set_color(DARK_COLORS['text'])
    ax.grid(alpha=0.15, linestyle='--', color=DARK_COLORS['grid'])

def setup_subplots_dark(rows: int, cols: int, figsize=(14, 8)):
    """Cria múltiplos subplots com tema escuro"""
    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor(DARK_COLORS['bg'])
    gs = fig.add_gridspec(rows, cols, hspace=0.3, wspace=0.3)
    
    axes = []
    for i in range(rows):
        row_axes = []
        for j in range(cols):
            ax = fig.add_subplot(gs[i, j])
            ax.set_facecolor(DARK_COLORS['surface'])
            apply_dark_style(fig, ax)
            row_axes.append(ax)
        axes.append(row_axes)
    
    return fig, axes

def style_bar_chart(ax: plt.Axes, bars, color: str = None):
    """Estiliza barras com cores consistentes"""
    if color is None:
        color = DARK_COLORS['primary']
    
    for bar in bars:
        bar.set_color(color)
        bar.set_edgecolor(DARK_COLORS['text'])
        bar.set_linewidth(1.5)
        bar.set_alpha(0.9)
