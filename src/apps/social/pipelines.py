import logging

import requests
from django.core.files.base import ContentFile
from django.db import transaction


from accounts.models import User

logger = logging.getLogger(__name__)


@transaction.atomic
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    logger.info(f"Starting create_user pipeline with details: {details}")

    if user:
        logger.info(f"Existing user found: {user.email}")
        return {"user": user}

    email = details.get("email", "")

    if not email:
        logger.error("Email not found in details")
        return None

    # Генерация username
    if backend.name == 'telegram':
        base_username = details.get('username', 'tg_user') or str(details.get('id'))
    elif backend.name == 'google-oauth2':
        base_username = email.split('@')[0]
    else:
        base_username = details.get('username', 'user')

    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    try:
        # Проверяем существует ли пользователь
        existing_user = User.objects.filter(email=email).first()
        if existing_user:
            logger.info(f"Found existing user by email: {email}")
            return {"user": existing_user}

        # Создаем пользователя через create_user
        user = User.objects.create_user(
            email=email,
            first_name=details.get("first_name", ""),
            last_name=details.get("last_name", ""),
            is_active=True,
            username=username,
        )

        # Обработка аватара
        picture_url = details.get("picture")
        if picture_url:
            try:
                response = requests.get(picture_url)
                if response.status_code == 200:
                    file_name = f"avatar_{user.id}.jpg"
                    user.avatar.save(file_name, ContentFile(response.content), save=True)
            except Exception as e:
                logger.error(f"Failed to download avatar: {e}")

        user.save()

        return {"user": user}

    except Exception as e:
        logger.error(f"Error in create_user pipeline: {e}")
        return None
