import os
import pytest
from unittest.mock import patch, MagicMock


def reload_config():
    from importlib import reload
    import src.config
    return reload(src.config)


def test_config_loads_api_key():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        config = reload_config()
        assert config.llm is not None


def test_config_missing_api_key():
    with patch.dict(os.environ, {}, clear=True):
        os.environ.pop("OPENAI_API_KEY", None)
        with pytest.raises(ValueError, match="LLM_API_KEY not set"):
            reload_config()


def test_config_custom_model_from_env():
    env = {
        "LLM_MODEL": "openrouter/meta-llama/llama-3.3-70b-instruct:free",
        "LLM_API_KEY": "test-key",
    }
    with patch.dict(os.environ, env, clear=True):
        config = reload_config()
        assert "llama-3.3-70b-instruct:free" in config.llm.model


def test_config_keyless_ollama_allowed():
    with patch.dict(os.environ, {"LLM_MODEL": "ollama/qwen2.5"}, clear=True):
        config = reload_config()
        assert "qwen2.5" in config.llm.model


def test_config_keyless_base_url_allowed():
    with patch.dict(os.environ, {"LLM_BASE_URL": "http://localhost:8080/v1"}, clear=True):
        config = reload_config()
        assert config.llm.base_url == "http://localhost:8080/v1"


def test_config_temperature_override():
    env = {"OPENAI_API_KEY": "test-key", "LLM_TEMPERATURE": "0.2"}
    with patch.dict(os.environ, env, clear=True):
        config = reload_config()
        assert config.llm.temperature == 0.2


def test_config_defaults_reproduce_legacy_behavior():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=True):
        config = reload_config()
        assert config.llm.model == "gpt-4o-mini"
        assert config.llm.temperature == 0.7
        assert config.llm.api_key == "test-key"


def test_create_writer_agent():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        from src.agents import create_writer_agent
        agent = create_writer_agent()
        assert agent.role == "Publication Writer"
        assert "publication-ready text" in agent.goal.lower()


def test_create_writing_task():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        from src.agents import create_writer_agent
        from src.tasks import create_writing_task
        agent = create_writer_agent()
        task = create_writing_task(agent, "AI agents")
        assert "AI agents" in task.description
        assert "<p>" in task.expected_output
        assert task.agent == agent


def test_crew_instantiation():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        from src.crew import PostPublisherCrew
        crew = PostPublisherCrew(tip="Climate change")
        assert crew.tip == "Climate change"
        assert crew.language == "English"


def test_crew_empty_tip_raises():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        from src.crew import PostPublisherCrew
        with pytest.raises(ValueError, match="Tip cannot be empty"):
            PostPublisherCrew(tip="")


def test_crew_kickoff_mocked():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        from src.crew import PostPublisherCrew
        with patch("src.crew.Crew") as MockCrew:
            mock_instance = MagicMock()
            mock_instance.kickoff.return_value = "Article about AI agents in <p> tags"
            MockCrew.return_value = mock_instance

            crew = PostPublisherCrew(tip="AI agents")
            result = crew.run()

            assert result == "Article about AI agents in <p> tags"
            assert "AI agents" in result
            MockCrew.assert_called_once()
