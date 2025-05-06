document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');

    if (!form) {
        console.error('Форма не найдена!');
        return;
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const email = document.getElementById('email')?.value;
        const password = document.getElementById('password')?.value;

        if (!email || !password) {
            alert('Поля email и пароль обязательны!');
            return;
        }

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                throw new Error('Неверные учетные данные');
            }

            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            window.location.href = '/profile';
        } catch (error) {
            alert(error.message);
            console.error('Ошибка входа:', error);
        }
    });
});