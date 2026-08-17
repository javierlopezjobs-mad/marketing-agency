import os
import pytest
from unittest.mock import patch, MagicMock


def test_config_loads_api_key():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        from src.config import llm
        assert llm is not None


def test_config_missing_api_key():
    with patch.dict(os.environ, {}, clear=True):
        os.environ.pop("OPENAI_API_KEY", None)
        with pytest.raises(ValueError, match="OPENAI_API_KEY not set"):
            from importlib import reload
            import src.config
            reload(src.config)


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
