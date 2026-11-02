from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_token_counts_and_returns_response(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=3),
    )
    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=lambda **kwargs: response)
    )
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", lambda **kwargs: client)

    result = ask_module.ask("質問")

    assert result == "回答"
    assert "入力: 12 / 出力: 3" in capsys.readouterr().out


def test_ask_handles_missing_usage_metadata(monkeypatch, capsys):
    response = SimpleNamespace(text="回答", usage_metadata=None)
    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=lambda **kwargs: response)
    )
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", lambda **kwargs: client)

    ask_module.ask("質問")

    assert "入力: 不明 / 出力: 不明" in capsys.readouterr().out