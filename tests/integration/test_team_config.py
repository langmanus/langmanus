import pytest
from src.config import TEAM_MEMBER_CONFIGRATIONS, TEAM_MEMBERS
from src.prompts.template import get_prompt_template, apply_prompt_template


def test_team_member_config_structure():
    """Test the structure of team member configurations"""
    required_keys = {"name", "desc", "desc_for_llm", "is_optional"}

    for member in TEAM_MEMBERS:
        config = TEAM_MEMBER_CONFIGRATIONS[member]
        # 检查所有必需的键是否存在
        assert all(key in config for key in required_keys)
        # 检查值的类型
        assert isinstance(config["name"], str)
        assert isinstance(config["desc"], str)
        assert isinstance(config["desc_for_llm"], str)
        assert isinstance(config["is_optional"], bool)


def test_desc_for_llm_content():
    """Test the content of desc_for_llm for each team member"""
    # 测试每个成员的 desc_for_llm 是否包含必要的关键信息
    researcher_desc = TEAM_MEMBER_CONFIGRATIONS["researcher"]["desc_for_llm"]
    assert "search engines" in researcher_desc.lower()
    assert "web crawlers" in researcher_desc.lower()

    coder_desc = TEAM_MEMBER_CONFIGRATIONS["coder"]["desc_for_llm"]
    assert "python" in coder_desc.lower() or "bash" in coder_desc.lower()
    assert "mathematical" in coder_desc.lower()

    browser_desc = TEAM_MEMBER_CONFIGRATIONS["browser"]["desc_for_llm"]
    assert "web pages" in browser_desc.lower()
    assert "interactions" in browser_desc.lower()

    reporter_desc = TEAM_MEMBER_CONFIGRATIONS["reporter"]["desc_for_llm"]
    assert "report" in reporter_desc.lower()


def test_template_desc_for_llm_rendering():
    """Test the rendering of desc_for_llm in templates"""
    test_state = {
        "TEAM_MEMBERS": TEAM_MEMBERS,
        "TEAM_MEMBER_CONFIGRATIONS": TEAM_MEMBER_CONFIGRATIONS,
        "messages": [{"role": "user", "content": "test message"}],
        "task": "test task",
        "workspace_context": "test context",
    }

    # 测试 planner 模板
    planner_messages = apply_prompt_template("planner", test_state)
    planner_content = planner_messages[0]["content"]

    # 检查是否所有成员的 desc_for_llm 都被正确渲染到模板中
    for member in TEAM_MEMBERS:
        desc = TEAM_MEMBER_CONFIGRATIONS[member]["desc_for_llm"]
        assert desc in planner_content

    # 测试 supervisor 模板
    supervisor_messages = apply_prompt_template("supervisor", test_state)
    supervisor_content = supervisor_messages[0]["content"]

    # 检查是否所有成员的 desc_for_llm 都被正确渲染到模板中
    for member in TEAM_MEMBERS:
        desc = TEAM_MEMBER_CONFIGRATIONS[member]["desc_for_llm"]
        assert desc in supervisor_content


@pytest.mark.parametrize("template_name", ["planner", "supervisor"])
def test_template_format_after_desc_for_llm(template_name):
    """Test the template format remains correct after desc_for_llm integration"""
    test_state = {
        "TEAM_MEMBERS": TEAM_MEMBERS,
        "TEAM_MEMBER_CONFIGRATIONS": TEAM_MEMBER_CONFIGRATIONS,
        "messages": [{"role": "user", "content": "test message"}],
        "task": "test task",
        "workspace_context": "test context",
    }

    messages = apply_prompt_template(template_name, test_state)
    content = messages[0]["content"]

    # 检查基本格式是否保持正确
    assert "---" in content  # 检查 frontmatter
    assert "CURRENT_TIME:" in content

    # 检查团队成员列表格式
    for member in TEAM_MEMBERS:
        assert f"**`{member}`**:" in content  # 检查成员标题格式
