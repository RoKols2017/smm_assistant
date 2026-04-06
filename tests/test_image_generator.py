"""
Тесты для генератора изображений
"""

import pytest
import httpx
from unittest.mock import patch, MagicMock
from generators.image_gen import ImageGenerator


def make_authentication_error(message="Auth failed"):
    request = httpx.Request("POST", "https://api.openai.com/v1/images/generations")
    response = httpx.Response(401, request=request)
    from openai import AuthenticationError
    return AuthenticationError(message, response=response, body=None)


def make_rate_limit_error(message="Rate limit exceeded"):
    request = httpx.Request("POST", "https://api.openai.com/v1/images/generations")
    response = httpx.Response(429, request=request)
    from openai import RateLimitError
    return RateLimitError(message, response=response, body=None)


def make_bad_request_error(message="Bad request"):
    request = httpx.Request("POST", "https://api.openai.com/v1/images/generations")
    response = httpx.Response(400, request=request)
    from openai import BadRequestError
    return BadRequestError(message, response=response, body=None)


def make_api_error(message="API error"):
    request = httpx.Request("POST", "https://api.openai.com/v1/images/generations")
    from openai import APIError
    return APIError(message, request=request, body=None)


class TestImageGenerator:
    """Тесты для класса ImageGenerator"""
    
    def test_init_success(self):
        """Тест успешной инициализации"""
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator(model="dall-e-3")
            
            assert generator.model == "dall-e-3"
    
    def test_init_default_model(self):
        """Тест модели по умолчанию"""
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator()
            
            assert generator.model == "dall-e-3"
    
    def test_init_model_validation(self):
        """Тест валидации модели"""
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            # Валидная модель
            generator = ImageGenerator(model="dall-e-3")
            assert generator.model == "dall-e-3"
            
            # Невалидная модель (должно вызвать предупреждение)
            with patch('generators.image_gen.logger') as mock_logger:
                ImageGenerator(model="invalid-model")
                mock_logger.warning.assert_called_once()
    
    def test_generate_image_empty_prompt(self):
        """Тест генерации с пустым промптом"""
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator()
            
            result = generator.generate_image("")
            
            assert result is None
    
    def test_generate_image_none_prompt(self):
        """Тест генерации с None промптом"""
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator()
            
            result = generator.generate_image(None)
            
            assert result is None
    
    def test_generate_image_long_prompt(self):
        """Тест генерации с длинным промптом"""
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator()
            
            long_prompt = "a" * 1500  # Длиннее 1000 символов
            
            with patch('generators.image_gen.logger') as mock_logger:
                result = generator.generate_image(long_prompt)
                
                # Проверяем, что было предупреждение о длинном промпте
                mock_logger.warning.assert_called_once()
    
    @patch('generators.image_gen.openai.OpenAI')
    def test_generate_image_success(self, mock_openai):
        """Тест успешной генерации изображения"""
        # Настройка мока
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].url = "https://example.com/image.jpg"
        mock_client.images.generate.return_value = mock_response
        mock_openai.return_value = mock_client
        
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator()
            
            result = generator.generate_image("Test prompt")
            
            assert result == "https://example.com/image.jpg"
            mock_client.images.generate.assert_called_once()
    
    @patch('generators.image_gen.openai.OpenAI')
    def test_generate_image_authentication_error(self, mock_openai):
        """Тест ошибки аутентификации"""
        mock_client = MagicMock()
        mock_client.images.generate.side_effect = make_authentication_error()
        mock_openai.return_value = mock_client
        
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator()
            
            result = generator.generate_image("Test prompt")
            
            assert result is None
    
    @patch('generators.image_gen.openai.OpenAI')
    def test_generate_image_rate_limit_error(self, mock_openai):
        """Тест ошибки лимита запросов"""
        mock_client = MagicMock()
        mock_client.images.generate.side_effect = make_rate_limit_error()
        mock_openai.return_value = mock_client
        
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator()
            
            result = generator.generate_image("Test prompt")
            
            assert result is None
    
    @patch('generators.image_gen.openai.OpenAI')
    def test_generate_image_bad_request_error(self, mock_openai):
        """Тест ошибки неверного запроса"""
        mock_client = MagicMock()
        mock_client.images.generate.side_effect = make_bad_request_error()
        mock_openai.return_value = mock_client
        
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator()
            
            result = generator.generate_image("Test prompt")
            
            assert result is None
    
    @patch('generators.image_gen.openai.OpenAI')
    def test_generate_image_api_error(self, mock_openai):
        """Тест ошибки API"""
        mock_client = MagicMock()
        mock_client.images.generate.side_effect = make_api_error()
        mock_openai.return_value = mock_client
        
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator()
            
            result = generator.generate_image("Test prompt")
            
            assert result is None
    
    @patch('generators.image_gen.openai.OpenAI')
    def test_generate_image_general_exception(self, mock_openai):
        """Тест общего исключения"""
        mock_client = MagicMock()
        mock_client.images.generate.side_effect = Exception("General error")
        mock_openai.return_value = mock_client
        
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator()
            
            result = generator.generate_image("Test prompt")
            
            assert result is None
    
    @patch('generators.image_gen.openai.OpenAI')
    def test_generate_image_parameters(self, mock_openai):
        """Тест параметров генерации"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [MagicMock()]
        mock_response.data[0].url = "https://example.com/image.jpg"
        mock_client.images.generate.return_value = mock_response
        mock_openai.return_value = mock_client
        
        with patch('generators.image_gen.config') as mock_config:
            mock_config.openai_api_key = 'test-key'
            
            generator = ImageGenerator(model="dall-e-2")
            
            generator.generate_image("Test prompt")
            
            # Проверяем параметры вызова
            call_args = mock_client.images.generate.call_args
            assert call_args[1]['model'] == "dall-e-2"
            assert call_args[1]['size'] == "1024x1024"
            assert call_args[1]['quality'] == "standard"
            assert call_args[1]['n'] == 1
