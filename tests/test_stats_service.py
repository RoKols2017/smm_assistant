from unittest.mock import MagicMock

from app.services.stats_service import StatsService


def test_stats_service_returns_message_when_vk_settings_missing_fields():
    user = MagicMock()
    user.id = 1
    user.vk_settings = MagicMock(vk_api_key="", vk_group_id=None)

    result = StatsService().get_vk_stats_for_user(user)

    assert result.group_name is None
    assert result.members_count is None
    assert result.validation_message == "VK settings заполнены не полностью."


def test_stats_service_uses_members_count_fallback_when_group_info_has_no_count(mocker):
    user = MagicMock()
    user.id = 1
    user.vk_settings = MagicMock(
        vk_api_key="test-valid-token",
        vk_group_id=123456,
        validation_message="ok",
    )

    service = StatsService()
    mocker.patch.object(service.vk_service, "get_group_info", return_value={"name": "Test Group"})
    extract_members_count = mocker.patch.object(service.vk_service, "extract_members_count", return_value=321)

    result = service.get_vk_stats_for_user(user)

    extract_members_count.assert_called_once_with(
        payload={"name": "Test Group"},
        fallback_group_id=123456,
        token="test-valid-token",
    )
    assert result.group_name == "Test Group"
    assert result.members_count == 321
    assert result.validation_message == "ok"
