"""
Interface Streamlit para Análise IQESC
Visualização interativa dos dados educacionais de SC
"""
import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório src ao path para imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import direto do arquivo, sem depender de __init__.py
from calculadora.calculadora_iqesc import CalculadoraIQESC

# Configuração da página
st.set_page_config(
    page_title="Análise IQESC - TCE-SC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .big-metric {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-left: 24px;
        padding-right: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Cache da calculadora
@st.cache_resource
def get_calculadora(ano, montante_icms, force_reload=False):
    """
    Carrega calculadora com cache e download automático
    
    Args:
        ano: Ano dos dados
        montante_icms: Valor total do ICMS Educacional
        force_reload: Forçar recarga (para invalidar cache)
    """
    return CalculadoraIQESC(ano=ano, auto_download=True, montante_total_icms=montante_icms)

def verificar_e_carregar_dados(ano, montante_icms, forcar_atualizacao=False):
    """
    Verifica cache e carrega dados automaticamente
    
    Args:
        ano: Ano dos dados
        montante_icms: Valor total do ICMS Educacional
        forcar_atualizacao: Se True, força download mesmo com cache existente
    
    Returns:
        (calculadora, mensagem_status)
    """
    from pathlib import Path
    import subprocess
    import sys
    
    cache_dir = Path(__file__).parent / "cache" / f"iqesc_{ano}"
    dados_cache = cache_dir / "dados.json"
    dados_legacy = Path(__file__).parent / f"iqesc_dados_{ano}.json"
    
    # Verifica se dados existem
    dados_existem = dados_cache.exists() or dados_legacy.exists()
    
    # Se forçar atualização ou dados não existem
    if forcar_atualizacao or not dados_existem:
        
        if forcar_atualizacao:
            st.info(f"🔄 Forçando atualização dos dados para o ano {ano}")
        else:
            st.info(f"📥 Dados não encontrados no cache para o ano {ano}")
        
        st.info(f"🌐 Conectando ao TCE-SC para baixar dados...")
        
        # Barra de progresso
        progress_bar = st.progress(0, text="Iniciando download...")
        
        try:
            # Executa scraper
            scraper_path = Path(__file__).parent / "src" / "iqesc_scraper_dinamico.py"
            
            if not scraper_path.exists():
                progress_bar.empty()
                return None, f"❌ Scraper não encontrado"
            
            progress_bar.progress(20, text="Conectando ao TCE-SC...")
            
            # Argumentos para o scraper
            args = [sys.executable, str(scraper_path), str(ano)]
            if forcar_atualizacao:
                args.append("--force-update")
            
            # Executa o scraper
            resultado = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            progress_bar.progress(80, text="Processando dados...")
            
            if resultado.returncode == 0:
                progress_bar.progress(100, text="Download concluído!")
                progress_bar.empty()
                
                # Carrega dados baixados
                try:
                    calc = CalculadoraIQESC(ano=ano, auto_download=False, montante_total_icms=montante_icms)
                    mensagem = f"✅ Dados {'atualizados' if forcar_atualizacao else 'baixados'} com sucesso do TCE-SC"
                    return calc, mensagem
                except Exception as e:
                    return None, f"❌ Erro ao carregar dados após download: {e}"
            else:
                progress_bar.empty()
                
                # Verifica se é problema de conexão ou dados não disponíveis
                erro_output = resultado.stdout + resultado.stderr
                if "Sem conexão" in erro_output or "connection" in erro_output.lower():
                    return None, f"❌ Sem conexão com internet. Não é possível baixar dados para {ano}."
                else:
                    return None, f"❌ Não foram encontrados dados para o ano {ano} no TCE-SC.\n\nDetalhes: {resultado.stderr[:200]}"
                    
        except subprocess.TimeoutExpired:
            progress_bar.empty()
            return None, f"⚠️ Timeout ao tentar baixar dados. Tente novamente."
        except Exception as e:
            progress_bar.empty()
            return None, f"❌ Erro ao baixar dados: {e}"
    else:
        # Carrega do cache
        try:
            calc = CalculadoraIQESC(ano=ano, auto_download=False, montante_total_icms=montante_icms)
            return calc, f"✅ Dados carregados do cache local"
        except Exception as e:
            return None, f"❌ Erro ao carregar cache: {e}"

# Título principal
st.title("📊 Análise IQESC - Indicadores Educacionais de Santa Catarina")
st.markdown("**Fonte:** Tribunal de Contas do Estado de Santa Catarina (TCE-SC)")

# Sidebar - Seleção de ano
st.sidebar.header("⚙️ Configurações")

# Input de ano com validação
st.sidebar.markdown("### 📅 Ano de Referência")
ano_selecionado = st.sidebar.number_input(
    "Digite o ano desejado:",
    min_value=2020,
    max_value=2030,
    value=2024,
    step=1,
    help="Digite o ano para o qual deseja consultar os dados IQESC"
)

# Input de montante total do ICMS
st.sidebar.markdown("### 💰 ICMS Educacional")
montante_icms = st.sidebar.number_input(
    "Montante Total Anual (R$):",
    min_value=0.0,
    max_value=10000000000.0,
    value=0.0,
    step=1000000.0,
    format="%.2f",
    help="Valor total do ICMS Educacional a ser distribuído entre os municípios. Deixe 0 para não calcular repasses."
)

st.sidebar.markdown("---")

# Botão para forçar atualização
if st.sidebar.button("🔄 Forçar Atualização de Dados", use_container_width=True):
    # Marca flag para forçar atualização no próximo carregamento
    st.session_state['forcar_atualizacao'] = True
    st.session_state['ultimo_ano'] = None  # Força recarregamento
    st.rerun()

st.sidebar.markdown("---")

# Verifica se precisa forçar atualização (e reseta a flag)
forcar_atualizacao = st.session_state.get('forcar_atualizacao', False)
if forcar_atualizacao:
    st.session_state['forcar_atualizacao'] = False

# Verifica se ano ou montante mudou
ultimo_ano = st.session_state.get('ultimo_ano', None)
ultimo_montante = st.session_state.get('ultimo_montante', None)

# Só carrega se mudou algo ou é primeira execução
if (ultimo_ano != ano_selecionado or 
    ultimo_montante != montante_icms or 
    'calc' not in st.session_state or
    forcar_atualizacao):
    
    # Salva valores atuais
    st.session_state['ultimo_ano'] = ano_selecionado
    st.session_state['ultimo_montante'] = montante_icms
    
    # Carrega calculadora
    try:
        with st.spinner(f"🔍 Verificando dados para o ano {ano_selecionado}..."):
            calc, mensagem = verificar_e_carregar_dados(ano_selecionado, montante_icms, forcar_atualizacao)
        
        if calc is None:
            st.error(mensagem)
            st.info("""
            💡 **Dicas:**
            - Verifique sua conexão com internet
            - Confirme se o ano digitado tem dados disponíveis no TCE-SC
            - Tente executar manualmente: `python src/iqesc_scraper_dinamico.py {ano}`
            - Use o botão "🔄 Forçar Atualização" se os dados estiverem desatualizados
            """.format(ano=ano_selecionado))
            st.stop()
        else:
            # Salva calculadora no session_state
            st.session_state['calc'] = calc
            st.session_state['mensagem'] = mensagem
    except Exception as e:
        st.error(f"❌ Erro inesperado: {e}")
        st.stop()

# Recupera calculadora do session_state
calc = st.session_state.get('calc')
mensagem = st.session_state.get('mensagem', '')

# Verifica se calculadora foi carregada com sucesso
if calc is None:
    st.error("❌ Nenhum dado carregado. Ajuste o ano ou use o botão de atualização.")
    st.stop()

# Mostra mensagem de sucesso
st.sidebar.success(mensagem)

# Mostra info sobre montante ICMS
if montante_icms > 0:
    st.sidebar.info(f"💵 Montante: R$ {montante_icms:,.2f}")
else:
    st.sidebar.warning("⚠️ Montante ICMS não informado. Valores de repasse não serão calculados.")

# Estatísticas gerais na sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Visão Geral")

stats = calc.calcular_estatisticas_gerais()
st.sidebar.metric("Total de Municípios", stats['total_municipios'])
st.sidebar.metric("IQESC Médio", f"{stats['iqesc']['media']:.4f}")
st.sidebar.metric("IQESC Máximo", f"{stats['iqesc']['maximo']:.4f}")
st.sidebar.metric("IQESC Mínimo", f"{stats['iqesc']['minimo']:.4f}")

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs([
    "🏛️ Análise por Município",
    "🏆 Rankings",
    "📊 Estatísticas Gerais",
    "💾 Exportar Dados"
])

# ============================================================================
# TAB 1: ANÁLISE POR MUNICÍPIO
# ============================================================================
with tab1:
    st.header("🏛️ Análise Detalhada por Município")
    st.markdown("Selecione um município para ver análise completa dos indicadores educacionais.")
    
    # Seleção de município
    municipios = calc.listar_municipios()
    municipio_selecionado = st.selectbox(
        "🔍 Selecione o Município:",
        options=municipios,
        placeholder="Digite ou selecione um município..."
    )
    
    if municipio_selecionado:
        analise = calc.analisar_municipio(municipio_selecionado)
        
        if 'erro' not in analise:
            m = analise['municipio']
            r = analise['ranking']
            d = analise['analise_desempenho']
            c = analise['comparacao_estadual']
            
            # Métricas principais
            st.markdown("### 📈 Índices Principais")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "IQESC Atual",
                    f"{d['iqesc_atual']:.4f}",
                    f"{d['gap_melhoria']:.4f} até máximo"
                )
            
            with col2:
                st.metric(
                    "Aproveitamento",
                    f"{d['aproveitamento_percentual']:.1f}%",
                    f"{d['classificacao'].split()[1]}"
                )
            
            with col3:
                st.metric(
                    "Ranking Estadual",
                    f"{r['posicao']}º",
                    f"de {r['total']} municípios"
                )
            
            with col4:
                delta_icon = "+" if c['posicao_relativa'] == 'acima' else "-"
                st.metric(
                    "vs Média Estadual",
                    f"{delta_icon}{c['diferenca']:.4f}",
                    f"{c['posicao_relativa'].capitalize()}"
                )
            
            st.markdown("---")
            
            # Repasse Financeiro (se montante foi informado)
            if montante_icms > 0 and 'repasse_financeiro' in analise:
                rep = analise['repasse_financeiro']
                
                st.markdown("### 💰 Repasse Financeiro (ICMS Educacional)")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Repasse Atual",
                        f"R$ {rep['repasse_atual']:,.2f}",
                        help=f"Baseado no IQESC atual de {d['iqesc_atual']:.4f}"
                    )
                
                with col2:
                    st.metric(
                        "Repasse Potencial",
                        f"R$ {rep['repasse_maximo']:,.2f}",
                        help="Se o município atingir IQESC = 1.0000"
                    )
                
                with col3:
                    st.metric(
                        "Gap Financeiro",
                        f"R$ {rep['gap_financeiro']:,.2f}",
                        f"{(rep['gap_financeiro']/rep['repasse_atual']*100) if rep['repasse_atual'] > 0 else 0:.1f}% potencial",
                        delta_color="normal"
                    )
                
                with col4:
                    st.metric(
                        "% da Distribuição",
                        f"{rep['percentual_distribuicao']:.4f}%",
                        help="Participação deste município no total estadual"
                    )
                
                st.markdown("---")
            
            # Indicadores detalhados
            st.markdown("### 📊 Indicadores Detalhados")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Componentes do IQESC")
                
                # Barra de progresso para cada indicador
                indicadores = [
                    ("IEO - Esforço Observado", m['ieo']),
                    ("IPA - Proficiência Avaliada", m['ipa']),
                    ("IEE - Esforço Escolar", m['iee']),
                    ("IEN - Esforço Não Observado", m['ien']),
                    ("CSE - Contexto Socioeconômico", m['cse']),
                    ("SCE - Sistema de Custos", m['sce']),
                ]
                
                for nome, valor in indicadores:
                    st.progress(valor, text=f"{nome}: {valor:.4f}")
            
            with col2:
                st.markdown("#### 💪 Pontos Fortes (Top 3)")
                for i, (indicador, valor) in enumerate(analise['pontos_fortes'], 1):
                    st.success(f"**{i}.** {indicador}: {valor:.4f}")
                
                st.markdown("#### ⚠️ Pontos de Atenção (3 Mais Fracos)")
                for i, (indicador, valor) in enumerate(analise['pontos_fracos'], 1):
                    st.warning(f"**{i}.** {indicador}: {valor:.4f}")
            
            st.markdown("---")
            
            # Recomendações
            st.markdown("### 💡 Recomendações Estratégicas")
            for rec in analise['recomendacoes']:
                if "CRÍTICA" in rec:
                    st.error(rec)
                elif "ATENÇÃO" in rec:
                    st.warning(rec)
                elif "GAP" in rec:
                    st.info(rec)
                else:
                    st.success(rec)
            
            st.markdown("---")
            
            # Botão para relatório completo
            st.markdown("### 📄 Relatório Completo")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if st.button("📋 Gerar Relatório Textual Completo", type="primary"):
                    relatorio = calc.gerar_relatorio_completo(municipio_selecionado)
                    st.session_state['relatorio_atual'] = relatorio
                    st.success("✅ Relatório gerado!")
            
            # Exibe relatório se disponível
            if 'relatorio_atual' in st.session_state:
                st.text_area(
                    "Relatório:",
                    st.session_state['relatorio_atual'],
                    height=600,
                    help="Você pode copiar este texto e colar em outro documento"
                )
                
                # Download do relatório
                st.download_button(
                    label="⬇️ Baixar Relatório (.txt)",
                    data=st.session_state['relatorio_atual'],
                    file_name=f"relatorio_iqesc_{municipio_selecionado.replace(' ', '_')}_{ano_selecionado}.txt",
                    mime="text/plain"
                )
        else:
            st.error(analise['erro'])
    
    # ============================================================================
    # TAB 2: RANKINGS
    # ============================================================================
    with tab2:
        st.header("🏆 Rankings dos Municípios")
        
        # Seleção de indicador e quantidade
        col1, col2 = st.columns([2, 1])
        
        with col1:
            indicador_ranking = st.selectbox(
                "Ordenar por:",
                options=[
                    ('iqesc', 'IQESC (Índice Final)'),
                    ('ieo', 'IEO - Esforço Observado'),
                    ('ipa', 'IPA - Proficiência Avaliada'),
                    ('iee', 'IEE - Esforço Escolar'),
                    ('ien', 'IEN - Esforço Não Observado'),
                    ('cse', 'CSE - Contexto Socioeconômico'),
                    ('sce', 'SCE - Sistema de Custos'),
                ],
                format_func=lambda x: x[1]
            )
        
        with col2:
            top_n = st.number_input(
                "Quantidade:",
                min_value=5,
                max_value=100,
                value=20,
                step=5
            )
        
        # Gera ranking
        ranking = calc.ranking_municipios(top_n=top_n, por=indicador_ranking[0])
        
        # Exibe em formato de tabela bonita
        st.markdown(f"### Top {top_n} - {indicador_ranking[1]}")
        
        # Prepara dados para tabela
        dados_tabela = []
        for i, m in enumerate(ranking, 1):
            dados_tabela.append({
                '🏅 Posição': f"{i}º",
                '🏛️ Município': m['nome'],
                '📊 IQESC': f"{m['iqesc']:.4f}",
                '📈 IEO': f"{m['ieo']:.4f}",
                '📚 IPA': f"{m['ipa']:.4f}",
                '🎓 IEE': f"{m['iee']:.4f}",
                '💼 IEN': f"{m['ien']:.4f}",
                '🏘️ CSE': f"{m['cse']:.4f}",
                '💰 SCE': f"{m['sce']:.4f}",
            })
        
        st.dataframe(
            dados_tabela,
            width='stretch',
            hide_index=True
        )
        
        # Destaque top 3
        st.markdown("### 🥇 Pódio")
        col1, col2, col3 = st.columns(3)
        
        if len(ranking) >= 1:
            with col1:
                st.markdown("#### 🥇 1º Lugar")
                st.info(f"**{ranking[0]['nome']}**")
                st.metric(indicador_ranking[1], f"{ranking[0][indicador_ranking[0]]:.4f}")
        
        if len(ranking) >= 2:
            with col2:
                st.markdown("#### 🥈 2º Lugar")
                st.info(f"**{ranking[1]['nome']}**")
                st.metric(indicador_ranking[1], f"{ranking[1][indicador_ranking[0]]:.4f}")
        
        if len(ranking) >= 3:
            with col3:
                st.markdown("#### 🥉 3º Lugar")
                st.info(f"**{ranking[2]['nome']}**")
                st.metric(indicador_ranking[1], f"{ranking[2][indicador_ranking[0]]:.4f}")
    
    # ============================================================================
    # TAB 3: ESTATÍSTICAS GERAIS
    # ============================================================================
    with tab3:
        st.header("📊 Estatísticas Gerais do Estado")
        
        stats = calc.calcular_estatisticas_gerais()
        
        # Métricas IQESC
        st.markdown("### 📈 IQESC (Índice Geral)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Média", f"{stats['iqesc']['media']:.4f}")
        
        with col2:
            st.metric("Mediana", f"{stats['iqesc']['mediana']:.4f}")
        
        with col3:
            st.metric("Máximo", f"{stats['iqesc']['maximo']:.4f}")
        
        with col4:
            st.metric("Mínimo", f"{stats['iqesc']['minimo']:.4f}")
        
        st.metric("Desvio Padrão", f"{stats['iqesc']['desvio_padrao']:.4f}")
        
        st.markdown("---")
        
        # Estatísticas por indicador
        st.markdown("### 📊 Estatísticas por Indicador")
        
        for indicador_key, indicador_nome in [
            ('ieo', 'IEO - Esforço Observado'),
            ('ipa', 'IPA - Proficiência Avaliada'),
            ('iee', 'IEE - Esforço Escolar'),
            ('ien', 'IEN - Esforço Não Observado'),
            ('cse', 'CSE - Contexto Socioeconômico'),
            ('sce', 'SCE - Sistema de Custos'),
        ]:
            with st.expander(f"📌 {indicador_nome}"):
                ind_stats = stats['indicadores'][indicador_key]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Média", f"{ind_stats['media']:.4f}")
                
                with col2:
                    st.metric("Máximo", f"{ind_stats['maximo']:.4f}")
                
                with col3:
                    st.metric("Mínimo", f"{ind_stats['minimo']:.4f}")
    
    # ============================================================================
    # TAB 4: EXPORTAR DADOS
    # ============================================================================
    with tab4:
        st.header("💾 Exportar Dados")
        st.markdown("Exporte os dados de todos os municípios para análise externa.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📄 Exportar CSV")
            st.markdown("Formato compacto, ideal para planilhas e análises estatísticas.")
            
            if st.button("📥 Gerar CSV", type="primary"):
                with st.spinner("Gerando arquivo CSV..."):
                    arquivo = calc.exportar_todos_csv()
                    st.success(f"✅ Arquivo gerado: `{Path(arquivo).name}`")
                    
                    # Lê e oferece download
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        csv_data = f.read()
                    
                    st.download_button(
                        label="⬇️ Baixar CSV",
                        data=csv_data,
                        file_name=f"iqesc_completo_{ano_selecionado}.csv",
                        mime="text/csv"
                    )
        
        with col2:
            st.markdown("### 📋 Exportar JSON")
            st.markdown("Formato completo com todas as análises e metadados.")
            
            if st.button("📥 Gerar JSON", type="primary"):
                with st.spinner("Gerando arquivo JSON..."):
                    arquivo = calc.exportar_todos_json()
                    st.success(f"✅ Arquivo gerado: `{Path(arquivo).name}`")
                    
                    # Lê e oferece download
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        json_data = f.read()
                    
                    st.download_button(
                        label="⬇️ Baixar JSON",
                        data=json_data,
                        file_name=f"iqesc_analise_completa_{ano_selecionado}.json",
                        mime="application/json"
                    )
        
        st.markdown("---")
        st.info("💡 **Dica:** Os arquivos também são salvos no diretório raiz do projeto.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        📊 Análise IQESC | TCE-SC<br>
        Desenvolvido para análise de indicadores educacionais de Santa Catarina
    </div>
""", unsafe_allow_html=True)
