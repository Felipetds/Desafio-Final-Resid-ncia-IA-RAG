"""Testes offline para repositorio1/src/generate.py."""

"""
teste_generate.py

Testes offline para repositorio1/src/generate.py.
"""

from types import SimpleNamespace

from repositorio1.src.generate import (
    calcular_confianca,
    gerar_resposta,
    mascarar_dados_pessoais,
    montar_contexto,
)

from repositorio1.src.schema import (
    QueryFilters,
    RetrievalResult,
    SourceEvidence,
)


def criar_evidencia(chunk_id="chunk_001", source_file="contratos_2025.csv", texto=None):
    if texto is None:
        texto = (
            "Em 2025, a empresa Exemplo Tecnologia Ltda., "
            "CNPJ 12.345.678/0001-90, celebrou contrato "
            "no valor de R$ 650.000,00."
        )

    return SourceEvidence(
        chunk_id=chunk_id,
        text=texto,
        rrf_score=0.0325,
        retrieval_sources=["dense", "bm25"],
        source_file=source_file,
        doc_type="contratacao",
        sensitivity="publico",
        base_id="estruturada_pncp_rj",
        natureza="estruturada",
        metadata={"uf": "RJ", "ano": 2025, "valor": 650000},
    )


def criar_retrieval(evidences=None, is_refusal=False, refusal_reason=None):
    return RetrievalResult(
        query="Quais contratos de tecnologia ficaram acima de R$ 500 mil em 2025?",
        query_id="q_generate_001",
        routes=["estruturada"],
        filters=QueryFilters(uf="RJ", ano=2025, valor_minimo=500000),
        is_refusal=is_refusal,
        refusal_reason=refusal_reason,
        evidences=evidences or [],
    )


class FakeCompletions:
    def __init__(self, conteudo, prompt=100, completion=30, total=130, erro=None):
        self.conteudo = conteudo
        self.prompt = prompt
        self.completion = completion
        self.total = total
        self.erro = erro

    def create(self, **kwargs):
        if self.erro:
            raise self.erro
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self.conteudo))],
            usage=SimpleNamespace(
                prompt_tokens=self.prompt,
                completion_tokens=self.completion,
                total_tokens=self.total,
            ),
        )


class FakeClient:
    def __init__(self, conteudo, prompt=100, completion=30, total=130, erro=None):
        self.chat = SimpleNamespace(
            completions=FakeCompletions(conteudo, prompt, completion, total, erro)
        )


def instalar_llm_falso(monkeypatch, cliente):
    monkeypatch.setattr(
        "repositorio1.src.generate.OpenAI",
        lambda **kwargs: cliente,
    )


def test_montar_contexto():
    contexto = montar_contexto([criar_evidencia()])
    assert "EVIDÊNCIA 1" in contexto
    assert "contratos_2025.csv" in contexto
    assert "chunk_001" in contexto
    assert "Exemplo Tecnologia Ltda." in contexto


def test_confianca_baixa():
    assert calcular_confianca([criar_evidencia()]) == "baixa"


def test_confianca_media():
    evidencias = [
        criar_evidencia("chunk_001", "arquivo_a.csv"),
        criar_evidencia("chunk_002", "arquivo_a.csv"),
    ]
    assert calcular_confianca(evidencias) == "media"


def test_confianca_alta():
    evidencias = [
        criar_evidencia("chunk_001", "arquivo_a.csv"),
        criar_evidencia("chunk_002", "arquivo_a.csv"),
        criar_evidencia("chunk_003", "arquivo_b.csv"),
    ]
    assert calcular_confianca(evidencias) == "alta"


def test_mascarar_cpf():
    resultado = mascarar_dados_pessoais("CPF 123.456.789-00")
    assert "123.456.789-00" not in resultado


def test_mascarar_email():
    resultado = mascarar_dados_pessoais("E-mail joao.silva@email.com")
    assert "joao.silva@email.com" not in resultado


def test_mascarar_telefone():
    resultado = mascarar_dados_pessoais("Telefone (21) 99999-8888")
    assert "(21) 99999-8888" not in resultado


def test_preservar_cnpj():
    resultado = mascarar_dados_pessoais("CNPJ 12.345.678/0001-90")
    assert "12.345.678/0001-90" in resultado


def test_geracao_normal(monkeypatch):
    retrieval = criar_retrieval([criar_evidencia()])
    cliente = FakeClient(
        "Foi encontrado contrato da Exemplo Tecnologia Ltda., "
        "CNPJ 12.345.678/0001-90, no valor de R$ 650.000,00 "
        "[Fonte: contratos_2025.csv].",
        prompt=120,
        completion=40,
        total=160,
    )
    instalar_llm_falso(monkeypatch, cliente)

    resposta = gerar_resposta(retrieval)

    assert resposta.is_refusal is False
    assert "Exemplo Tecnologia Ltda." in resposta.answer
    assert resposta.confidence_level == "baixa"
    assert len(resposta.sources_used) == 1
    assert resposta.tokens.prompt == 120
    assert resposta.tokens.completion == 40
    assert resposta.tokens.total == 160


def test_guardrail_na_resposta(monkeypatch):
    retrieval = criar_retrieval([criar_evidencia()])
    cliente = FakeClient(
        "CPF 123.456.789-00, telefone (21) 99999-8888, "
        "e-mail joao@email.com."
    )
    instalar_llm_falso(monkeypatch, cliente)

    resposta = gerar_resposta(retrieval)

    assert "123.456.789-00" not in resposta.answer
    assert "(21) 99999-8888" not in resposta.answer
    assert "joao@email.com" not in resposta.answer


def test_cnpj_preservado_na_resposta(monkeypatch):
    retrieval = criar_retrieval([criar_evidencia()])
    cliente = FakeClient("Fornecedor CNPJ 12.345.678/0001-90.")
    instalar_llm_falso(monkeypatch, cliente)

    resposta = gerar_resposta(retrieval)
    assert "12.345.678/0001-90" in resposta.answer


def test_recusa_nao_chama_llm(monkeypatch):
    retrieval = criar_retrieval(
        [],
        is_refusal=True,
        refusal_reason="Solicitação envolve dados sensíveis.",
    )

    def nao_deve_chamar(**kwargs):
        raise AssertionError("LLM não deveria ser chamado.")

    monkeypatch.setattr("repositorio1.src.generate.OpenAI", nao_deve_chamar)

    resposta = gerar_resposta(retrieval)

    assert resposta.is_refusal is True
    assert resposta.sources_used == []
    assert resposta.refusal_reason == "Solicitação envolve dados sensíveis."


def test_sem_evidencias_nao_chama_llm(monkeypatch):
    retrieval = criar_retrieval([])

    def nao_deve_chamar(**kwargs):
        raise AssertionError("LLM não deveria ser chamado.")

    monkeypatch.setattr("repositorio1.src.generate.OpenAI", nao_deve_chamar)

    resposta = gerar_resposta(retrieval)

    assert resposta.is_refusal is False
    assert resposta.confidence_level == "baixa"
    assert resposta.sources_used == []
    assert "informações suficientes" in resposta.answer.lower()


def test_falha_do_llm(monkeypatch):
    retrieval = criar_retrieval([criar_evidencia()])
    cliente = FakeClient("", erro=RuntimeError("Falha simulada"))
    instalar_llm_falso(monkeypatch, cliente)

    resposta = gerar_resposta(retrieval)

    assert resposta.is_refusal is False
    assert resposta.confidence_level == "baixa"
    assert resposta.sources_used == []


def test_resposta_vazia_do_llm(monkeypatch):
    retrieval = criar_retrieval([criar_evidencia()])
    instalar_llm_falso(monkeypatch, FakeClient("   "))

    resposta = gerar_resposta(retrieval)

    assert resposta.is_refusal is False
    assert resposta.confidence_level == "baixa"
    assert resposta.sources_used == []


def test_aceita_retrieval_como_dict(monkeypatch):
    retrieval = criar_retrieval([criar_evidencia()]).model_dump()
    instalar_llm_falso(
        monkeypatch,
        FakeClient("Contrato encontrado [Fonte: contratos_2025.csv]."),
    )

    resposta = gerar_resposta(retrieval)

    assert resposta.query_id == "q_generate_001"
    assert resposta.is_refusal is False
    assert len(resposta.sources_used) == 1
