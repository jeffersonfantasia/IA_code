"""
Parser para arquivos XML de Notas Fiscais Eletrônicas (NF-e)
"""
import os
from lxml import etree
from typing import Dict, List, Optional
import pandas as pd


class NFEParser:
    """Classe para processar arquivos XML de NF-e"""

    # Namespaces comuns em NF-e
    NAMESPACES = {
        'nfe': 'http://www.portalfiscal.inf.br/nfe'
    }

    def __init__(self):
        self.data = []

    def parse_xml_file(self, file_path: str) -> Optional[Dict]:
        """
        Processa um arquivo XML de NF-e e extrai as informações principais

        Args:
            file_path: Caminho para o arquivo XML

        Returns:
            Dicionário com os dados extraídos ou None em caso de erro
        """
        try:
            tree = etree.parse(file_path)
            root = tree.getroot()

            # Tenta com namespace
            nfe_info = root.find('.//nfe:infNFe', self.NAMESPACES)

            # Se não encontrar, tenta sem namespace (XML sem namespace declarado)
            if nfe_info is None:
                # Remove namespace para facilitar busca
                for elem in root.iter():
                    if elem.tag.startswith('{'):
                        elem.tag = elem.tag.split('}')[1]
                nfe_info = root.find('.//infNFe')

            if nfe_info is None:
                return None

            # Extrai dados da identificação
            ide = nfe_info.find('.//ide')
            emit = nfe_info.find('.//emit')
            dest = nfe_info.find('.//dest')
            total = nfe_info.find('.//total')

            data = {
                'arquivo': os.path.basename(file_path),
                'numero_nf': self._get_text(ide, 'nNF'),
                'serie': self._get_text(ide, 'serie'),
                'data_emissao': self._get_text(ide, 'dhEmi') or self._get_text(ide, 'dEmi'),
                'chave_acesso': nfe_info.get('Id', '').replace('NFe', ''),

                # Emitente
                'emit_cnpj': self._get_text(emit, 'CNPJ'),
                'emit_nome': self._get_text(emit, 'xNome'),
                'emit_fantasia': self._get_text(emit, 'xFant'),

                # Destinatário
                'dest_cnpj': self._get_text(dest, 'CNPJ') or self._get_text(dest, 'CPF'),
                'dest_nome': self._get_text(dest, 'xNome'),

                # Valores
                'valor_produtos': self._get_text(total, './/vProd'),
                'valor_desconto': self._get_text(total, './/vDesc'),
                'valor_frete': self._get_text(total, './/vFrete'),
                'valor_total': self._get_text(total, './/vNF'),
                'valor_icms': self._get_text(total, './/vICMS'),
                'valor_ipi': self._get_text(total, './/vIPI'),

                # Natureza da operação
                'natureza_operacao': self._get_text(ide, 'natOp'),
                'tipo_operacao': 'Entrada' if self._get_text(ide, 'tpNF') == '0' else 'Saída',
            }

            # Extrai itens/produtos
            items = nfe_info.findall('.//det')
            data['qtd_itens'] = len(items)

            return data

        except Exception as e:
            return {
                'arquivo': os.path.basename(file_path),
                'erro': str(e)
            }

    def _get_text(self, parent, tag: str, default: str = '') -> str:
        """
        Busca o texto de um elemento filho

        Args:
            parent: Elemento pai
            tag: Tag do elemento filho
            default: Valor padrão se não encontrar

        Returns:
            Texto do elemento ou valor padrão
        """
        if parent is None:
            return default

        elem = parent.find(f'.//{tag}')
        if elem is not None and elem.text:
            return elem.text.strip()
        return default

    def process_folder(self, folder_path: str) -> pd.DataFrame:
        """
        Processa todos os arquivos XML em uma pasta

        Args:
            folder_path: Caminho da pasta com arquivos XML

        Returns:
            DataFrame com os dados de todas as notas fiscais
        """
        self.data = []

        if not os.path.exists(folder_path):
            raise ValueError(f"Pasta não encontrada: {folder_path}")

        # Lista todos os arquivos XML
        xml_files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith('.xml')
        ]

        if not xml_files:
            raise ValueError(f"Nenhum arquivo XML encontrado em: {folder_path}")

        # Processa cada arquivo
        for xml_file in xml_files:
            nfe_data = self.parse_xml_file(xml_file)
            if nfe_data:
                self.data.append(nfe_data)

        # Converte para DataFrame
        df = pd.DataFrame(self.data)

        # Formata colunas de valores como float
        value_columns = ['valor_produtos', 'valor_desconto', 'valor_frete',
                        'valor_total', 'valor_icms', 'valor_ipi']
        for col in value_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Formata data
        if 'data_emissao' in df.columns:
            df['data_emissao'] = pd.to_datetime(df['data_emissao'], errors='coerce')

        return df
