// AJAX dla podstrony budżetowej
document.getElementById('submitButton').addEventListener('click', function () {
    const form = document.getElementById('budgetForm');
    const formData = new FormData(form); 
    const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

    fetch(form.action, { // Za pomocą Fetch API wysyłamy formularz do serwera
        method: 'POST', // Wybieramy metode POST
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest' // Identyfikujemy jako zapytanie AJAX
        },
        body: formData // Wrzucamy dane z formularza
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response failed');
        }
        return response.json(); // Analizujemy odpowiedź serwera
    })
    .then(data => { // Sprawdzamy typ odpowiedzi i dostosowujemy odpowiedni tekst
        const responseMessage = document.getElementById('responseMessage');
        if (data.status === 'success') {
            responseMessage.textContent = data.message; 
            responseMessage.style.color = 'green';
        } else {
            responseMessage.textContent = data.message;
            responseMessage.style.color = 'red';
        }
    })
    .catch(error => { // Wyłapuje błędy
        console.error('There was a problem with the fetch operation:', error);
        const responseMessage = document.getElementById('responseMessage');
        responseMessage.textContent = 'Wystąpił błąd, spróbuj ponownie później.';
        responseMessage.style.color = 'red';
    });
});