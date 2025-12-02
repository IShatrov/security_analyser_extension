document.addEventListener('DOMContentLoaded', function() {
    console.log("in event listener")
  // Получаем текущую активную вкладку
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    if (tabs[0]) {
      const url = tabs[0].url;
      document.getElementById('current-url').textContent = url;
      
      // Здесь в будущем будет анализ безопасности
      // Пока просто показываем URL
      fetchLocalhostAPI(url);
    }
  });
});

async function fetchLocalhostAPI(url) {
  const apiDataElement = document.getElementById('api-data');
  const apiResultElement = document.getElementById('api-result');
  
  try {
    // Показываем статус загрузки
    apiDataElement.textContent = 'Выполняется запрос...';
    apiDataElement.className = 'api-data loading';
    
    const response = await fetch('http://localhost:8080/example', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        url_to_test: url,
      })
    });
    
    // Проверяем статус ответа
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
      // 4. Парсим JSON ответ от FastAPI
      const data = await response.json();
      
    apiDataElement.innerHTML = `
      <strong>Статус:</strong> ${response.status} ${response.statusText}<br>
      <strong>Данные:</strong><br>
      <pre>${JSON.stringify(data, null, 2)}</pre>
    `;
    
    // Если хотите, можно обновить статус безопасности на основе ответа
    //updateSecurityStatus(data);
    
  } catch (error) {
    // Обработка ошибок
    apiDataElement.textContent = `Ошибка: ${error.message}`;
    apiDataElement.className = 'api-data';
    apiResultElement.classList.add('error');
    
    console.error('Ошибка запроса к API:', error);
  }
}
