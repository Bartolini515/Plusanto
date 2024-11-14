# Plik tymczasowy który jest używany do przechowywania algorytmów w czasie wykonywania programu
# Ew. zostanie jako faktyczny plik

#### ZAŁOŻENIA BUDŻETU ####
# Bazujemy budżet na zasadzie 50(wydatki)/30(zachcianki)/15(dodatek czyli inwestycja i spłacanie kredytu)/5(awaryjne) || 50(wydatki)/30(dodatek czyli inwestycja i spłacanie kredytów)/20(awaryjne)
# W przypadku opcji pierwszej stosujemy zasadę 5 przychodów (w koncie awaryjnym trzyma się 5 wartości przychodu)
# Użytkownik może wybrac który budżet chce użyć
# Użytkownika może określić wielkość buforu budżetu wydatkowego (w przypadku planu 2)
# Pytamy czy użytkownik chce rozprowadzić swój balans jeżeli wykryjemy go większego niż 2 wartości przychodu 
# 
#
# 50/30/15/5
# Jeśli wydatki przekraczają budżet wydatkowy, wtedy dajemy komunikat o tym i innymi funduszami pokrywamy niedomiar 
# Jeśli budżet awaryjny jest mniejszy niż 2 wartości przychodu:
#   Jeżeli istnieje dług wtedy połowa dodatku jest przekazywana do awaryjnego 
#   Jeżeli nie ma długu wtedy całość dodatku jest przekazywana do awaryjnego 
# Jeśli budżet awaryjny jest większy od 5 wartości przychodu wtedy przekazujemy każde kolejne do dodatku 
# Jeśli wydatki są mniejsze niż budżet wydatkowy to przekazujemy nadmiar do dodatku 
# Jeśli istnieje dług to spłacamy go z dodatku
# 
# 50/30/20
# Jeśli wydatki przekraczają budżet wydatkowy, wtedy dajemy komunikat o tym i innymi funduszami pokrywamy niedomiar 
# Jeśli wydatki są mniejsze niż budżet wydatkowy to przekazujemy nadmiar do dodatku, lecz pozostawia się (jeśli możliwe) bufor określony przez użytkownika
# Jeśli istnieje dług to spłacamy go z dodatku




# TODO
# Optymalizacja
# Opcja wybrania różnych planów budżetowych
# Kombinowanie z kontem awaryjnym i tym co jeżeli wydatki więcej - wystarczy komunikat i to tyle
# Budżet na wydatki musi mieć więcej i nie oddawać całego nadmiaru aby zaopatrzać niespodziewane małe wydatki
# Użytkownika ma możliwość ustalenia buforu

# TODO może
# Dodanie możliwości wyboru dokładnych wartości budżetu
# Dodanie możliwości wprowadzania różnych typów długów i ich spłacania


def budgetEstablish(value, budgetType):
    match budgetType:
        case 1:
            budgetExpenses = value * 0.5
            budgetWants = value * 0.3
            budgetEmergency = value * 0.05
            allowance = value * 0.15
        case 2:
            budgetExpenses = value * 0.5
            budgetWants = 0
            budgetEmergency = value * 0.20
            allowance = value * 0.30
    return budgetExpenses, budgetWants, budgetEmergency, allowance

def calculateExpensesDeficit(expenses, budgetExpenses, budgetWants, allowance, budgetEmergency, balance, budgetType):
    match budgetType:
        case 1: # W przypadku 50/30/15/5
            difference = expenses - budgetExpenses
            match difference: # Sprawdzamy dla każdej możliwości czy da się załatać lukę
                case difference if (budgetWants - difference) > 0:
                    budgetExpenses += difference
                    budgetWants -= difference
                    print(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z budżetu zachcianek.') # TODO dodaje komunikat o przekroczeniu budżetu na wydatki i pokryciu go budżetem zachcianek
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case difference if (budgetWants + allowance - difference) > 0:
                    budgetExpenses += difference 
                    budgetWants -= difference 
                    allowance -= abs(budgetWants)
                    budgetWants = 0
                    print(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z budżetu zachcianek oraz dodatku.') # TODO dodaje komunikat o przekroczeniu budżetu na wydatki i pokryciu go budżetem zachcianek oraz dodatkiem
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case difference if (budgetWants + allowance + budgetEmergency - difference) > 0:
                    budgetExpenses += difference 
                    budgetWants -= difference 
                    allowance -= abs(budgetWants)
                    budgetEmergency -= abs(allowance)
                    budgetWants, allowance = 0, 0
                    print(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z budżetu zachcianek i dodatku oraz budżetu awaryjnego.') # TODO dodaje komunikat o przekroczeniu budżetu na wydatki i pokryciu go budżetem zachcianek i dodatkiem oraz budżetem awaryjnym
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case difference if balance - abs(budgetWants + allowance + budgetEmergency - difference) > 0:
                    budgetExpenses += difference 
                    budgetWants -= difference 
                    allowance -= abs(budgetWants)
                    budgetEmergency -= abs(allowance)
                    balance -= abs(budgetEmergency)
                    budgetWants, allowance, budgetEmergency = 0, 0, 0
                    print(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z budżetu zachcianek, dodatku, budżetu awaryjnego oraz obecnego balansu konta.') # TODO dodaje komunikat o przekroczeniu budżetu na wydatki i pokryciu go budżetem zachcianek, dodatkiem, budżetem awaryjnym oraz balansem konta
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case _:
                    # TODO Czy coś tu dodać aby robiło gdy nie ma wystarczających środków?
                    print(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference}, pokrycie nie jest możliwe. Brakująca ilość: {balance - abs(budgetWants + allowance + budgetEmergency - difference)}.') # TODO dodaje komunikat o przekroczeniu budżetu na wydatki i braku możliwości pokrycia go
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                    
        case 2: # W przypadku 50/30/20
            difference = expenses - budgetExpenses
            match difference: # Sprawdzamy dla każdej możliwości czy da się załatać lukę
                case difference if (allowance - difference) > 0:
                    budgetExpenses += difference 
                    allowance -= difference
                    print(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z dodatku.') # TODO dodaje komunikat o przekroczeniu budżetu na wydatki i pokryciu go dodatkiem
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case difference if (allowance + budgetEmergency - difference) > 0:
                    budgetExpenses += difference 
                    allowance -= difference
                    budgetEmergency -= abs(allowance)
                    allowance = 0
                    print(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z dodatku i budżetu awaryjnego.') # TODO dodaje komunikat o przekroczeniu budżetu na wydatki i pokryciu go dodatkiem i budżetem awaryjnym
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case difference if balance - abs(allowance + budgetEmergency - difference) > 0:
                    budgetExpenses += difference 
                    allowance -= difference
                    budgetEmergency -= abs(allowance)
                    balance -= abs(budgetEmergency)
                    allowance, budgetEmergency = 0, 0, 
                    print(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z dodatku, budżetu awaryjnego oraz obecnego balansu konta.') # TODO dodaje komunikat o przekroczeniu budżetu na wydatki i pokryciu go dodatkiem, budżetem awaryjnym oraz balansem konta
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case _:
                    # TODO Czy coś tu dodać aby robiło gdy nie ma wystarczających środków?
                    print(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference}, pokrycie nie jest możliwe. Brakująca ilość: {balance - abs(budgetWants + allowance + budgetEmergency - difference)}.') # TODO dodaje komunikat o przekroczeniu budżetu na wydatki i braku możliwości pokrycia go
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
    

    
# TODO porozdzielać wszystko na funkcje
def budgetRule(balance, income, expenses, debt, emergencyFund, budgetType):
    # TODO jakoś to rozwikłać aby dodawało wszystkie komunikaty i potem wyświetlało je w takim jednym miejscu, ale to już bardziej dla frontendu zadanie
    budgetExpenses, budgetWants, budgetEmergency, allowance = budgetEstablish(income, budgetType)
    repayDebt = 0
    
    if balance > income*2: # Sprawdza balans, jeżeli powyżej 2 wartości przychodu to pyta użytkownika czy chce rozprowadzić
        print('Posiadasz balans powyżej 2 wartości przychodu, czy chcesz rozprowadzić nadmiar do budżetu?') # TODO dodaje komunikat o nadmiarze w balansie i czy użytkownik chce go rozprowadzić
        if input('Tak/Nie: ').lower() == 'tak': # TODO zastapić faktycznym sposobem sprawdzania
            difference = balance - (income * 2)
            balance -= difference
            budgetExpenses, budgetWants, budgetEmergency, allowance += budgetEstablish(difference, budgetType)
    
    if expenses > budgetExpenses: # Sprawdza czy wydatki przekraczają budżet na wydatki, jeżeli tak to stara się załatać lukę
        budgetExpenses, budgetWants, budgetEmergency, allowance, balance = calculateExpensesDeficit(expenses, budgetExpenses, budgetWants, allowance, budgetEmergency, balance, budgetType)
    elif (difference := budgetExpenses - expenses) > 800: # W przeciwnym razie dodaje nadmiar do dodatku ale zostawia 800 jeśli to możliwe, jeśli nie to zostawia jak jest
        difference -= 800
        budgetExpenses -= difference
        allowance += difference
        print(f'Posiadasz nadmiar w budżecie wydatkowym, w wysokości {difference}, nadmiar przekazany został do dodatku.') # TODO dodaje komunikat o nadmiarze w budżecie wydatkowym i przekazaniu go do dodatku


    match budgetType:
        case 1:
            if emergencyFund > income * 5: # W przypadku jeżeli posiadamy fundusz awaryjny o wielkości powyżej 5 miesięcznych przychodów dodajemy jego składki na inwestycje
                allowance += budgetEmergency
                print(f'Fundusz awaryjny jest powyżej 5 wartości przychodu, budżet awaryjny został przekazany do dodatku.') # TODO dodaje komunikat o przekazaniu budżetu awaryjnego do dodatku
            elif emergencyFund < income * 2: # W przypadku jeżeli posiadamy fundusz awaryjny o wielkości mniejszej niż 2 miesięczne przychody przekazujemy połowę dodatku na budżet awaryjny
                if debt: # Jeżeli istnieje dług to przekazujemy pół dodateku na budżet awaryjny, a drugie na spłate długu
                    halfAllowance = 0.5 * allowance
                    allowance = 0
                    budgetEmergency += halfAllowance
                    repayDebt += halfAllowance
                    print(f'Fundusz awaryjny jest poniżej 2 wartości przychodu, połowa dodatku o wartości {halfAllowance} została przekazana na budżet awaryjny. Pozostała część posłuży spłaceniu długu.') # TODO dodaje komunikat o przekazaniu połowy dodatku na budżet awaryjny, drugiej na spłacenie długu
                else:
                    budgetEmergency += allowance
                    allowance = 0
                    print(f'Fundusz awaryjny jest poniżej 2 wartości przychodu, dodatek został przekazany na budżet awaryjny.') # TODO dodaje komunikat o przekazaniu dodatku na budżet awaryjny.


    if debt and allowance: # Jeżeli istnieje dług oraz dodatek to przekazujemy dodatek na spłacenie długu
        repayDebt += allowance
        allowance = 0
        difference = debt - repayDebt
        if difference > 0:
            debt -= repayDebt
            print(f'Spłacono część długu kwotą {repayDebt} za pomocą dodatku. Pozostały dług to {debt}') # TODO dodaje komunikat o przekazaniu dodatku na spłatę długu.
        else: # Jeżeli dług został spłacony w całości wtedy usuwamy dług oraz dodajemy resztę do dodatku
            debt = 0
            allowance += abs(difference)
            print(f'Cały dług w wysokości {debt} został spłacony za pomocą dodatku. Pozostały dodatek to {allowance}') # TODO dodaje komunikat o spłacie całego długu.