import os
import json

def criar_chunk(texto, source_file, doc_type, chunk_idx, base_id="estruturada_pncp_rj"):
    return {
        "text": texto,
        "metadata": {
            "chunk_id": f"{source_file}_chunk_{chunk_idx}",
            "source_file": source_file,
            "doc_type": doc_type,
            "sensitivity": "publico",
            "base_id": base_id
        }
    }

def processar_fixtures():
    print("Iniciando a ingestão (Modo Fixture/Teste)...")
    
    texto_simulado = "O GOVERNO DO ESTADO DO RIO DE JANEIRO torna público a realização de licitação na modalidade Pregão Eletrônico. O objeto desta licitação é a contratação de serviços de tecnologia."
    pedacos = texto_simulado.split(". ")
    
    documentos_processados = []
    for idx, pedaco in enumerate(pedacos):
        if pedaco.strip():
            chunk = criar_chunk(
                texto=pedaco.strip() + ".",
                source_file="edital_pregao_01_2026.pdf",
                doc_type="edital",
                chunk_idx=idx
            )
            documentos_processados.append(chunk)
            
    os.makedirs("data/processed", exist_ok=True)
    caminho_saida = "data/processed/chunks_teste.json"
    
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(documentos_processados, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Ingestão concluída! {len(documentos_processados)} chunks gerados em {caminho_saida}")

if __name__ == "__main__":
    processar_fixtures()
