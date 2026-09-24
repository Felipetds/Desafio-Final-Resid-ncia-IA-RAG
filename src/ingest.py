import os
import json
import csv
from bs4 import BeautifulSoup
import pypdf

def criar_chunk_base(texto, source_file, doc_type, chunk_idx, base_id, sensitivity, extras):
    metadata = {
        "chunk_id": f"{source_file}_chunk_{chunk_idx}",
        "source_file": source_file,
        "doc_type": doc_type,
        "sensitivity": sensitivity,
        "base_id": base_id
    }
    metadata.update(extras)
    return {"text": texto, "metadata": metadata}

def extrair_metadados_especificos(natureza, dados=None):
    # Inicializa todas as chaves obrigatórias como strings vazias
    meta = {
        "natureza": natureza, "uf": "", "ano": "", "modalidade": "",
        "orgao": "", "municipio": "", "valor": "", "fornecedor": "", "vigencia": ""
    }
    
    if dados is None:
        return meta

    if natureza == "estruturada":
        # Navega de forma segura pelos nós do JSON do PNCP
        unidade_orgao = dados.get("unidadeOrgao", {}) or {}
        orgao_entidade = dados.get("orgaoEntidade", {}) or {}
        
        meta["uf"] = unidade_orgao.get("ufSigla", "")
        meta["municipio"] = unidade_orgao.get("municipioNome", "")
        meta["orgao"] = orgao_entidade.get("razaoSocial", "")
        meta["ano"] = dados.get("anoCompra", "")
        meta["modalidade"] = dados.get("modalidadeNome", "")
        
        # Prioriza o valor homologado; se nulo, usa o estimado
        valor_homologado = dados.get("valorTotalHomologado")
        valor_estimado = dados.get("valorTotalEstimado")
        meta["valor"] = valor_homologado if valor_homologado is not None else (valor_estimado if valor_estimado is not None else "")
        
    elif natureza == "agregada":
        # Extrai dados do CSV massivo (cada linha é um dicionário)
        meta["uf"] = dados.get("UF", "")
        meta["municipio"] = dados.get("Município", "")
        meta["orgao"] = dados.get("Órgão", "")
        meta["ano"] = dados.get("Ano", "")
        meta["valor"] = dados.get("Valor Estimado", "")

    return meta

def processar_estruturada(caminho):
    chunks = []
    if not os.path.exists(caminho): return chunks
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    registros = dados if isinstance(dados, list) else [dados]
    
    for idx, reg in enumerate(registros, 1):
        # Transforma o JSON em texto legível para o chunk
        texto = json.dumps(reg, ensure_ascii=False)
        extras = extrair_metadados_especificos("estruturada", reg)
        chunks.append(criar_chunk_base(texto, os.path.basename(caminho), "contrato", idx, "base_estruturada", "publico", extras))
    return chunks

def processar_normativa(caminho):
    chunks = []
    if not os.path.exists(caminho): return chunks
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except UnicodeDecodeError:
        with open(caminho, "r", encoding="latin-1") as f:
            soup = BeautifulSoup(f, "html.parser")
            
    texto = soup.get_text(separator=" ")
    # Separa adequadamente os artigos conforme checklist
    artigos = texto.split("Art. ")
    for idx, art in enumerate(artigos[1:], 1):
        extras = extrair_metadados_especificos("normativa")
        chunks.append(criar_chunk_base(f"Art. {art.strip()}", os.path.basename(caminho), "lei", idx, "base_normativa", "publico", extras))
    return chunks

def processar_agregada(caminho, limit=500):
    chunks = []
    if not os.path.exists(caminho): return chunks
    # Assegura que o separador é o ponto e vírgula e a codificação é utf-8 (padrão Brasil)
    with open(caminho, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        for idx, row in enumerate(reader, 1):
            if idx > limit:
                break
            # Transforma a linha do CSV num texto único para pesquisa
            texto = " | ".join([f"{k}: {v}" for k, v in row.items() if v])
            extras = extrair_metadados_especificos("agregada", row)
            chunks.append(criar_chunk_base(texto, os.path.basename(caminho), "relatorio", idx, "base_agregada", "publico", extras))
    return chunks

def processar_conversacional(caminho):
    chunks = []
    if not os.path.exists(caminho): return chunks
    texto_completo = ""
    
    if caminho.endswith(".pdf"):
        with open(caminho, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                extract = page.extract_text()
                if extract:
                    texto_completo += extract + "\n"
    elif caminho.endswith(".txt"):
        with open(caminho, "r", encoding="utf-8") as f:
            texto_completo = f.read()
            
    # Ajuste do tamanho dos chunks: Quebra em parágrafos para não ficarem excessivamente longos
    paragrafos = [p.strip() for p in texto_completo.split("\n\n") if len(p.strip()) > 10]
    for idx, p in enumerate(paragrafos, 1):
        extras = extrair_metadados_especificos("conversacional")
        chunks.append(criar_chunk_base(p, os.path.basename(caminho), "ata_reuniao", idx, "base_conversacional", "restrito", extras))
    return chunks

def rodar_ingestao_hibrida():
    print("Iniciando ingestão (Metadados Reais e Ajustes de Fatiamento)...")
    todos_chunks = []
    
    caminho_est = "data/raw/v2/estruturada/pncp/rj/pregao_eletronico/2026-03/contratacoes_publicacao.json"
    todos_chunks.extend(processar_estruturada(caminho_est))
    
    caminho_norm = "data/raw/v2/normativa/federal/lei_14133_2021/lei_14133_2021.html"
    todos_chunks.extend(processar_normativa(caminho_norm))
    
    caminhos_agg = [
        "data/raw/v2/agregada/pca_2026_estado_rj.csv",
        "data/raw/v2/agregada/itens_pe_038_26_2026.csv"
    ]
    for c in caminhos_agg:
        # Mantém a amostra determinística de 500 registos exigida pelo checklist
        todos_chunks.extend(processar_agregada(c, limit=500))
        
    caminhos_conv = [
        "data/raw/v2/conversacional/atas/ebserh/2026/ata_00191.pdf",
        "data/raw/v2/conversacional/atas/fiocruz/2026/ata_00001.pdf",
        "data/raw/v2/conversacional/atas/ministerio_saude/2026/ata_00137.pdf",
        "data/raw/v2/conversacional/comunicacoes_sinteticas/troca_mensagens_material_escritorio_001.txt"
    ]
    for c in caminhos_conv:
        todos_chunks.extend(processar_conversacional(c))

    os.makedirs("data/processed", exist_ok=True)
    caminho_saida = "data/processed/chunks_teste.json"
    
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(todos_chunks, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Ingestão concluída! {len(todos_chunks)} chunks regerados com metadados reais e limites seguros.")

if __name__ == "__main__":
    rodar_ingestao_hibrida()
