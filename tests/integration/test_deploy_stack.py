import os
import shutil
import socket
import subprocess
import time
from pathlib import Path
from urllib.request import urlopen

import pytest


ROOT = Path(__file__).resolve().parents[2]


def _docker_available() -> bool:
    return shutil.which("docker") is not None


def _pick_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _compose(project_name: str, env_file: Path, *args: str) -> subprocess.CompletedProcess[str]:
    command = [
        "docker",
        "compose",
        "--project-name",
        project_name,
        "--env-file",
        str(env_file),
        "-f",
        "docker-compose.yml",
        "-f",
        "docker-compose.production.yml",
        *args,
    ]
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        env={"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", "")},
        check=False,
    )


@pytest.mark.integration
def test_production_stack_serves_healthz_through_nginx(tmp_path):
    if not _docker_available():
        pytest.skip("docker is not available")

    http_port = _pick_free_port()
    project_name = f"smm-assistant-nginx-{http_port}"
    env_file = tmp_path / ".deploy.env"
    env_file.write_text(
        "\n".join(
            [
                "FLASK_ENV=production",
                "FLASK_SECRET_KEY=test-secret-key",
                "POSTGRES_DB=smm_assistant",
                "POSTGRES_USER=smm_assistant",
                "POSTGRES_PASSWORD=test-db-password",
                "DATABASE_URL=postgresql://smm_assistant:test-db-password@postgres:5432/smm_assistant",
                "LOG_LEVEL=INFO",
                "REQUEST_TIMEOUT=30",
                "VK_API_VERSION=5.139",
                "OPENAI_API_KEY=",
                "OPENAI_TEXT_MODEL=gpt-5",
                "OPENAI_IMAGE_MODEL=dall-e-3",
                f"NGINX_HTTP_PORT={http_port}",
                "TRUST_PROXY_COUNT=1",
                "PREFERRED_URL_SCHEME=https",
                "SESSION_COOKIE_SECURE=true",
                "REMEMBER_COOKIE_SECURE=true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    logs_output = ""
    try:
        up_result = _compose(project_name, env_file, "up", "-d", "--build")
        assert up_result.returncode == 0, up_result.stderr or up_result.stdout

        deadline = time.time() + 90
        last_error = None
        while time.time() < deadline:
            try:
                with urlopen(f"http://127.0.0.1:{http_port}/healthz", timeout=5) as response:
                    payload = response.read().decode("utf-8")
                    assert response.status == 200
                    assert '"status":"ok"' in payload
                    assert '"database":{"status":"ok"}' in payload
                    break
            except Exception as exc:  # pragma: no cover - diagnostic path
                last_error = exc
                time.sleep(2)
        else:
            ps_result = _compose(project_name, env_file, "ps")
            logs_result = _compose(project_name, env_file, "logs", "--no-color", "nginx", "web")
            logs_output = (
                "docker compose ps\n"
                + ps_result.stdout
                + "\n\ndocker compose logs\n"
                + logs_result.stdout
                + logs_result.stderr
            )
            raise AssertionError(f"nginx health route did not become ready: {last_error}\n{logs_output}")
    finally:
        down_result = _compose(project_name, env_file, "down", "-v")
        if down_result.returncode != 0 and logs_output:
            raise AssertionError(logs_output)
