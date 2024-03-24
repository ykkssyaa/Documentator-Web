// Функция, которая будет вызываться при клике на кнопку "Удалить все документы"
document.getElementById("delete-documents-button").addEventListener("click", function() {
    // Показываем модальное окно
    document.getElementById("confirm-delete-modal").style.display = "block";
});

// Функция, которая будет вызываться при клике на кнопку подтверждения удаления
document.getElementById("confirm-delete-button").addEventListener("click", function() {
    // Отправляем форму на удаление
    document.getElementById("delete-documents-form").submit();
});

// Функция, которая будет вызываться при клике на кнопку отмены удаления
document.getElementById("cancel-delete-button").addEventListener("click", function() {
    // Скрываем модальное окно
    document.getElementById("confirm-delete-modal").style.display = "none";
});
