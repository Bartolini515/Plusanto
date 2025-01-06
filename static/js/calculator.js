// Po naciśnięciu przycisku wykonuje program
document.getElementById('tax-calculator').addEventListener('submit', function(event) {
    event.preventDefault();
    const income = parseFloat(incomeInput.value);
    const deductions = parseFloat(deductionsInput.value);
    const taxableIncome = income - deductions;
    const taxAmount = calculateTax(taxableIncome);
    document.getElementById('tax-amount').innerText = `Wartość twojego podatku: ${taxAmount}`;
    document.getElementById('result').style.display = 'block';
});

// Funkcja obliczająca podatek
function calculateTax(income) { 
    const taxRate = income > 120000 ? 0.32 : 0.12; // Progi podatkowe: 32% dla dochodu powyżej 120 000 PLN, 12% dla dochodu poniżej 120 000 PLN
    return income > 0 ? (income * taxRate).toFixed(2) : 0; // Jeżeli dochód jest dodatni, oblicz podatek, w przeciwnym wypadku zwróć 0
}

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
    const inputs = [incomeInput, deductionsInput];
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
const incomeInput = document.getElementById('id_income');
const deductionsInput = document.getElementById('id_deductions');

// Debouncowanie funkcji
const validateFormInputsDebounced = debounce(validateInputs, 300);

// Dodawanie event listenerów do każdego inputu i ich odpowiednich walidatorów
incomeInput.addEventListener('input', validateFormInputsDebounced);
deductionsInput.addEventListener('input', validateFormInputsDebounced);