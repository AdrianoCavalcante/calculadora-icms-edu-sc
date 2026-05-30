"""
Módulo da Calculadora IQESC
============================

Sistema de cálculo e análise dos indicadores IQESC para municípios de SC.
"""

__all__ = ['CalculadoraIQESC']

# Import feito de forma a funcionar tanto localmente quanto no Streamlit Cloud
try:
    from .calculadora_iqesc import CalculadoraIQESC
except ImportError:
    # Se o import relativo falhar, tenta import direto
    try:
        from calculadora_iqesc import CalculadoraIQESC
    except ImportError:
        # Último fallback
        pass
