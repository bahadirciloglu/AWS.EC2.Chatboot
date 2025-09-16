import os
import pytest

PROMPTS_DIR = "data/prompts"
CONTEXT_PATH = "data/context.md"

def test_prompts_exist():
    prompt_files = [f for f in os.listdir(PROMPTS_DIR) if f.endswith(".txt") or f.endswith(".json")]
    assert len(prompt_files) > 0, "Prompt dizininde hiç dosya yok!"
    for fname in prompt_files:
        with open(os.path.join(PROMPTS_DIR, fname), "r", encoding="utf-8") as f:
            content = f.read().strip()
            assert content, f"{fname} dosyası boş!"

def test_context_exists():
    assert os.path.exists(CONTEXT_PATH), "context.md dosyası yok!"
    with open(CONTEXT_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()
        assert content, "context.md dosyası boş!"

def test_prompt_context_merge():
    prompt_files = [f for f in os.listdir(PROMPTS_DIR) if f.endswith(".txt") or f.endswith(".json")]
    with open(CONTEXT_PATH, "r", encoding="utf-8") as f:
        context = f.read().strip()
    for fname in prompt_files:
        with open(os.path.join(PROMPTS_DIR, fname), "r", encoding="utf-8") as f:
            prompt = f.read().strip()
            merged = f"{prompt}\n\nEk Bağlam:\n{context}"
            assert prompt in merged
            assert context in merged
            assert "Ek Bağlam:" in merged 