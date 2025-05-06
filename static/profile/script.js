
// Ожидаем полной загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // Получаем кнопку с проверкой
    const logoutBtn = document.getElementById('logoutBtn');

    if (!logoutBtn) {
        console.error('Элемент с id="logoutBtn" не найден! Проверьте:');
        console.log('1. Правильность написания id в HTML');
        console.log('2. Что элемент существует в DOM');
        console.log('3. Что скрипт подключен после элемента');
        return;
    }

    // Добавляем обработчик
    logoutBtn.addEventListener('click', async function() {
        console.log('Кнопка выхода нажата');

        try {
            // Блокируем кнопку
            logoutBtn.disabled = true;
            const originalText = logoutBtn.textContent;
            logoutBtn.textContent = 'Выход...';

            // Отправляем запрос на выход
            const response = await fetch('/logout', {
                method: 'GET',
                credentials: 'include'
            });

            // Очищаем данные
            localStorage.clear();
            document.cookie.split(';').forEach(cookie => {
                const [name] = cookie.trim().split('=');
                document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
            });

            // Перенаправляем
            window.location.href = '/login';

        } catch (error) {
            console.error('Ошибка при выходе:', error);
            window.location.href = '/login';
        }
    });
});