import pytest


@pytest.mark.django_db
def test_create_user(user):
    assert user.first_name == 'User'
    assert user.email == 'user@example.com'
    assert user.check_password('Userpassword123/*-')
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert not user.is_admin


@pytest.mark.django_db
def test_create_superuser(superuser):
    assert superuser.first_name == 'Admin User'
    assert superuser.email == 'admin@example.com'
    assert superuser.check_password('Adminpassword123/*-')
    assert superuser.is_active
    assert superuser.is_staff
    assert superuser.is_superuser
    assert superuser.is_admin


def test_create_user_without_first_name(user_data, user_model):
    user_data['first_name'] = ''
    with pytest.raises(ValueError, match="Имя обязательно для создания пользователя."):
        user_model.objects.create_user(**user_data)


def test_create_user_without_email(user_data, user_model):
    user_data['email'] = ''
    with pytest.raises(ValueError, match="Email обязателен для создания пользователя."):
        user_model.objects.create_user(**user_data)


def test_create_user_without_password(user_data, user_model):
    user_data['password'] = ''
    with pytest.raises(ValueError, match="Пароль обязателен для создания пользователя."):
        user_model.objects.create_user(**user_data)


def test_create_superuser_without_is_staff(superuser_data, user_model):
    superuser_data['is_staff'] = False
    with pytest.raises(ValueError, match="Суперпользователь должен иметь is_staff=True."):
        user_model.objects.create_superuser(**superuser_data)


def test_create_superuser_without_is_superuser(superuser_data, user_model):
    superuser_data['is_superuser'] = False
    with pytest.raises(ValueError, match="Суперпользователь должен иметь is_superuser=True."):
        user_model.objects.create_superuser(**superuser_data)


def test_create_superuser_without_is_admin(superuser_data, user_model):
    superuser_data['is_admin'] = False
    with pytest.raises(ValueError, match="Администратор должен иметь is_admin=True."):
        user_model.objects.create_superuser(**superuser_data)
