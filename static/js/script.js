document.addEventListener('DOMContentLoaded', function() {
    // Получаем CSRF-токен из куки
    function getCsrfToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 'csrftoken'.length + 1) === ('csrftoken' + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Инициализация данных из Django
    let userData = { clicks: 0, colors: [] };
    const dataScript = document.getElementById('initial-user-data');
    if (dataScript) {
        try {
            userData = JSON.parse(dataScript.textContent);
        } catch (e) {
            console.error("Ошибка парсинга данных пользователя:", e);
        }
    }

    let currentCount = userData.clicks || 0;
    let ownedColors = userData.colors || [];

    // DOM-элементы
    const counterDisplay = document.getElementById('counter-display');
    const clickBtn = document.getElementById('btn-click');
    const saveBtn = document.getElementById('btn-save');
    const mainCard = document.getElementById('main-card');
    const activeColorSelect = document.getElementById('active-color-select');

    // ФУНКЦИЯ СМЕНЫ ЦВЕТА
    function applySelectedColor(colorName) {
        // Убираем пробелы, если они есть в БД
        colorName = colorName ? colorName.trim() : "";
        
        if (!colorName) {
            mainCard.classList.remove('active-color-bg');
            return;
        }
        
        const colorMap = {
            'Красный': '#ffcccc',
            'Синий': '#cce5ff',
            'Зелёный': '#ccffcc',
            'Жёлтый': '#fff3cd'
        };
        const newColor = colorMap[colorName];
        
        if (newColor) {
            // Устанавливаем CSS-переменную и добавляем класс-перебиватель
            mainCard.style.setProperty('--chosen-color', newColor);
            mainCard.classList.add('active-color-bg');
        } else {
            // Если название не совпало - сбрасываем
            mainCard.classList.remove('active-color-bg');
            console.warn(`Цвет "${colorName}" не найден в colorMap! Проверьте название в БД`);
        }
    }

    // ОБНОВЛЕНИЕ UI
    function updateUI() {
        counterDisplay.innerText = currentCount;
        updateShopButtons();
        updateOwnedColorsDropdown();
    }

    function updateShopButtons() {
        const buyButtons = document.querySelectorAll('.buy-color-btn');
        buyButtons.forEach(btn => {
            const cost = parseInt(btn.dataset.cost);
            const colorName = btn.dataset.color;
            
            if (ownedColors.includes(colorName) || currentCount < cost) {
                btn.disabled = true;
                if (ownedColors.includes(colorName)) {
                    btn.innerText = "Уже есть";
                } else {
                    btn.innerText = `Нужно ${cost}`;
                }
            } else {
                btn.disabled = false;
                btn.innerText = "Купить";
            }
        });
    }

    // ГЛАВНОЕ ИСПРАВЛЕНИЕ: Никогда не ставим пустое значение, если есть купленные цвета!
    function updateOwnedColorsDropdown() {
        const currentSelection = activeColorSelect.value;
        activeColorSelect.innerHTML = '';

        // 1. Добавляем "Выберите цвет" (оно всегда disabled)
        const defaultOption = document.createElement('option');
        defaultOption.value = "";
        defaultOption.disabled = true;
        defaultOption.innerText = "Выберите цвет";
        activeColorSelect.appendChild(defaultOption);

        // 2. Если купленных цветов нет
        if (ownedColors.length === 0) {
            const noColorOption = document.createElement('option');
            noColorOption.value = "";
            noColorOption.disabled = true;
            noColorOption.innerText = "Нет купленных цветов";
            activeColorSelect.appendChild(noColorOption);
            mainCard.style.backgroundColor = '#ffffff';
            return; // Прерываем функцию, чтобы ничего не ломать
        }

        // 3. Добавляем купленные цвета
        ownedColors.forEach(color => {
            const option = document.createElement('option');
            option.value = color;
            option.innerText = color;
            activeColorSelect.appendChild(option);
        });

        // 4. Восстанавливаем выбор. Если он потерян, ставим первый попавшийся!
        if (ownedColors.includes(currentSelection) && currentSelection !== "") {
            activeColorSelect.value = currentSelection;
            applySelectedColor(currentSelection);
        } else {
            // Если вдруг выбор сбросился - принудительно ставим первый цвет из списка
            activeColorSelect.value = ownedColors[0];
            applySelectedColor(ownedColors[0]);
        }
    }

    // 1. Кнопка "CLICK"
    clickBtn.addEventListener('click', function() {
        currentCount++;
        updateUI(); 
    });

    // 2. Кнопка "SAVE"
    saveBtn.addEventListener('click', function() {
        fetch('/add_click/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ 'clicks': currentCount })
        })
        .then(response => {
            if (response.status === 401 || response.status === 403) {
                alert('Чтобы сохранить прогресс, пожалуйста, войдите в аккаунт!');
                window.location.href = '/login/';
                return;
            }
            if (response.ok) {
                console.log('Клики сохранены в БД');
            } else {
                alert('Ошибка при сохранении кликов');
            }
        })
        .catch(error => console.error('Ошибка:', error));
    });

    // 3. Кнопка "Купить" в магазине
    document.querySelectorAll('.buy-color-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const colorName = this.dataset.color;
            const cost = parseInt(this.dataset.cost);

            if (currentCount < cost) {
                alert("Недостаточно кликов!");
                return;
            }

            fetch('/buy_color/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ 'color': colorName })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    currentCount -= cost;
                    ownedColors.push(colorName);
                    updateUI(); // Перерисовываем магазин

                    // Бонус: сразу выбираем купленный цвет
                    activeColorSelect.value = colorName;
                    applySelectedColor(colorName);

                    alert(`Вы успешно купили цвет "${colorName}"!`);
                } else {
                    alert(data.message || "Ошибка при покупке.");
                }
            })
            .catch(error => console.error('Ошибка покупки:', error));
        });
    });

    // 4. Смена активного цвета
    activeColorSelect.addEventListener('change', function() {
        const selectedColor = this.value;
        applySelectedColor(selectedColor);
    });

    // Запускаем обновление интерфейса при загрузке
    updateUI();
});