function checkAlerts(messages, levels) {
    alertBox = document.getElementsByClassName("alert")[0] // Wybiera pierwszy element, czyli jedyny, z klasy "alert"
    const error_messages = [];
    const success_messages = [];

    messages.forEach((message, i) => { // Dopisuje do odpowiadającej tablicy każdą wiadomość (dodatkowe levele na potencjalne rozszerzenie)
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
        alertBox.appendChild(ul); 
    };
};