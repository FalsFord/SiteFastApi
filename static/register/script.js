document.getElementById('registrationForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const city = document.getElementById('city').value;
    const role = document.querySelector('input[name="role"]:checked').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Валидация
    if (password !== confirmPassword) {
        alert('Пароли не совпадают!');
        return;
    }

    if (password.length < 6) {
        alert('Пароль должен содержать не менее 6 символов');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                city: city,
                role: role,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Показываем успешную регистрацию
            document.getElementById('welcomeUser').textContent = username;
            document.getElementById('successModal').style.display = 'block';
        } else {
            alert(data.message || 'Ошибка регистрации');
        }

    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при регистрации');
    }
});

// Закрытие модального окна
document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('successModal').style.display = 'none';
    window.location.href = '/login';
});

window.addEventListener('click', function(e) {
    const modal = document.getElementById('successModal');
    if (e.target === modal) {
        modal.style.display = 'none';
        window.location.href = '/login';
    }
});z