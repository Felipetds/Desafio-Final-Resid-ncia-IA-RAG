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

def processar_estruturada(caminho):
    chunks = []
    if not os.path.exists(caminho): return chunks
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    registros = dados if isinstance(dados, list) else [dados]
    for idx, reg in enumerate(registros, 1):
        texto = json.dumps(reg, ensure_ascii=False)
        extras = {"natureza": "estruturada"}
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
        extras = {"natureza": "normativa"}
        chunks.append(criar_chunk_base(f"Art. {art.strip()}", os.path.basename(caminho), "lei", idx, "base_normativa", "publico", extras))
    return chunks

def processar_agregada(caminho, limit=500):
    # LIMIT_DEV: Limita o processamento a N linhas para acelerar testes de UI
    # O arquivo CSV original permanece intacto. Remover o limit na prod.
    chunks = []
    if not os.path.exists(caminho): return chunks
    with open(caminho, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            if idx > limit:
                break
            texto = " | ".join([f"{k}: {v}" for k, v in row.items() if v])
            extras = {"natureza": "agregada"}
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
            
    paragrafos = [p.strip() for p in texto_completo.split("\n\n") if len(p.strip()) > 10]
    for idx, p in enumerate(paragrafos, 1):
        extras = {"natureza": "conversacional"}
        chunks.append(criar_chunk_base(p, os.path.basename(caminho), "ata_reuniao", idx, "base_conversacional", "restrito", extras))
    return chunks

def rodar_ingestao_hibrida():
    print("Iniciando ingestão (Modo Desenvolvimento - Amostra 500 records na Agregada)...")
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
        # APLICADO O LIMITE APENAS NA BASE AGREGADA CONFORME SOLICITADO PELA GERENCIA
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
        
    print(f"✅ Ingestão concluída! {len(todos_chunks)} chunks gerados para desenvolvimento.")

if __name__ == "__main__":
    rodar_ingestao_hibrida()
