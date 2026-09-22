import os
import json

def criar_chunk_base(texto, source_file, doc_type, chunk_idx, base_id, sensitivity, extras):
    # Mantém os metadados obrigatórios do contrato do projeto
    metadata = {
        "chunk_id": f"{source_file}_chunk_{chunk_idx}",
        "source_file": source_file,
        "doc_type": doc_type,
        "sensitivity": sensitivity,
        "base_id": base_id
    }
    # Adiciona os metadados específicos da natureza do dado
    metadata.update(extras)
    
    return {
        "text": texto,
        "metadata": metadata
    }

def processar_normativa(texto, arquivo):
    # Checklist: seção, artigo ou cláusula com overlap
    chunks = []
    artigos = texto.split("Art. ")
    for idx, art in enumerate(artigos[1:], 1): # Pula o índice 0 (cabeçalho antes do primeiro artigo)
        extras = {"natureza": "normativa", "orgao": "Governo Estadual"}
        chunks.append(criar_chunk_base(f"Art. {art.strip()}", arquivo, "lei", idx, "base_normativa", "publico", extras))
    return chunks

def processar_estruturada(registro, arquivo, idx):
    # Checklist: um registro completo por chunk
    texto = json.dumps(registro, ensure_ascii=False)
    extras = {
        "natureza": "estruturada",
        "uf": registro.get("uf", ""),
        "ano": registro.get("ano", ""),
        "modalidade": registro.get("modalidade", ""),
        "valor": registro.get("valor", ""),
        "fornecedor": registro.get("fornecedor", ""),
        "vigencia": registro.get("vigencia", "")
    }
    return criar_chunk_base(texto, arquivo, "contrato", idx, "base_estruturada", "publico", extras)

def processar_conversacional(mensagem, arquivo, idx, sensibilidade="restrito"):
    # Checklist: mensagens/atas com sensibilidade
    extras = {"natureza": "conversacional"}
    return criar_chunk_base(mensagem, arquivo, "ata_reuniao", idx, "base_conversacional", sensibilidade, extras)

def processar_agregada(dado, arquivo, idx):
    # Checklist: número com unidade, período e recorte
    texto = f"Resultado: {dado['valor']} {dado['unidade']} registradas no período de {dado['periodo']} para o recorte de {dado['recorte']}."
    extras = {
        "natureza": "agregada",
        "municipio": dado.get("municipio", "")
    }
    return criar_chunk_base(texto, arquivo, "relatorio", idx, "base_agregada", "publico", extras)

def rodar_ingestao_hibrida():
    print("Iniciando ingestão adaptada para as 4 bases (Regras do Checklist)...")
    todos_chunks = []
    
    # 1. Teste Normativa
    texto_norma = "Preâmbulo da lei. Art. 1 O pipeline RAG será implementado imediatamente. Art. 2 Os dados sensíveis devem ser anonimizados antes da indexação."
    todos_chunks.extend(processar_normativa(texto_norma, "lei_rag_2026.txt"))
    
    # 2. Teste Estruturada
    registro = {"uf": "RJ", "ano": "2026", "modalidade": "Pregao Eletronico", "valor": "R$ 150.000", "fornecedor": "Tech Solucoes LTDA", "vigencia": "12 meses"}
    todos_chunks.append(processar_estruturada(registro, "compras_rj_marco.json", 1))
    
    # 3. Teste Conversacional
    todos_chunks.append(processar_conversacional("Discussão técnica: Acesso ao banco de dados PNCP concedido ao usuário administrador.", "log_reuniao_01.txt", 1, "sigiloso"))
    
    # 4. Teste Agregada
    dado_agg = {"valor": "345", "unidade": "licitações", "periodo": "1º trimestre de 2026", "recorte": "Serviços de TI", "municipio": "Rio de Janeiro"}
    todos_chunks.append(processar_agregada(dado_agg, "indicadores_trimestrais.json", 1))

    os.makedirs("data/processed", exist_ok=True)
    caminho_saida = "data/processed/chunks_teste.json"
    
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(todos_chunks, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Ingestão concluída! {len(todos_chunks)} chunks gerados englobando as 4 naturezas exigidas.")

if __name__ == "__main__":
    rodar_ingestao_hibrida()

# Redefinir apenas a função principal para carregar o JSON real
def rodar_ingestao_hibrida():
    print("Iniciando ingestão (Base Estruturada REAL + Fixtures para o resto)...")
    todos_chunks = []
    
    # 1. Base Estruturada (AGORA COM OS 1358 DADOS REAIS!)
    caminho_real = "data/raw/v1/estruturada/pncp/rj/pregao_eletronico/2026-03/contratacoes_publicacao.json"
    if os.path.exists(caminho_real):
        with open(caminho_real, "r", encoding="utf-8") as f:
            dados_reais = json.load(f)
            # O PNCP geralmente agrupa os dados numa lista
            registros = dados_reais if isinstance(dados_reais, list) else [dados_reais]
            
            print(f"Extraindo {len(registros)} registros estruturados do PNCP...")
            for idx, reg in enumerate(registros, 1):
                todos_chunks.append(processar_estruturada(reg, "contratacoes_publicacao.json", idx))
    else:
        print("⚠️ Erro: Arquivo estruturado real não encontrado.")

    # 2. Teste Normativa (Fixture mantida até entrega da Janice)
    texto_norma = "Preâmbulo da lei. Art. 1 O pipeline RAG será implementado imediatamente. Art. 2 Os dados sensíveis devem ser anonimizados."
    todos_chunks.extend(processar_normativa(texto_norma, "lei_rag_2026.txt"))
    
    # 3. Teste Conversacional (Fixture mantida)
    todos_chunks.append(processar_conversacional("Discussão técnica: Acesso ao PNCP concedido.", "log_reuniao_01.txt", 1, "sigiloso"))
    
    # 4. Teste Agregada (Fixture mantida)
    dado_agg = {"valor": "345", "unidade": "licitações", "periodo": "1º trimestre de 2026", "recorte": "Serviços de TI", "municipio": "Rio de Janeiro"}
    todos_chunks.append(processar_agregada(dado_agg, "indicadores_trimestrais.json", 1))

    os.makedirs("data/processed", exist_ok=True)
    caminho_saida = "data/processed/chunks_teste.json"
    
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(todos_chunks, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Ingestão concluída! {len(todos_chunks)} chunks gerados.")

if __name__ == "__main__":
    rodar_ingestao_hibrida()
