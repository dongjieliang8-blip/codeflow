"""Basic smoke tests for CodeFlow modules."""

import tempfile
import os
from pathlib import Path


def test_collect_source_files():
    from src.utils import collect_source_files

    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "test.py").write_text("print('hello')\n")
        Path(tmp, "ignore.txt").write_text("not code")
        Path(tmp, ".git").mkdir()

        files = collect_source_files(tmp)
        paths = [f["path"] for f in files]
        assert "test.py" in paths
        assert "ignore.txt" not in paths


def test_llm_config_from_env():
    from src.llm.client import LLMConfig

    config = LLMConfig.from_env()
    assert config.model == "deepseek-chat"
    assert "deepseek" in config.base_url


def test_format_files_for_prompt():
    from src.utils import format_files_for_prompt

    files = [{
        "path": "a.py",
        "lines": 2,
        "content": "x = 1\ny = 2",
    }]
    result = format_files_for_prompt(files)
    assert "a.py" in result
    assert "x = 1" in result


def test_pipeline_imports():
    from src.pipeline import Pipeline
    from src.agents import scanner, architect, executor, reviewer
    assert Pipeline is not None
    assert scanner.SYSTEM_PROMPT
    assert architect.SYSTEM_PROMPT
    assert executor.SYSTEM_PROMPT
    assert reviewer.SYSTEM_PROMPT
