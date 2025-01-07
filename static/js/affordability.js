// Importowanie z innych modułów
import { renderChart } from './chart.js';


// AJAX dla podstrony przystępnościomierza
document.querySelectorAll('.button2').forEach(button => {
    button.addEventListener('click', function (event) {
        event.preventDefault(); // Zapobiegamy defaultowemy zachowaniu na POSTa

        const responseMessage = document.getElementById('responseMessage');
        const ctx = chartDisplay.getContext('2d');
        ctx.clearRect(0, 0, chartDisplay.width, chartDisplay.height);

        if (myChart) {
            myChart.destroy();
        }

        if (validateInputs()) {
            const action = this.getAttribute('data-action');
            const form = document.getElementById('affordability-checker');
            const formData = new FormData(form);
            if (action == 'save') { // Jeżeli jest zapisywanie to dodaje balansy
                formData.append('balanceAft', balanceAftDisplay.textContent);
                formData.append('budgetExpensesAft', budgetExpensesAftDisplay.textContent);
                formData.append('budgetWantsAft', budgetWantsAftDisplay.textContent);
                formData.append('allowanceAft', allowanceAftDisplay.textContent);
            }
            formData.append('action', action);
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
                if (data.status === 'success') {
                    if (action == 'calculate') {
                        if (data.canDo == '1') {
                            canDoDisplay.textContent = 'Wydatek jest możliwy do pokrycia!';
                            canDoDisplay.style.color = 'green'
                            balanceDisplay.textContent = data.balance;
                            budgetExpensesDisplay.textContent = data.budgetExpenses;
                            budgetWantsDisplay.textContent = data.budgetWants;
                            allowanceDisplay.textContent = data.allowance;

                            balanceAftDisplay.textContent = data.balanceAft;
                            budgetExpensesAftDisplay.textContent = data.budgetExpensesAft;
                            budgetWantsAftDisplay.textContent = data.budgetWantsAft;
                            allowanceAftDisplay.textContent = data.allowanceAft;

                            document.getElementById("calculatedResults").style.display = "";

                            const type = 'bar';
                            const labels = data.labels;
                            const dataValues = data.values;
                            const title = 'Porównanie przed i po wydatku';
                            const show = true;
                            myChart = renderChart(ctx, type, labels, title, dataValues, show);
                        } else {
                            document.getElementById("calculatedResults").style.display = "";
                            canDoDisplay.textContent = 'Wydatek nie jest możliwy do pokrycia!';
                            canDoDisplay.style.color = 'red';
                        }
                        // Pokazujemy wiadomości zwrotne od algorytmu
                        const messagesContainer = document.getElementById('messages');
                        messagesContainer.innerHTML = '';
                        data.messages.forEach(message => {
                        const li = document.createElement('li');
                        li.textContent = message;
                        messagesContainer.appendChild(li);
                    });
                    }
                    responseMessage.textContent = data.message; 
                    responseMessage.style.color = 'green';
                } else {
                    responseMessage.textContent = data.message;
                    responseMessage.style.color = 'red';
                }
            })
            .catch(error => { // Wyłapuje błędy
                console.error('There was a problem with the fetch operation:', error);
                responseMessage.textContent = 'Wystąpił błąd, spróbuj ponownie później.';
                responseMessage.style.color = 'red';
            });
        } else { // Jeżeli walidacje JS nie przeszły dajemy niepoprawny format danych
            responseMessage.textContent = 'Niepoprawny format danych.';
            responseMessage.style.color = 'red';
        };
    });
});

// Funkcja opóźniająca akcje, "debouncing"
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

// Funkcja walidująca wprowadzone dane
function validateInputs() {
    const inputs = [expenseInput];
    const errorMessageElement = document.getElementById('errorValidateJS');
    let isValid = true; // Zakładamy z początku, że wszystko jest zgodne

    // Czyścimy wczesniejszy błąd (używamy tego samego spana do kilku errorów, zmienić?)
    errorMessageElement.textContent = '';
    errorMessageElement.style.display = 'none';

    // Iterujemy przez wszystkie elementy
    inputs.forEach(input => {
        if (input.value.length > 9) { // Jeżeli ma więcej niż 9 liczb dajemy błąd
            isValid = false;
            errorMessageElement.textContent = 'Pola nie mogą być dłuższe niż 9 liczb.';
            errorMessageElement.style.display = 'block';
            input.style.borderColor = 'red';
        } else if(!/^\d*$/.test(input.value)) { // Regex który sprawdza czy pole zawiera tylko cyfry
            isValid = false;
            errorMessageElement.textContent = 'Pola muszą zawierać wyłącznie cyfry, bez znaków specjalnych.';
            errorMessageElement.style.display = 'block';
            input.style.borderColor = 'red';
        } else {
            input.style.borderColor = '';
        }
    });

    return isValid;
}

// Wyciąganie elementow ze strony
const expenseInput = document.getElementById('id_expense');
const balanceDisplay = document.getElementById('balanceDisplay');
const budgetExpensesDisplay = document.getElementById('budgetExpensesDisplay');
const budgetWantsDisplay = document.getElementById('budgetWantsDisplay');
const allowanceDisplay = document.getElementById('allowanceDisplay');

const balanceAftDisplay = document.getElementById('balanceAftDisplay');
const budgetExpensesAftDisplay = document.getElementById('budgetExpensesAftDisplay');
const budgetWantsAftDisplay = document.getElementById('budgetWantsAftDisplay');
const allowanceAftDisplay = document.getElementById('allowanceAftDisplay');
const canDoDisplay = document.getElementById('canDoDisplay');
const chartDisplay = document.getElementById('chartDisplay');

// Debouncowanie funkcji
const validateFormInputsDebounced = debounce(validateInputs, 300);

// Dodawanie event listenerów do każdego inputu i ich odpowiednich walidatorów
expenseInput.addEventListener('input', validateFormInputsDebounced);

// Reszta
let myChart = null;