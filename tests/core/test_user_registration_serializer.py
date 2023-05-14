import pytest
from core.serializers import UserRegistrationSerializer


"""
Тесты для UserRegistrationSerializer:

Проверить, что при передаче правильных данных происходит успешная регистрация пользователя.
Проверить, что при передаче неправильных данных (несовпадение паролей) возвращается ошибка.
"""



@pytest.mark.django_db
class TestUserRegistrationSerializer:
    # @pytest.mark.django_db
    def test_user_registration_serializer_valid_data(self):
        """
        Регистрация пользователя
        """
        data = {
            'username': 'testuser',
            'password': 'TestPassword123',
            'password_repeat': 'TestPassword123',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()

        assert user.username == data['username']
        assert user.email == data['email']


    # @pytest.mark.django_db
    def test_user_registration_serializer_invalid_password(self):
        """
        Проверка регистрации при несовпадении указанных паролей
        """
        data = {
            'username': 'testuser',
            'password': 'TestPassword123',
            'password_repeat': 'DifferentPassword123',  # задаем неверный пароль
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password_repeat' in serializer.errors


    # @pytest.mark.django_db
    def test_user_registration_serializer_valid_email(self):
        data = {
            'username': 'testuser',
            'password': 'TestPassword123',
            'password_repeat': 'TestPassword123',
            'email': 'invalid-email',  # Неверный формат почты
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors
