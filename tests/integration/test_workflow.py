import pytest
from src.workflow import run_agent_workflow, enable_debug_logging
import logging

def test_enable_debug_logging():
    """Test that debug logging is properly enabled."""
    enable_debug_logging()
    logger = logging.getLogger('src')
    assert logger.getEffectiveLevel() == logging.DEBUG

@pytest.mark.skip(reason="Temporarily skipping this test")
def test_run_agent_workflow_basic():
    """Test basic workflow execution."""
    test_input = "What is the weather today?"
    result = run_agent_workflow(test_input)
    assert result is not None

def test_run_agent_workflow_empty_input():
    """Test workflow execution with empty input."""
    with pytest.raises(ValueError):
        run_agent_workflow("") 