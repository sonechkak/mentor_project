// Ждем полной загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // Добавляем стили для кнопки
    const style = document.createElement('style');
    style.textContent = `
        .btn-social {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 4px;
            transition: all 0.3s ease;
        }

        .btn-social:hover {
            background-color: #4B0082;
        }

        .btn-social img {
            margin-right: 8px;
        }
    `;
    document.head.appendChild(style);
});

// Функция инициализации Telegram авторизации
function telegramAuth() {
    // Удаляем существующий контейнер, если он есть
    const existingContainer = document.getElementById('telegram-widget-container');
    if (existingContainer) {
        existingContainer.remove();
    }

    // Создаем новый контейнер для виджета
    const widgetContainer = document.createElement('div');
    widgetContainer.id = 'telegram-widget-container';
    widgetContainer.style.display = 'none';  // Скрываем контейнер
    document.body.appendChild(widgetContainer);

    // Создаем и настраиваем скрипт виджета
    const script = document.createElement('script');
    script.src = 'https://telegram.org/js/telegram-widget.js?22';
    script.async = true;

    // Устанавливаем все необходимые атрибуты
    const widgetParams = {
        'data-telegram-login': 'sysmind_mentor_project_bot',
        'data-size': 'large',
        'data-userpic': 'false',
        'data-auth-url': 'https://local-mentor-app.sonechkak.ru/complete/telegram/',
        'data-request-access': 'write'
    };

    // Применяем параметры к скрипту
    Object.entries(widgetParams).forEach(([key, value]) => {
        script.setAttribute(key, value);
    });

    // Добавляем обработчик загрузки скрипта
    script.onload = function() {
        console.log('Telegram widget loaded');
        // Здесь можно добавить дополнительную логику после загрузки виджета
        // Например, программно кликнуть по кнопке виджета
    };

    // Добавляем скрипт в контейнер
    widgetContainer.appendChild(script);
}