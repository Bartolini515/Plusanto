#### ZAŁOŻENIA BUDŻETU ####
# Istnieją 2 plany budżetowe stabilny: 50(wydatki)/30(zachcianki)/15(dodatek)/5(awaryjne) || rozwojowy: 50(wydatki)/30(dodatek)/20(awaryjne)
# Użytkownik może wybrać który budżet chce użyć jako fundamentu, a następnie może dostosować wielkości poszczególnych części budżetu, lecz wydatki pozostają niezmienione
# Użytkownik może określić wielkość buforu budżetu wydatkowego (w przypadku budżetu rozwojowego, budżet stabilny posiada od tego zachcianki)
# Użytkownik może określić planowany budżet awaryjny
# Budżety mają swoje unikalne właściwości, to jak działają opisane jest w każdym parametrze na stronie
# Użytkownik może rozprowadzić swoje saldo jeżeli jest ono większe niż 2 wartości dochodu
# Dodatek wykorzystywany jest m.in. do spłacania długów
# 
# 
## Obowiązujące dla obu budżetów ##
# Jeśli wydatki przekraczają budżet wydatkowy, wtedy innymi budżetami pokrywamy niedomiar 
# Jeśli planowany fundusz awaryjny został osiągnięty, wtedy przekazujemy każde kolejne budżety awaryjne do dodatku 
# Jeśli wydatki są mniejsze niż budżet wydatkowy to przekazujemy nadmiar do dodatku
# Jeśli istnieje dług to spłacamy go z dodatku
#
## Stabilny (50/30/15/5) ##
# Posiada zachcianki
# Jeśli budżet awaryjny jest mniejszy niż 40% planowanego funduszu awaryjnego:
#   Jeżeli istnieje dług wtedy połowa dodatku jest przekazywana do awaryjnego 
#   Jeżeli nie ma długu wtedy całość dodatku jest przekazywana do awaryjnego 
# 
## Rozwojowy (50/30/20) ##
# Posiada bufor który jest dodatkową wartością dodawaną do wydatków służy jako zabezpieczenie przed nagłymi małymi wydatkami
# Pozostawia się (jeśli możliwe) bufor określony przez użytkownika, nawet jeżeli budżet wydatkowy przekazywany jest na dodatek




# TODO
# Lepsze opisanie wszystkiego oraz przeniesienie do takiego poradnika typu help
# 5 przychodów będzie tylko sugestią w helpie


# TODO może
# Dodanie możliwości wprowadzania różnych typów długów i ich spłacania

import math


# Funkcja tworzenia komunikatów
def createMessage(message:str):
    messagesArray.append(message)


# Funkcja ustalania budżetu
def budgetEstablish(value:int, budgetType, percentWants:int, percentAllowance:int, percentEmergency:int): 
    percentWants, percentEmergency, percentAllowance = percentWants / 100, percentEmergency / 100, percentAllowance / 100
    match budgetType:
        case '1':
            budgetExpenses = math.ceil(value * 0.5)
            budgetWants = math.ceil(value * percentWants)
            budgetEmergency = math.ceil(value * percentEmergency)
            allowance = math.ceil(value * percentAllowance)
        case '2':
            budgetExpenses = math.ceil(value * 0.5)
            budgetWants = 0
            budgetEmergency = math.ceil(value * percentEmergency)
            allowance = math.ceil(value * percentAllowance)
    return budgetExpenses, budgetWants, budgetEmergency, allowance


# Funkcja rozprowadzania dodatkowej wartości do istniejącego już budżetu
def budgetAdd(value:int, budgetType, budgetExpenses:int, budgetWants:int, budgetEmergency:int, allowance:int, percentWants:int, percentAllowance:int, percentEmergency:int): # Funkcja dodawania do budżetu kolejnych wartości odpowiednio rozdzielonych
    budgetExpensesTemp, budgetWantsTemp, budgetEmergencyTemp, allowanceTemp = budgetEstablish(value, budgetType, percentWants, percentAllowance, percentEmergency)
    budgetExpenses, budgetWants, budgetEmergency, allowance = budgetExpenses + budgetExpensesTemp, budgetWants + budgetWantsTemp, budgetEmergency + budgetEmergencyTemp, allowance + allowanceTemp
    return budgetExpenses, budgetWants, budgetEmergency, allowance


# Funkcja obliczania i łatania deficitu w budżecie wydatkowym
def calculateExpensesDeficit(expenses:int, budgetExpenses:int, budgetWants:int, allowance:int, budgetEmergency:int, balance:int, budgetType):
    match budgetType:
        case '1': # W przypadku 50/30/15/5
            difference = expenses - budgetExpenses
            match difference: # Sprawdzamy dla każdej możliwości czy da się załatać lukę
                case difference if (budgetWants - difference) >= 0:
                    budgetExpenses += difference
                    budgetWants -= difference
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z budżetu zachcianek.')
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case difference if (budgetWants + allowance - difference) >= 0:
                    budgetExpenses += difference 
                    budgetWants -= difference 
                    allowance -= abs(budgetWants)
                    budgetWants = 0
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z budżetu zachcianek oraz dodatku.')
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case difference if (budgetWants + allowance + budgetEmergency - difference) >= 0:
                    budgetExpenses += difference 
                    budgetWants -= difference 
                    allowance -= abs(budgetWants)
                    budgetEmergency -= abs(allowance)
                    budgetWants, allowance = 0, 0
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z budżetu zachcianek i dodatku oraz budżetu awaryjnego.')
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case difference if balance - abs(budgetWants + allowance + budgetEmergency - difference) >= 0:
                    budgetExpenses += difference 
                    budgetWants -= difference 
                    allowance -= abs(budgetWants)
                    budgetEmergency -= abs(allowance)
                    balance -= abs(budgetEmergency)
                    budgetWants, allowance, budgetEmergency = 0, 0, 0
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z budżetu zachcianek, dodatku, budżetu awaryjnego oraz obecnego salda.')
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case _:
                    # TODO Czy coś tu dodać aby robiło gdy nie ma wystarczających środków?
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference}, pokrycie nie jest możliwe. Brakująca ilość: {balance - abs(budgetWants + allowance + budgetEmergency - difference)}.')
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance

                    
        case '2': # W przypadku 50/30/20
            difference = expenses - budgetExpenses
            match difference: # Sprawdzamy dla każdej możliwości czy da się załatać lukę
                case difference if (allowance - difference) >= 0:
                    budgetExpenses += difference 
                    allowance -= difference
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z dodatku.')
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case difference if (allowance + budgetEmergency - difference) >= 0:
                    budgetExpenses += difference 
                    allowance -= difference
                    budgetEmergency -= abs(allowance)
                    allowance = 0
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z dodatku i budżetu awaryjnego.')
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case difference if balance - abs(allowance + budgetEmergency - difference) >= 0:
                    budgetExpenses += difference 
                    allowance -= difference
                    budgetEmergency -= abs(allowance)
                    balance -= abs(budgetEmergency)
                    allowance, budgetEmergency = 0, 0
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z dodatku, budżetu awaryjnego oraz obecnego salda.')
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case _:
                    # TODO Czy coś tu dodać aby robiło gdy nie ma wystarczających środków?
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference}, pokrycie nie jest możliwe. Brakująca ilość: {balance - abs(budgetWants + allowance + budgetEmergency - difference)}.')
                    global lackingFunds
                    lackingFunds = True
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                
# Funkcja rozprowadzająca saldo
def distributeBalance(balance, income, budgetType, budgetExpenses, budgetWants, budgetEmergency, allowance, percentWants, percentAllowance, percentEmergency):
    difference = balance - (income * 2)
    balance -= abs(difference)
    budgetExpenses, budgetWants, budgetEmergency, allowance = budgetAdd(abs(difference), budgetType, budgetExpenses, budgetWants, budgetEmergency, allowance, percentWants, percentAllowance, percentEmergency)
    createMessage(f'Nadmiar w saldzie został rozprowadzony w wysokości {abs(difference)}')
    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance


# Funkcja rozprowadzająca fundusz
def distributeFund(emergencyFund:int, plannedEmergencyFund:int, allowance:int, budgetEmergency:int, debt:int, repayDebt:int):
    if emergencyFund > plannedEmergencyFund: # W przypadku jeżeli posiadamy fundusz awaryjny powyżej planowanego, dodajemy jego składki do dodatku
        allowance += budgetEmergency
        budgetEmergency = 0
        createMessage(f'Fundusz awaryjny jest powyżej planowanego funduszu, budżet awaryjny został przekazany do dodatku.')
    
    else: # W przypadku jeżeli posiadamy fundusz awaryjny o wielkości mniejszej niż 40% planowanego przekazujemy połowę dodatku na budżet awaryjny
        if debt: # Jeżeli istnieje dług to przekazujemy pół dodatku na budżet awaryjny, a drugie na spłate długu
            halfAllowance = math.ceil(0.5 * allowance)
            allowance = 0
            budgetEmergency += halfAllowance
            repayDebt += halfAllowance
            createMessage(f'Fundusz awaryjny jest poniżej 2 wartości przychodu, połowa dodatku o wartości {halfAllowance} została przekazana na budżet awaryjny. Pozostała część posłuży spłaceniu długu.')
        else:
            budgetEmergency += allowance
            allowance = 0
            createMessage(f'Fundusz awaryjny jest poniżej 2 wartości przychodu, dodatek został przekazany na budżet awaryjny.')
    return allowance, budgetEmergency, repayDebt


# Funkcja rozprowadzająca nadmiar budżetu wydatkowego
def distributeExpenses(budgetExpenses:int, expenses:int, allowance:int, bufor:int, budgetType):
    difference = budgetExpenses - expenses
    match budgetType: # w zależności od typu budżetu wlicza w obliczenia bufor bądź nie
        case '1':
            budgetExpenses -= difference
            allowance += difference
            createMessage(f'Posiadasz nadmiar w budżecie wydatkowym, w wysokości {difference}, nadmiar przekazany został do dodatku.')
            return budgetExpenses, allowance
        
        case '2':
            if difference > bufor:
                difference -= bufor
                budgetExpenses -= difference
                allowance += difference
                createMessage(f'Posiadasz nadmiar w budżecie wydatkowym, w wysokości {difference}, nadmiar przekazany został do dodatku.')
            return budgetExpenses, allowance
    

# Funkcja spłacania długu
def debtRepayment(repayDebt:int, allowance:int, debt:int):
    repayDebt += allowance
    debtActual = debt
    allowance = 0
    difference = debt - repayDebt
    if difference > 0:
        debt -= repayDebt
        createMessage(f'Spłacono część długu kwotą {repayDebt} za pomocą dodatku. Pozostały dług to {debt}')
    else: # Jeżeli dług został spłacony w całości wtedy usuwamy dług oraz dodajemy resztę do dodatku
        debt = 0
        allowance += abs(difference)
        createMessage(f'Cały dług w wysokości {debtActual} został spłacony za pomocą dodatku. Pozostały dodatek to {allowance}')
    return allowance, debt


# Funkcja sprawdzająca czy budżet awaryjny jest nadto planowany
def checkEmergencyBudget(emergencyFund:int, plannedEmergencyFund:int, budgetEmergency:int, allowance:int):
    difference = plannedEmergencyFund - emergencyFund
    
    if ((difference2 := difference - budgetEmergency) < 0):
        allowance += abs(difference2)
        budgetEmergency = difference
        createMessage(f'Twój budżet awaryjny przekraczał planowany, został odpowiednio skorygowany przekazując {abs(difference2)} do dodatku.')
    return budgetEmergency, allowance
    
    
    
    
# Funkcja główna budżetu
def budgetRule(balance:int, income:int, expenses:int, debt:int, emergencyFund:int, budgetType, bufor:int, percentWants:int, percentAllowance:int, percentEmergency:int, plannedEmergencyFund:int, distributeConf:int):
    repayDebt = 0
    
    global lackingFunds
    lackingFunds = False
    
    global messagesArray
    messagesArray = []
    
    budgetExpenses, budgetWants, budgetEmergency, allowance = budgetEstablish(income, budgetType, percentWants, percentAllowance, percentEmergency)
    
    if distributeConf: # Sprawdza czy użytkownik chciał rozprowadzić saldo
        budgetExpenses, budgetWants, budgetEmergency, allowance, balance = distributeBalance(balance, income, budgetType, budgetExpenses, budgetWants, budgetEmergency, allowance, percentWants, percentAllowance, percentEmergency)

    if expenses > budgetExpenses: # Sprawdza czy wydatki przekraczają budżet na wydatki, jeżeli tak to stara się załatać lukę
        budgetExpenses, budgetWants, budgetEmergency, allowance, balance = calculateExpensesDeficit(expenses, budgetExpenses, budgetWants, allowance, budgetEmergency, balance, budgetType)
    else: # Jeżeli jest nadmiar to go rozprowadza
        budgetExpenses, allowance = distributeExpenses(budgetExpenses, expenses, allowance, bufor, budgetType)

    if emergencyFund > plannedEmergencyFund or (budgetType == '1' and emergencyFund < plannedEmergencyFund * 0.4): # Jeżeli mamy typ budżetu 1 i fundusz awaryjny jest poniżej 40% planowanego albo jeżeli fundusz awaryjny jest powyżej planowanego to rozprowadza fundusz
        allowance, budgetEmergency, repayDebt = distributeFund(emergencyFund, plannedEmergencyFund, allowance, budgetEmergency, debt, repayDebt)
    else:
        budgetEmergency, allowance = checkEmergencyBudget(emergencyFund, plannedEmergencyFund, budgetEmergency, allowance)

    if (debt and allowance) or repayDebt: # Jeżeli istnieje dług oraz dodatek, lub spłata długu to przekazujemy dodatek na spłacenie długu
        allowance, debt = debtRepayment(repayDebt, allowance, debt)
        
    return balance, budgetExpenses, budgetWants, allowance, budgetEmergency, debt, messagesArray, lackingFunds




### SEKCJA PRZYSTĘPNOŚCIOMIERZA ###

# Funkcja zajmująca się obliczaniem wydatku gdy jest on jednorazowy
def singleExpense(balance, budgetWants, allowance, expense, budgetType, canDo):
    match budgetType:
        case '1':
            if (difference := budgetWants - expense) >= 0:
                createMessage(f'Twój wydatek w wysokości {expense} może zostać pokryty z budżetu na zachcianki. Zostanie ci wtedy {difference} budżetu zachciankowego.')
                return balance, difference, allowance, canDo # difference staje sie nowym budżetem na zachcianki
            elif (difference := allowance - expense) >= 0:
                createMessage(f'Twój wydatek w wysokości {expense} może zostać pokryty z dodatku. Zostanie ci wtedy {difference} dodatku.')
                return balance, budgetWants, difference, canDo # difference staje sie nowym dodatkiem
            elif (difference := balance - expense) >= 0:
                createMessage(f'Twój wydatek w wysokości {expense} może zostać pokryty z salda. Zostanie ci wtedy {difference} salda.')
                return difference, budgetWants, allowance, canDo # difference staje sie nowym saldem
            else:
                createMessage(f'Twój wydatek w wysokości {expense} nie może zostać pokryty z budżetu na zachcianki ani z dodatku, ani z salda. Brakująca wartość wynosi {expense - (allowance + balance + budgetWants)}.')
                canDo = '0'
                return balance, budgetWants, allowance, canDo
        case '2':
            if (difference := allowance - expense) >= 0:
                createMessage(f'Twój wydatek w wysokości {expense} może zostać pokryty z dodatku. Zostanie ci wtedy {difference} dodatku.')
                return balance, budgetWants, difference, canDo # difference staje sie nowym dodatkiem
            elif (difference := balance - expense) >= 0:
                createMessage(f'Twój wydatek w wysokości {expense} może zostać pokryty z salda. Zostanie ci wtedy {difference} salda.')
                return difference, budgetWants, allowance, canDo # difference staje sie nowym saldem
            else:
                createMessage(f'Twój wydatek w wysokości {expense} nie może zostać pokryty z dodatku ani z salda. Brakująca wartość wynosi {expense - (allowance + balance)}.')
                canDo = '0'
                return balance, budgetWants, allowance, canDo




# Funkcja główna przystępniościomierza
def affordabilityRule(income, balance, budgetExpenses, budgetWants, allowance, expense, frequency, budgetType):
    global messagesArray
    messagesArray = []
    
    canDo = '1'
    
    match frequency:
        case '1':
            balance, budgetWants, allowance, canDo = singleExpense(balance, budgetWants, allowance, expense, budgetType, canDo)
        case '2' | '3':
            if frequency == '3':
                expense = math.ceil(expense / 12) # W przypadku wydatku rocznego zostaje on rozłożony na 12 miesięcy
            fullBudgetExpenses = math.ceil(income * 0.5)
            if fullBudgetExpenses - budgetExpenses >= expense:
                budgetExpenses += expense
                createMessage(f'Twój wydatek w wysokości {expense} (wartość miesięczna) może zostać wpisany w budżet wydatkowy. Budżet wydatkowy wyniesie wtedy {budgetExpenses}.')
            else:
                createMessage(f'Twój wydatek w wysokości {expense} (wartość miesięczna) nie może zostać wpisany w budżet wydatkowy. Brakująca wartość wynosi {expense - (fullBudgetExpenses - budgetExpenses)}.')
                canDo = '0'
    return balance, budgetExpenses, budgetWants, allowance, canDo, messagesArray