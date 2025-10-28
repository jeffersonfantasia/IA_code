# Processador de Notas Fiscais Eletrônicas (NF-e)

Interface web para processar e visualizar dados de arquivos XML de Notas Fiscais Eletrônicas em formato tabular.

## Funcionalidades

- Processamento em lote de arquivos XML de NF-e
- Visualização dos dados em formato tabular interativo
- Filtros por emitente e tipo de operação
- Estatísticas e métricas resumidas
- Exportação para Excel (.xlsx) e CSV
- Seleção customizável de colunas
- Interface amigável e responsiva

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd IA_code
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## Como Usar

### 1. Execute a aplicação

```bash
streamlit run app.py
```

### 2. Acesse a interface

O navegador abrirá automaticamente em `http://localhost:8501`

### 3. Processe os XMLs

1. Digite o caminho completo da pasta contendo os arquivos XML de NF-e
   - Exemplo Linux/Mac: `/home/usuario/documentos/notas_fiscais`
   - Exemplo Windows: `C:\Users\Usuario\Documents\notas_fiscais`

2. Clique no botão **"Processar XMLs"**

3. Visualize os dados na tabela interativa

### 4. Utilize os recursos

- **Filtros:** Filtre por emitente ou tipo de operação
- **Configurar Colunas:** Selecione quais colunas deseja visualizar
- **Exportar:** Baixe os dados em formato Excel ou CSV
- **Estatísticas:** Visualize resumos e análises dos dados

## Dados Extraídos

O processador extrai as seguintes informações de cada nota fiscal:

### Identificação
- Número da NF
- Série
- Data de emissão
- Chave de acesso
- Natureza da operação
- Tipo de operação (Entrada/Saída)

### Emitente
- CNPJ
- Razão social
- Nome fantasia

### Destinatário
- CNPJ/CPF
- Nome

### Valores
- Valor dos produtos
- Valor de desconto
- Valor do frete
- Valor total da NF
- ICMS
- IPI

### Produtos
- Quantidade de itens

## Estrutura do Projeto

```
IA_code/
├── app.py                 # Interface Streamlit principal
├── nfe_parser.py          # Parser de arquivos XML de NF-e
├── requirements.txt       # Dependências do projeto
├── README.md             # Este arquivo
└── .gitignore            # Arquivos ignorados pelo Git
```

## Tecnologias Utilizadas

- **Streamlit:** Framework para criar a interface web
- **Pandas:** Manipulação e análise de dados
- **lxml:** Parsing de arquivos XML
- **openpyxl:** Exportação para Excel

## Formato dos Arquivos XML

A aplicação suporta arquivos XML de NF-e no formato padrão brasileiro (conforme especificação da SEFAZ).

## Troubleshooting

### Erro: "Pasta não encontrada"
- Verifique se o caminho está correto
- Use caminhos absolutos (caminho completo)
- No Windows, use barras invertidas `\` ou barras normais `/`

### Erro: "Nenhum arquivo XML encontrado"
- Verifique se os arquivos têm a extensão `.xml`
- Confirme se os arquivos estão na pasta especificada

### Erro ao processar XML
- Verifique se os arquivos XML estão no formato correto de NF-e
- Alguns arquivos corrompidos podem ser ignorados automaticamente

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto é open source e está disponível sob a licença MIT.

## Suporte

Para reportar problemas ou sugerir melhorias, abra uma issue no repositório.
