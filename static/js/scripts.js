function checkAlerts(messages, levels) {
    alertBox = document.getElementsByClassName("alert")[0] // Wybiera pierwszy element, czyli jedyny, z klasy "alert"
    const error_messages = [];
    const success_messages = [];

    messages.forEach((message, i) => { // Dopisuje do odpowiadającej tablicy każdą wiadomość (dodatkowe poziomy na potencjalne rozszerzenie)
        switch (levels[i]) {
            case 'debug':
            case 'info':
            case 'success':
                success_messages.push(message);
                break;
            case 'warning':
            case 'error':
                error_messages.push(message);
                break;
            default:
                break;
        };
    });

    if (error_messages.length > 0) { // Jeżeli istnieją errory to wyświetla tylko je ignorując inne komunikaty
        alertBox.style.backgroundColor = "red";
        // Jak maks naprawi <li> to wtedy usunąć wszystko z br
        const ul = document.createElement("ul");
        error_messages.forEach(message => {
            const li = document.createElement("li");
            li.textContent = message;
            ul.appendChild(li);
            const br = document.createElement("br");
            ul.appendChild(br);
        });

        alertBox.innerHTML = "";
        alertBox.style.display = '';
        setTimeout(() => {
            alertBox.style.display = "none";
        }, 8000);
        alertBox.appendChild(ul); 
    } else { // Jeżeli nie ma errorów to wyświetla wszystkie komunikaty
        const ul = document.createElement("ul");
        success_messages.forEach(message => {
            const li = document.createElement("li");
            li.textContent = message;
            ul.appendChild(li);
            const br = document.createElement("br");
            ul.appendChild(br);
        });

        alertBox.innerHTML = "";
        alertBox.style.display = '';
        setTimeout(() => {
            alertBox.style.display = "none";
        }, 8000);
        alertBox.appendChild(ul); 
    };
};

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

// Funkcja sprawdzająca akceptację ciasteczek
function checkCookiesAccept() {
    blockade = document.getElementsByClassName("blokada")[0] // Wybiera pierwszy element, czyli jedyny, z klasy "blokada"
    cookies = document.getElementsByClassName("ciasteczka")[0] // Wybiera pierwszy element, czyli jedyny, z klasy "ciasteczka"
    if (getCookie('cookies-accepted') == "") { // Sprawdza czy istnieje cookie cookies-accepted, jeżeli funkcja zwraca pusty string to wyświetla proces akceptacji
        blockade.style.display = '';
        cookies.style.display = '';
        document.getElementById('cookie-accept').addEventListener('click', function() {
            blockade.style.display = 'none';
            cookies.style.display = 'none';
            document.cookie = "cookies-accepted=True; expires=Wed, 29 Dec 2077 12:00:00 UTC;"; // Utworzenie pliku cookie który sygnalizuje o akceptacji ciasteczek
        });

        document.getElementById('cookie-deny').addEventListener('click', function() {
            window.history.back(); // Jeżeli użytkownik odrzuca ciasteczka to wraca do poprzedniej strony
        });
    }
}