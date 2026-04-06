from unittest.mock import patch

import pytest

from app.extensions import db
from app.models.generated_post import GeneratedPost
from app.models.user import User
from app.services.content_workflow import ContentWorkflowService


def register_and_login(client):
    client.post(
        "/auth/register",
        data={
            "email": "content@example.com",
            "password": "supersecret123",
            "confirm_password": "supersecret123",
        },
        follow_redirects=True,
    )


def test_content_generation_without_vk_autopost(client, app):
    register_and_login(client)

    with patch("app.services.openai_service.TextGenerator.generate_post", return_value="Generated text"), \
         patch("app.services.openai_service.ImageGenerator.generate_image", return_value="https://example.com/image.png"):
        response = client.post(
            "/content/generate",
            data={
                "tone": "friendly",
                "topic": "AI tools",
                "generate_image": "y",
            },
            follow_redirects=True,
        )

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Контент успешно сгенерирован" in body
    assert "Generated text" in body


def test_content_generation_gracefully_handles_vk_failure(client):
    register_and_login(client)
    with patch("app.settings.routes.VKCapabilityService.validate") as mock_validate:
        mock_validate.return_value.validation_status = "validated"
        mock_validate.return_value.validation_message = "ok"
        mock_validate.return_value.can_access_group = True
        mock_validate.return_value.can_post_to_wall = None
        mock_validate.return_value.can_upload_wall_photo = None

        client.post(
            "/settings/",
            data={"vk_api_key": "test-valid-vk-token", "vk_group_id": "123456"},
            follow_redirects=True,
        )

    with patch("app.services.openai_service.TextGenerator.generate_post", return_value="Generated text"), \
         patch("app.services.vk_service.VKPublisher.publish_post", return_value=None):
        response = client.post(
            "/content/generate",
            data={
                "tone": "friendly",
                "topic": "AI tools",
                "auto_post_vk": "y",
            },
            follow_redirects=True,
        )

    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Контент успешно сгенерирован, но автопостинг в VK не выполнен" in body


def test_content_workflow_rolls_back_session_when_commit_fails(app, mocker):
    with app.app_context():
        user = User(email="workflow@example.com", password_hash="hashed")
        db.session.add(user)
        db.session.commit()

        service = ContentWorkflowService()
        mocker.patch.object(service.openai_service, "generate_post", return_value="Generated text")
        rollback = mocker.spy(db.session, "rollback")
        mocker.patch.object(db.session, "commit", side_effect=RuntimeError("db is down"))

        with pytest.raises(RuntimeError, match="db is down"):
            service.generate_for_user(
                user=user,
                tone="friendly",
                topic="AI tools",
                generate_image=False,
                auto_post_vk=False,
            )

        rollback.assert_called_once()
        assert GeneratedPost.query.count() == 0
