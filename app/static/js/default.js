// Элементы DOM
const itemsList = document.getElementById('items-list');
const nameInput = document.getElementById('name');
const priceInput = document.getElementById('price');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const formTitle = document.getElementById('form-title');
const messageToast = document.getElementById('message_toast');


let editMode = false;
let editingId = null;

// Вспомогательная функция для отображения сообщений
function showMessage(text, isError = false) {
    messageToast.textContent = text;
    messageToast.style.display = 'block';
    setTimeout(() => {
        messageToast.style.display = 'none';
    }, 3000);
}

// Загрузка всех товаров
async function loadItems() {
    try {
        const response = await fetch('/items');
        if (!response.ok) throw new Error('Ошибка загрузки');
        const items = await response.json();
        renderItems(items);
    } catch (error) {
        console.error(error);
        showMessage('Не удалось загрузить список товаров', true);
        itemsList.innerHTML = '<tr><td colspan="4" class="w3-center">Ошибка загрузки</td></tr>';
    }
}

// Отображение товаров в таблице
function renderItems(items) {
    if (items.length === 0) {
        itemsList.innerHTML = '<tr><td colspan="4" class="w3-center">Нет товаров</td></tr>';
        return;
    }
    itemsList.innerHTML = items.map(item => `
        <tr>
            <td>${item.id}</td>
            <td>${escapeHtml(item.name)}</td>
            <td>${item.price.toFixed(2)} ₽</td>
            <td>
                <div class="action-buttons">
                    <button class="edit-btn" data-id="${item.id}" data-name="${escapeHtml(item.name)}" data-price="${item.price}">
                        <i class="fas fa-edit"></i> Редактировать
                    </button>
                    <button class="delete-btn" data-id="${item.id}">
                        <i class="fas fa-trash-alt"></i> Удалить
                    </button>
                </div>
            </td>
        </tr>
    `).join('');

    // Навешиваем обработчики на кнопки
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = parseInt(btn.dataset.id);
            const name = btn.dataset.name;
            const price = parseFloat(btn.dataset.price);
            startEdit(id, name, price);
        });
    });
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = parseInt(btn.dataset.id);
            deleteItem(id);
        });
    });
}

// Простая защита от XSS
function escapeHtml(str) {
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

// Создание товара
async function createItem(name, price) {
    try {
        const response = await fetch('/items', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, price })
        });
        if (!response.ok) throw new Error('Ошибка создания');
        const newItem = await response.json();
        showMessage(`Товар "${newItem.name}" создан`);
        loadItems();
        resetForm();
    } catch (error) {
        console.error(error);
        showMessage('Не удалось создать товар', true);
    }
}

// Обновление товара
async function updateItem(id, name, price) {
    try {
        const response = await fetch(`/items/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, price })
        });
        if (!response.ok) throw new Error('Ошибка обновления');
        const updated = await response.json();
        showMessage(`Товар "${updated.name}" обновлён`);
        loadItems();
        resetForm();
    } catch (error) {
        console.error(error);
        showMessage('Не удалось обновить товар', true);
    }
}

// Удаление товара
async function deleteItem(id) {
    if (!confirm('Вы уверены, что хотите удалить товар?')) return;
    try {
        const response = await fetch(`/items/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Ошибка удаления');
        showMessage('Товар удалён');
        loadItems();
        if (editMode && editingId === id) resetForm();
    } catch (error) {
        console.error(error);
        showMessage('Не удалось удалить товар', true);
    }
}

// Режим редактирования
function startEdit(id, name, price) {
    editMode = true;
    editingId = id;
    nameInput.value = name;
    priceInput.value = price;
    formTitle.innerHTML = '<i class="fas fa-edit"></i> Редактировать товар';
    submitBtn.innerHTML = '<i class="fas fa-save"></i> Сохранить';
    cancelBtn.style.display = 'inline-block';
}

// Сброс формы
function resetForm() {
    editMode = false;
    editingId = null;
    nameInput.value = '';
    priceInput.value = '';
    formTitle.innerHTML = '<i class="fas fa-plus-circle"></i> Добавить товар';
    submitBtn.innerHTML = '<i class="fas fa-save"></i> Создать';
    cancelBtn.style.display = 'none';
}

// Обработка отправки формы
submitBtn.addEventListener('click', () => {
    const name = nameInput.value.trim();
    const price = parseFloat(priceInput.value);
    if (!name) {
        showMessage('Введите название товара', true);
        return;
    }
    if (isNaN(price) || price < 0) {
        showMessage('Введите корректную цену (число ≥ 0)', true);
        return;
    }
    if (editMode && editingId !== null) {
        updateItem(editingId, name, price);
    } else {
        createItem(name, price);
    }
});

cancelBtn.addEventListener('click', resetForm);

// Загрузка при старте
loadItems();