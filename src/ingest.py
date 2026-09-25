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
    meta = {
        "natureza": natureza, "uf": "", "ano": "", "modalidade": "",
        "orgao": "", "municipio": "", "valor": "", "fornecedor": "", "vigencia": ""
    }
    
    if dados is None:
        return meta

    if natureza == "estruturada":
        unidade_orgao = dados.get("unidadeOrgao", {}) or {}
        orgao_entidade = dados.get("orgaoEntidade", {}) or {}
        
        meta["uf"] = unidade_orgao.get("ufSigla", "")
        meta["municipio"] = unidade_orgao.get("municipioNome", "")
        meta["orgao"] = orgao_entidade.get("razaoSocial", "")
        meta["ano"] = str(dados.get("anoCompra", ""))
        meta["modalidade"] = dados.get("modalidadeNome", "")
        
        valor_homologado = dados.get("valorTotalHomologado")
        valor_estimado = dados.get("valorTotalEstimado")
        meta["valor"] = valor_homologado if valor_homologado is not None else (valor_estimado if valor_estimado is not None else "")
        
    elif natureza == "agregada":
        meta["orgao"] = dados.get("Órgão", dados.get("Unidade Responsável", dados.get("orgao", "")))
        vigencia = dados.get("Data Desejada", dados.get("data_homologacao", ""))
        meta["vigencia"] = vigencia
        
        ano_val = str(dados.get("Ano", dados.get("ano", "")))
        if not ano_val and vigencia and len(str(vigencia)) >= 4:
            ano_val = str(vigencia)[:4]
            
        # NOVA REGRA: Extrair o ano do ID (ex: "XXXX/2026") se ainda estiver vazio
        if not ano_val:
            for v in dados.values():
                if isinstance(v, str) and "/202" in v:
                    partes = v.split("/")
                    if len(partes) > 1 and len(partes[-1]) >= 4 and partes[-1][:4].isdigit():
                        ano_val = partes[-1][:4]
                        break
                        
        meta["ano"] = ano_val
        meta["uf"] = dados.get("UF", dados.get("uf", "RJ"))
        meta["valor"] = dados.get("Valor Estimado", dados.get("Valor Total Estimado (R$)", dados.get("valor_total_homologado", "")))
        meta["fornecedor"] = dados.get("fornecedor", dados.get("Fornecedor", ""))

    return meta

def fatiar_texto(texto, max_chars=2000, overlap=200):
    chunks_text = []
    start = 0
    text_len = len(texto)
    while start < text_len:
        end = start + max_chars
        bloco = texto[start:end]
        # Tenta quebrar num espaço em branco para não cortar palavras ao meio
        if end < text_len:
            last_space = bloco.rfind(' ')
            if last_space != -1 and last_space > max_chars // 2:
                bloco = texto[start:start+last_space]
                end = start + last_space
        if len(bloco.strip()) > 10:
            chunks_text.append(bloco.strip())
        start = end - overlap
        if start >= text_len or overlap >= (end - start):
            break
    return chunks_text

def processar_estruturada(caminho):
    chunks = []
    if not os.path.exists(caminho): return chunks
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    registros = dados if isinstance(dados, list) else [dados]
    
    for idx, reg in enumerate(registros, 1):
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
    artigos = texto.split("Art. ")
    for idx, art in enumerate(artigos[1:], 1):
        extras = extrair_metadados_especificos("normativa")
        chunks.append(criar_chunk_base(f"Art. {art.strip()}", os.path.basename(caminho), "lei", idx, "base_normativa", "publico", extras))
    return chunks

def processar_agregada(caminho, limit=500):
    chunks = []
    if not os.path.exists(caminho): return chunks
    with open(caminho, "r", encoding="utf-8-sig") as f:
        primeira_linha = f.readline()
        delimitador = ';' if ';' in primeira_linha else ','
        f.seek(0)
        
        reader = csv.DictReader(f, delimiter=delimitador)
        for idx, row in enumerate(reader, 1):
            if idx > limit:
                break
            texto = " | ".join([f"{k}: {v}" for k, v in row.items() if v])
            extras = extrair_metadados_especificos("agregada", row)
            chunks.append(criar_chunk_base(texto, os.path.basename(caminho), "relatorio", idx, "base_agregada", "publico", extras))
    return chunks

def processar_conversacional(caminho):
    chunks = []
    if not os.path.exists(caminho): return chunks
    chunk_idx = 1
    
    if caminho.endswith(".pdf"):
        with open(caminho, "rb") as f:
            reader = pypdf.PdfReader(f)
            # Lê o PDF página a página e aplica o fatiamento em janelas de 2000 caracteres
            for page_num, page in enumerate(reader.pages, 1):
                extract = page.extract_text()
                if extract:
                    blocos = fatiar_texto(extract, max_chars=2000, overlap=200)
                    for bloco in blocos:
                        extras = extrair_metadados_especificos("conversacional")
                        extras["pagina"] = page_num # Requisito de observabilidade cumprido!
                        chunks.append(criar_chunk_base(bloco, os.path.basename(caminho), "ata_reuniao", chunk_idx, "base_conversacional", "restrito", extras))
                        chunk_idx += 1
                        
    elif caminho.endswith(".txt"):
        with open(caminho, "r", encoding="utf-8") as f:
            texto_completo = f.read()
        blocos = fatiar_texto(texto_completo, max_chars=2000, overlap=200)
        for bloco in blocos:
            extras = extrair_metadados_especificos("conversacional")
            chunks.append(criar_chunk_base(bloco, os.path.basename(caminho), "ata_reuniao", chunk_idx, "base_conversacional", "restrito", extras))
            chunk_idx += 1
            
    return chunks

def rodar_ingestao_hibrida():
    print("Iniciando ingestão (Chunks Conversacionais Seguros e Extração de Ano)...")
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
        
    print(f"✅ Ingestão concluída! Total gerado: {len(todos_chunks)} chunks (o número subiu devido ao fatiamento correto dos PDFs!).")

if __name__ == "__main__":
    rodar_ingestao_hibrida()
