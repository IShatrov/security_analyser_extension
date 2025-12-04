document.addEventListener('DOMContentLoaded', function() {
    console.log("in event listener")
  // Получаем текущую активную вкладку
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    if (tabs[0]) {
      const url = tabs[0].url;
      
      // Анализ безопасности
      // Можно было вместо запроса к localhost сделать через onnx или tensorflow
      // Но нам было лень
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
  
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    const verdictText = data.prediction === 'safe' ? 'Безопасно' : 'Небезопасно';
    const probabilityPercent = (data.probability * 100).toFixed(2);
      
    apiDataElement.innerHTML = `
      <strong>Вердикт:</strong> ${verdictText}<br>
      <strong>Вероятность безопасности:</strong> ${probabilityPercent}%
    `;
    
    
  } catch (error) {
    apiDataElement.textContent = `Ошибка: ${error.message}`;
    apiDataElement.className = 'api-data';
    apiResultElement.classList.add('error');
    
    console.error('Ошибка запроса к API:', error);
  }
}
