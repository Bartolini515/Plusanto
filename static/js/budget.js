// Importowanie z innych modułów
import { renderChart } from './chart.js';


// AJAX dla podstrony budżetowej
document.getElementById('submitButton').addEventListener('click', function (event) {
    event.preventDefault(); // Zapobiegamy defaultowemy zachowaniu na POSTa

    const responseMessage = document.getElementById('responseMessage');
    const ctx = chartDisplay.getContext('2d');
    ctx.clearRect(0, 0, chartDisplay.width, chartDisplay.height);

    if (myChart) {
        myChart.destroy();
    }

    if (parseInt(balanceInput.value) > parseInt(incomeInput.value) * 2) {
        if (confirm('Posiadasz saldo powyżej 2 wartości dochodu, czy chcesz rozprowadzić nadmiar do budżetu?')) {
            distributeConf = true;
        }
    }

    if (validatePercentages() && validateFormInputs()) {
        const form = document.getElementById('budgetForm');
        const formData = new FormData(form);
        formData.append('distributeConf', distributeConf);
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
                balanceDisplay.textContent = data.balance;
                budgetExpensesDisplay.textContent = data.budgetExpenses;
                budgetWantsDisplay.textContent = data.budgetWants;
                allowanceDisplay.textContent = data.allowance;
                budgetEmergencyDisplay.textContent = data.budgetEmergency;
                debtDisplay.textContent = data.debt;

                document.getElementById("calculatedResults").style.display = "";

                // Pokazujemy wiadomości zwrotne od algorytmu budżetowego
                const messagesContainer = document.getElementById('messages');
                messagesContainer.innerHTML = '';
                data.messages.forEach(message => {
                const li = document.createElement('li');
                li.textContent = message;
                messagesContainer.appendChild(li);
                });

                const type = 'pie';
                const labels = data.labels;
                const dataValues = data.values;
                const title = 'Alokacja budżetu';
                const show = false;
                myChart = renderChart(ctx, type, labels, title, dataValues, show);

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

// Funkcja do odczytywania ciasteczek o podanej nazwie
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie); // Dekoduje ciasteczko aby zająć się znakami specjalnymi
    let ca = decodedCookie.split(';'); // Dzielimy ciasteczko na części rozdzielone znakiem ';'
    for(let i = 0; i <ca.length; i++) { // Przeszukujemy ciasteczko
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length); // Jeżeli znajdziemy ciasteczko zwracamy jego wartość
        }
    }
    return "";
}

// Funkcja opóźniająca akcje, "debouncing"
function debounce(func, delay) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

// Walidacja dla procentów na stronie budżetowej
function validatePercentages() {
    const errorMessageElement = document.getElementById('errorValidateJS');
    const wants = parseInt(percentWantsInput.value) || 0;
    const allowance = parseInt(percentAllowanceInput.value) || 0;
    const emergency = parseInt(percentEmergencyInput.value) || 0;
    const total = wants + allowance + emergency;

    if (total != 50) {
        errorMessageElement.textContent = 'Suma procentów musi się równać 50%. Niezgadzająca się ilość punktów procentowych: ' + (total - 50);
        errorMessageElement.style.display = 'block'; // Pokaż błąd
        // Zmiana stylu obramowań sygnalizująca błędne dane
        percentWantsInput.style.borderColor = 'red';
        percentAllowanceInput.style.borderColor = 'red';
        percentEmergencyInput.style.borderColor = 'red';
        return false;
    } else {
        // Reset stylu oraz komunikatu
        errorMessageElement.textContent = '';
        errorMessageElement.style.display = 'none';
        percentWantsInput.style.borderColor = '';
        percentAllowanceInput.style.borderColor = '';
        percentEmergencyInput.style.borderColor = '';
        return true;
    }
}

// Walidacja dla długości pól na stronie budżetowej
function validateFormInputs() {
    const inputs = [balanceInput, incomeInput, expensesInput, debtInput, emergencyFundInput, plannedEmergencyFundInput, buforInput];
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

// Funkcja ustawiająca elementy zgodnie z typem budżetu
function checkBudgetType(value) { 
    switch (value) {
        case '1': // Typ budżetu stabilny
            // Dla procentów
            percentWantsSpan.style.display = ''; // Pokaż element
            percentWantsInput.value = 30;
            percentAllowanceInput.value = 15;
            if (getCookie('emergencyFundChecked') == 'True') {
                percentEmergencyInput.value = 5; 
            } else {
                percentEmergencyInput.value = 0;
            }

            // Dla buforu
            buforSpan.style.display = 'none' // Ukryj element
            buforInput.value = 0;
            break;
        case '2': // Typ budżetu rozwojowy
            // Dla procentów
            percentWantsSpan.style.display = 'none'; // Ukryj element
            percentWantsInput.value = 0; 
            percentAllowanceInput.value = 30; 
            if (getCookie('emergencyFundChecked') == 'True') {
                percentEmergencyInput.value = 20; 
            } else {
                percentEmergencyInput.value = 0;
            }

            // Dla buforu
            buforSpan.style.display = '' // Pokaż element
            buforInput.value = '';
            break;
    }
}

// Funkcja projektowania danych z JSONa do pól
export function budgetOutDataDisplay(data) {
    const ctx = chartDisplay.getContext('2d');
    ctx.clearRect(0, 0, chartDisplay.width, chartDisplay.height);

    if (myChart) {
        myChart.destroy();
    }

    balanceDisplay.textContent = data.balance;
    budgetExpensesDisplay.textContent = data.budgetExpenses;
    budgetWantsDisplay.textContent = data.budgetWants;
    allowanceDisplay.textContent = data.allowance;
    budgetEmergencyDisplay.textContent = data.budgetEmergency;
    debtDisplay.textContent = data.debt;
    document.getElementById("calculatedResults").style.display = "";

    const type = 'pie';
    const labels = data.labels;
    const dataValues = data.values;
    const title = 'Alokacja budżetu';
    const show = false;
    myChart = renderChart(ctx, type, labels, title, dataValues, show);
}

// Funkcja ustawiająca elementy zgodnie z wybranymi opcjami
function checkOptions() {
    if (getCookie('debtChecked') == '' || getCookie('emergencyFundChecked') == '') { 
            document.cookie = "debtChecked=True; expires=Wed, 29 Dec 2077 12:00:00 UTC;";
            document.cookie = "emergencyFundChecked=True; expires=Wed, 29 Dec 2077 12:00:00 UTC;";
    }

    if (getCookie('debtChecked') == 'True') {
        debtSpan.style.display = '';
        debtDisplayHeader.style.display = '';
        debtCheckbox.checked = true;
    } else {
        debtSpan.style.display = 'none';
        debtDisplayHeader.style.display = 'none';
        debtCheckbox.checked = false;
        debtInput.value = 0;
    }

    if (getCookie('emergencyFundChecked') == 'True') {
        emergencyFundSpan.style.display = '';
        percentEmergencySpan.style.display = '';
        emergencyFundCheckbox.checked = true;
    } else {
        emergencyFundSpan.style.display = 'none';
        percentEmergencySpan.style.display = 'none';
        emergencyFundCheckbox.checked = false;
        emergencyFundInput.value = 0;
        plannedEmergencyFundInput.value = 0;
        percentEmergencyInput.value = 0;
    }
}

// Funkcja sprawdzająca stan checkbox-a
function checkDebtChecked(state){
    if (state) {
        document.cookie = "debtChecked=True; expires=Wed, 29 Dec 2077 12:00:00 UTC;";
    } else {
        document.cookie = "debtChecked=False; expires=Wed, 29 Dec 2077 12:00:00 UTC;";
    }
    checkOptions()
}

// Funkcja sprawdzająca stan checkbox-a
function checkEmergencyFundChecked(state){
    if (state) {
        document.cookie = "emergencyFundChecked=True; expires=Wed, 29 Dec 2077 12:00:00 UTC;";
    } else {
        document.cookie = "emergencyFundChecked=False; expires=Wed, 29 Dec 2077 12:00:00 UTC;";
    }
    checkOptions()
}


function toggleHelp() {
    const helpText = document.getElementById('helpText');
    helpText.classList.toggle('active'); // Dodaje/usuwa klasę "active"
}

// Wyciąganie elementów z formularza
const balanceInput = document.getElementById('id_balance');
const incomeInput = document.getElementById('id_income');
const expensesInput = document.getElementById('id_expenses');
const debtInput = document.getElementById('id_debt');
const emergencyFundInput = document.getElementById('id_emergencyFund');
const plannedEmergencyFundInput = document.getElementById('id_plannedEmergencyFund');
const buforInput = document.getElementById('id_bufor');
const budgetTypeField = document.getElementById('id_budgetType');
const percentWantsInput = document.getElementById('id_percentWants');
const percentAllowanceInput = document.getElementById('id_percentAllowance');
const percentEmergencyInput = document.getElementById('id_percentEmergency');

const balanceDisplay = document.getElementById('balanceDisplay');
const budgetExpensesDisplay = document.getElementById('budgetExpensesDisplay');
const budgetWantsDisplay = document.getElementById('budgetWantsDisplay');
const allowanceDisplay = document.getElementById('allowanceDisplay');
const budgetEmergencyDisplay = document.getElementById('budgetEmergencyDisplay');
const debtDisplay = document.getElementById('debtDisplay');
const chartDisplay = document.getElementById('chartDisplay');

const debtSpan = document.getElementById('debtSpan');
const emergencyFundSpan = document.getElementById('emergencyFundSpan');
const buforSpan = document.getElementById('buforSpan');
const percentWantsSpan = document.getElementById('percentWantsSpan');
const percentEmergencySpan = document.getElementById('percentEmergencySpan');
const debtDisplayHeader = document.getElementById('debtDisplayHeader');

const debtCheckbox = document.getElementById('debtCheckbox');
const emergencyFundCheckbox = document.getElementById('emergencyFundCheckbox');

// Debouncowanie funkcji
const validateFormInputsDebounced = debounce(validateFormInputs, 300);
const validatePercentagesDebounced = debounce(validatePercentages, 300);

// Dodawanie event listenerów do każdego inputu i ich odpowiednich walidatorów
balanceInput.addEventListener('input', validateFormInputsDebounced);
incomeInput.addEventListener('input', validateFormInputsDebounced);
expensesInput.addEventListener('input', validateFormInputsDebounced);
debtInput.addEventListener('input', validateFormInputsDebounced);
emergencyFundInput.addEventListener('input', validateFormInputsDebounced);
buforInput.addEventListener('input', validateFormInputsDebounced);
budgetTypeField.addEventListener('input', validateFormInputsDebounced);
budgetTypeField.addEventListener('change', () => checkBudgetType(budgetTypeField.value));
percentWantsInput.addEventListener('input', validatePercentagesDebounced);
percentAllowanceInput.addEventListener('input', validatePercentagesDebounced);
percentEmergencyInput.addEventListener('input', validatePercentagesDebounced);

debtCheckbox.addEventListener('change', () => checkDebtChecked(debtCheckbox.checked));
emergencyFundCheckbox.addEventListener('change', () => checkEmergencyFundChecked(emergencyFundCheckbox.checked));

// Reszta
checkOptions();
checkBudgetType(budgetTypeField.value);
let myChart = null;
let distributeConf = false;
