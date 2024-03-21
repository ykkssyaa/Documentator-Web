document.addEventListener('DOMContentLoaded', function() {
    // Находим все элементы чекбоксов с классом 'duty-checkbox'
    const csrfToken = document.getElementById('csrf-token').getAttribute('data-csrf-token');
    const checkboxes = document.querySelectorAll('.duty-checkbox');

    // Для каждого чекбокса добавляем обработчик события change
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            // Получаем идентификатор обязательства (Duty)
            var dutyId = this.dataset.dutyId;

            // Получаем состояние чекбокса (выбран или нет)
            var isChecked = this.checked;

            // Отправляем AJAX-запрос на обновление состояния обязательства
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/documents/duty/' + dutyId + '/update/', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.setRequestHeader('X-CSRFToken', csrfToken);

            xhr.onload = function() {
                if (xhr.status === 200) {
                    // Обработка успешного ответа
                    var response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        console.log('Состояние обязательства успешно обновлено');
                    } else {
                        console.error('Ошибка при обновлении состояния обязательства:', response.error);
                    }
                } else {
                    console.error('Ошибка при отправке запроса:', xhr.statusText);
                }
            };
            xhr.onerror = function() {
                console.error('Ошибка при отправке запроса');
            };
            xhr.send('done=' + isChecked);
        });
    });
});