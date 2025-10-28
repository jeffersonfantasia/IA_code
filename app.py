"""
Interface Streamlit para processamento de Notas Fiscais Eletrônicas (NF-e)
"""
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from nfe_parser import NFEParser


# Configuração da página
st.set_page_config(
    page_title="Processador de NF-e",
    page_icon="📄",
    layout="wide"
)

# Título
st.title("📄 Processador de Notas Fiscais Eletrônicas")
st.markdown("---")

# Descrição
st.markdown("""
Esta aplicação permite processar múltiplos arquivos XML de Notas Fiscais Eletrônicas (NF-e)
e visualizar os dados em formato tabular.

**Como usar:**
1. Digite o caminho da pasta contendo os arquivos XML
2. Clique em "Processar XMLs"
3. Visualize os dados na tabela
4. Exporte os resultados para Excel ou CSV
""")

st.markdown("---")

# Input para o caminho da pasta
col1, col2 = st.columns([3, 1])

with col1:
    folder_path = st.text_input(
        "📁 Caminho da pasta com arquivos XML",
        placeholder="/home/usuario/notas_fiscais",
        help="Digite o caminho completo da pasta contendo os arquivos XML"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Espaçamento
    process_button = st.button("🔄 Processar XMLs", type="primary", use_container_width=True)

# Estado da sessão para armazenar dados
if 'df_nfe' not in st.session_state:
    st.session_state.df_nfe = None

# Processamento
if process_button:
    if not folder_path:
        st.error("⚠️ Por favor, insira o caminho da pasta!")
    elif not os.path.exists(folder_path):
        st.error(f"⚠️ Pasta não encontrada: {folder_path}")
    elif not os.path.isdir(folder_path):
        st.error(f"⚠️ O caminho informado não é uma pasta: {folder_path}")
    else:
        try:
            with st.spinner("🔄 Processando arquivos XML..."):
                parser = NFEParser()
                df = parser.process_folder(folder_path)

                if df.empty:
                    st.warning("⚠️ Nenhum dado foi extraído dos arquivos XML.")
                else:
                    st.session_state.df_nfe = df
                    st.success(f"✅ {len(df)} nota(s) fiscal(is) processada(s) com sucesso!")

        except ValueError as e:
            st.error(f"⚠️ Erro: {str(e)}")
        except Exception as e:
            st.error(f"⚠️ Erro ao processar arquivos: {str(e)}")

# Exibição dos dados
if st.session_state.df_nfe is not None:
    df = st.session_state.df_nfe

    st.markdown("---")
    st.subheader("📊 Dados das Notas Fiscais")

    # Métricas resumidas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de NFs", len(df))

    with col2:
        if 'valor_total' in df.columns:
            total_value = df['valor_total'].sum()
            st.metric("Valor Total", f"R$ {total_value:,.2f}")

    with col3:
        if 'qtd_itens' in df.columns:
            total_items = df['qtd_itens'].sum()
            st.metric("Total de Itens", f"{total_items:,.0f}")

    with col4:
        if 'tipo_operacao' in df.columns:
            saidas = len(df[df['tipo_operacao'] == 'Saída'])
            st.metric("NFs de Saída", saidas)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtros
    with st.expander("🔍 Filtros", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            if 'emit_nome' in df.columns:
                emitentes = ['Todos'] + sorted(df['emit_nome'].dropna().unique().tolist())
                selected_emit = st.selectbox("Emitente", emitentes)

        with col2:
            if 'tipo_operacao' in df.columns:
                tipos = ['Todos'] + sorted(df['tipo_operacao'].dropna().unique().tolist())
                selected_tipo = st.selectbox("Tipo de Operação", tipos)

    # Aplicar filtros
    df_filtered = df.copy()

    if 'emit_nome' in df.columns and selected_emit != 'Todos':
        df_filtered = df_filtered[df_filtered['emit_nome'] == selected_emit]

    if 'tipo_operacao' in df.columns and selected_tipo != 'Todos':
        df_filtered = df_filtered[df_filtered['tipo_operacao'] == selected_tipo]

    # Seleção de colunas para exibir
    with st.expander("⚙️ Configurar Colunas", expanded=False):
        all_columns = df_filtered.columns.tolist()
        default_columns = [col for col in [
            'numero_nf', 'serie', 'data_emissao', 'emit_nome',
            'dest_nome', 'valor_total', 'tipo_operacao'
        ] if col in all_columns]

        selected_columns = st.multiselect(
            "Selecione as colunas para exibir",
            options=all_columns,
            default=default_columns
        )

    # Exibir tabela
    if selected_columns:
        st.dataframe(
            df_filtered[selected_columns],
            use_container_width=True,
            height=400
        )
    else:
        st.dataframe(df_filtered, use_container_width=True, height=400)

    # Exportação
    st.markdown("---")
    st.subheader("📥 Exportar Dados")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        # Exportar para Excel
        excel_buffer = pd.io.common.BytesIO()
        df_filtered.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)

        st.download_button(
            label="📊 Baixar Excel",
            data=excel_buffer,
            file_name=f"notas_fiscais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col2:
        # Exportar para CSV
        csv = df_filtered.to_csv(index=False).encode('utf-8-sig')

        st.download_button(
            label="📄 Baixar CSV",
            data=csv,
            file_name=f"notas_fiscais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Mostrar estatísticas detalhadas
    if st.checkbox("📈 Mostrar Estatísticas Detalhadas"):
        st.markdown("---")
        st.subheader("📈 Estatísticas")

        if 'valor_total' in df_filtered.columns:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Resumo de Valores:**")
                stats_df = df_filtered['valor_total'].describe()
                stats_df = pd.DataFrame(stats_df).T
                st.dataframe(stats_df, use_container_width=True)

            with col2:
                if 'tipo_operacao' in df_filtered.columns:
                    st.markdown("**Por Tipo de Operação:**")
                    tipo_summary = df_filtered.groupby('tipo_operacao').agg({
                        'numero_nf': 'count',
                        'valor_total': 'sum'
                    }).reset_index()
                    tipo_summary.columns = ['Tipo', 'Quantidade', 'Valor Total']
                    st.dataframe(tipo_summary, use_container_width=True)

else:
    st.info("👆 Insira o caminho da pasta e clique em 'Processar XMLs' para começar.")

# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Desenvolvido para processamento de Notas Fiscais Eletrônicas (NF-e)"
    "</div>",
    unsafe_allow_html=True
)
