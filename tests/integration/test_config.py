import os
import pytest
from pathlib import Path
from unittest.mock import patch
from src.config.loader import load_yaml_config, process_dict
from src.config.env import BASIC_MODEL, REASONING_MODEL, VL_MODEL
from src.llms.llm import (
    get_llm_by_type,
    ChatLiteLLM,
    ChatOpenAI,
    ChatDeepSeek,
    AzureChatOpenAI,
)


@pytest.fixture(autouse=True)
def clear_llm_cache():
    """清空LLM缓存"""
    from src.llms.llm import _llm_cache

    _llm_cache.clear()


@pytest.fixture
def temp_config_file(tmp_path):
    config_content = """
    USE_CONF: true
    BASIC_MODEL:
        model: anthropic/claude-2
        api_key: test-key
        api_base: http://test-base
    REASONING_MODEL:
        model: anthropic/claude-3
        api_key: test-key-2
        api_base: http://test-base-2
    VISION_MODEL:
        model: anthropic/claude-3-vision
        api_key: test-key-3
        api_base: http://test-base-3
    """
    config_file = tmp_path / "test_conf.yaml"
    config_file.write_text(config_content)
    return str(config_file)


def test_load_yaml_config_file_not_exists():
    """测试加载不存在的配置文件"""
    config = load_yaml_config("/non/existent/path.yaml")
    assert config == {}


def test_process_dict_with_env_vars():
    """测试字典中环境变量的处理"""
    os.environ["TEST_VAR"] = "test_value"
    test_dict = {"key1": "$TEST_VAR", "key2": {"nested_key": "$TEST_VAR"}}
    processed = process_dict(test_dict)
    assert processed["key1"] == "test_value"
    assert processed["key2"]["nested_key"] == "test_value"


@patch("src.llms.llm.ChatLiteLLM")
def test_get_llm_by_type_with_conf(mock_litellm):
    """测试使用配置文件创建LLM实例"""
    # 配置mock对象
    mock_instance = ChatLiteLLM(
        model="anthropic/claude-2", api_key="test-key", api_base="http://test-base"
    )
    mock_litellm.return_value = mock_instance

    with patch("src.llms.llm.load_yaml_config") as mock_load_config:
        mock_load_config.return_value = {
            "USE_CONF": True,
            "BASIC_MODEL": {
                "model": "anthropic/claude-2",
                "api_key": "test-key",
                "api_base": "http://test-base",
            },
        }
        llm = get_llm_by_type("basic")
        assert isinstance(llm, ChatLiteLLM)
        mock_litellm.assert_called_once_with(
            model="anthropic/claude-2", api_key="test-key", api_base="http://test-base"
        )


@patch("src.llms.llm.BASIC_AZURE_DEPLOYMENT", "")
@patch("src.llms.llm.VL_AZURE_DEPLOYMENT", "")
@patch("src.llms.llm.REASONING_AZURE_DEPLOYMENT", "")
@patch("src.llms.llm.BASIC_MODEL", "gpt-4o")
def test_get_llm_by_type_with_env():
    """测试使用环境变量创建LLM实例"""
    with patch("src.llms.llm.load_yaml_config") as mock_load_config:
        mock_load_config.return_value = {"USE_CONF": False}
        llm = get_llm_by_type("basic")
        assert isinstance(llm, ChatOpenAI)


@patch("src.llms.llm.BASIC_AZURE_DEPLOYMENT", "")
@patch("src.llms.llm.VL_AZURE_DEPLOYMENT", "")
@patch("src.llms.llm.REASONING_AZURE_DEPLOYMENT", "")
@patch("src.llms.llm.REASONING_MODEL", "deepseek-chat")
def test_get_llm_by_type_deepseek():
    """测试创建DeepSeek LLM实例"""
    with patch("src.llms.llm.load_yaml_config") as mock_load_config:
        mock_load_config.return_value = {"USE_CONF": False}
        llm = get_llm_by_type("reasoning")
        assert isinstance(llm, ChatDeepSeek)


@patch("src.llms.llm.BASIC_AZURE_DEPLOYMENT", "")
@patch("src.llms.llm.VL_AZURE_DEPLOYMENT", "")
@patch("src.llms.llm.REASONING_AZURE_DEPLOYMENT", "")
@patch("src.llms.llm.REASONING_MODEL", "deepseek/deepseek-chat")
def test_get_llm_by_type_litellm():
    """测试创建LiteLLM llm实例"""
    with patch("src.llms.llm.load_yaml_config") as mock_load_config:
        mock_load_config.return_value = {"USE_CONF": False}
        llm = get_llm_by_type("reasoning")
        assert isinstance(llm, ChatLiteLLM)


@patch("src.llms.llm.BASIC_AZURE_DEPLOYMENT", "gpt-4")
@patch("src.llms.llm.AZURE_API_KEY", "test-key")
@patch("src.llms.llm.AZURE_API_BASE", "http://xxxxx")
@patch("src.llms.llm.AZURE_API_VERSION", "2025-03-23")
def test_get_llm_by_type_azure():
    """测试创建Azure LLM实例"""
    with patch("src.llms.llm.load_yaml_config") as mock_load_config:
        mock_load_config.return_value = {"USE_CONF": False}
        llm = get_llm_by_type("basic")
        assert isinstance(llm, AzureChatOpenAI)
