# Plik tymczasowy który jest używany do przechowywania algorytmów w czasie wykonywania programu
# Ew. zostanie jako faktyczny plik

#### ZAŁOŻENIA BUDŻETU ####
# Istnieją 2 plany budżetowe stabilny: 50(wydatki)/30(zachcianki)/15(dodatek)/5(awaryjne) || rozwojowy: 50(wydatki)/30(dodatek)/20(awaryjne)
# Użytkownik może wybrać który budżet chce użyć jako fundamentu, a następnie może dostosować wielkości poszczególnych części budżetu, lecz wydatki pozostają niezmienione
# Użytkownik może określić wielkość buforu budżetu wydatkowego (w przypadku planu 2)
# Użytkownik może określić planowany budżet awaryjny w przypadku planu 1
# Budżety mają swoje unikalne właściwości, to jak działają opisane jest w każdym parametrze na stronie
# Pytamy czy użytkownik chce rozprowadzić swoje saldo jeżeli wykryjemy go większego niż 2 wartości dochodu
# Dodatek wykorzystywany jest m.in. do spłacania długów oraz inwestycji
#
# 50/30/15/5
# Jeśli wydatki przekraczają budżet wydatkowy, wtedy dajemy komunikat o tym i innymi budżetami pokrywamy niedomiar 
# Jeśli budżet awaryjny jest mniejszy niż 40% planowanego funduszu awaryjnego:
#   Jeżeli istnieje dług wtedy połowa dodatku jest przekazywana do awaryjnego 
#   Jeżeli nie ma długu wtedy całość dodatku jest przekazywana do awaryjnego 
# Jeśli planowany fundusz awaryjny został osiągnięty, wtedy przekazujemy każde kolejne budżety awaryjne do dodatku 
# Jeśli wydatki są mniejsze niż budżet wydatkowy to przekazujemy nadmiar do dodatku 
# Jeśli istnieje dług to spłacamy go z dodatku
# 
# 50/30/20
# Jeśli wydatki przekraczają budżet wydatkowy, wtedy dajemy komunikat o tym i innymi budżetami pokrywamy niedomiar 
# Jeśli wydatki są mniejsze niż budżet wydatkowy to przekazujemy nadmiar do dodatku, lecz pozostawia się (jeśli możliwe) bufor określony przez użytkownika
# Jeśli istnieje dług to spłacamy go z dodatku




# TODO
# Optymalizacja
# Opcja wybrania różnych planów budżetowych
# Kombinowanie z kontem awaryjnym i tym co jeżeli wydatki więcej - wystarczy komunikat i to tyle
# Budżet na wydatki musi mieć więcej i nie oddawać całego nadmiaru aby zaopatrzać niespodziewane małe wydatki
# Użytkownik ma możliwość ustalenia buforu
# Dodanie możliwości wyboru dokładnych wartości budżetu
# Lepsze opisanie wszystkiego oraz przeniesienie do takiego poradnika typu help
# Dodanie możliwości dla użytkownika definiowania wielkości maksymalnego funduszu awaryjnego w przypadku pierwszej opcji
# 5 przychodów będzie tylko sugestią w helpie
# Zamienić przychód na dochód bo kwestia definicji
# Zamienić balansy na salda

# Jezeli budżet emergency jest taki jak planowany wtedy reszta do dodatku bo mamy planowany | done
# procenty sie nie zmieniaja gdy zmiana typu | done
# wyeliminować floaty | done
# > Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości 2.0, pokrycie nie jest możliwe. Brakująca ilość: 0.0. | done


# TODO może
# Dodanie możliwości wprowadzania różnych typów długów i ich spłacania

import math


def createMessage(message): # Funkcja tworzenia komunikatów
    messagesArray.append(message)


def budgetEstablish(value, budgetType, percentWants, percentAllowance, percentEmergency): # Funckja ustalania budżetu
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


def budgetAdd(value, budgetType, budgetExpenses, budgetWants, budgetEmergency, allowance, percentWants, percentAllowance, percentEmergency): # Funcja dodawania do budżetu kolejnych wartości odpowiednio rozdzielonych
    budgetExpensesTemp, budgetWantsTemp, budgetEmergencyTemp, allowanceTemp = budgetEstablish(value, budgetType, percentWants, percentAllowance, percentEmergency)
    budgetExpenses, budgetWants, budgetEmergency, allowance = budgetExpenses + budgetExpensesTemp, budgetWants + budgetWantsTemp, budgetEmergency + budgetEmergencyTemp, allowance + allowanceTemp
    return budgetExpenses, budgetWants, budgetEmergency, allowance


def calculateExpensesDeficit(expenses, budgetExpenses, budgetWants, allowance, budgetEmergency, balance, budgetType):
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
                    allowance, budgetEmergency = 0, 0, 
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference} pokryte zostały z dodatku, budżetu awaryjnego oraz obecnego salda.')
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
                
                case _:
                    # TODO Czy coś tu dodać aby robiło gdy nie ma wystarczających środków?
                    createMessage(f'Przekraczasz budżet na wydatki, dodatkowe koszty w wysokości {difference}, pokrycie nie jest możliwe. Brakująca ilość: {balance - abs(budgetWants + allowance + budgetEmergency - difference)}.')
                    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
         
                
def distributeBalance(balance, income, budgetType, budgetExpenses, budgetWants, budgetEmergency, allowance, percentWants, percentAllowance, percentEmergency): # Funkcja rozprowadzająca saldo
    difference = balance - (income * 2)
    balance -= abs(difference)
    budgetExpenses, budgetWants, budgetEmergency, allowance = budgetAdd(abs(difference), budgetType, budgetExpenses, budgetWants, budgetEmergency, allowance, percentWants, percentAllowance, percentEmergency)
    createMessage(f'Nadmiar w saldzie został rozprowadzony w wysokości {abs(difference)}')
    return budgetExpenses, budgetWants, budgetEmergency, allowance, balance
     
        
def distributeFund(emergencyFund, plannedEmergencyFund, allowance, budgetEmergency, debt, repayDebt): # Funkcja rozprowadzająca fundusz
    if emergencyFund >= plannedEmergencyFund: # W przypadku jeżeli posiadamy fundusz awaryjny powyżej planowanego, dodajemy jego składki do dodatku
        allowance += budgetEmergency
        createMessage(f'Fundusz awaryjny jest powyżej planowanego funduszu, budżet awaryjny został przekazany do dodatku.')
    
    else: # W przypadku jeżeli posiadamy fundusz awaryjny o wielkości mniejszej niż 40% planowanego przekazujemy połowę dodatku na budżet awaryjny
        if debt: # Jeżeli istnieje dług to przekazujemy pół dodateku na budżet awaryjny, a drugie na spłate długu
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
    

def debtRepayment(repayDebt, allowance, debt): # Funkcja spłacania długu
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


def checkEmergencyBudget(emergencyFund, plannedEmergencyFund, budgetEmergency, allowance): # Funkcja sprawdzająca czy budżet awaryjny jest nadto planowany
    difference = plannedEmergencyFund - emergencyFund
    
    if (difference2 := difference - budgetEmergency) < 0:
        allowance += abs(difference2)
        budgetEmergency = difference
        createMessage(f'Twój budżet awaryjny przekraczał planowany, został odpowiednio skorygowany przekazując {abs(difference2)} do dodatku.')
    return budgetEmergency, allowance
    
    
    
    
def budgetRule(balance, income, expenses, debt, emergencyFund, budgetType, bufor, percentWants, percentAllowance, percentEmergency, plannedEmergencyFund, distributeConf):
    balance, income, expenses, debt, emergencyFund, bufor, percentWants, percentAllowance, percentEmergency, plannedEmergencyFund = int(balance), int(income), int(expenses), int(debt), int(emergencyFund), int(bufor), int(percentWants), int(percentAllowance), int(percentEmergency), int(plannedEmergencyFund)
    repayDebt = 0
    
    global messagesArray
    messagesArray = []
    
    budgetExpenses, budgetWants, budgetEmergency, allowance = budgetEstablish(income, budgetType, percentWants, percentAllowance, percentEmergency)
    
    if distributeConf: # Sprawdza saldo, jeżeli powyżej 2 wartości dochodu to pyta użytkownika czy chce rozprowadzić
        budgetExpenses, budgetWants, budgetEmergency, allowance, balance = distributeBalance(balance, income, budgetType, budgetExpenses, budgetWants, budgetEmergency, allowance, percentWants, percentAllowance, percentEmergency)

    if expenses > budgetExpenses: # Sprawdza czy wydatki przekraczają budżet na wydatki, jeżeli tak to stara się załatać lukę
        budgetExpenses, budgetWants, budgetEmergency, allowance, balance = calculateExpensesDeficit(expenses, budgetExpenses, budgetWants, allowance, budgetEmergency, balance, budgetType)
    elif (difference := budgetExpenses - expenses) > bufor: # W przeciwnym razie dodaje nadmiar do dodatku ale zostawia bufor jeśli to możliwe, jeśli nie to zostawia jak jest
        difference -= bufor # TODO Bufor musi zostać określony na 0, nwm o co mi chodziło więc zostawie to tu
        budgetExpenses -= difference
        allowance += difference
        createMessage(f'Posiadasz nadmiar w budżecie wydatkowym, w wysokości {difference}, nadmiar przekazany został do dodatku.')

    if budgetType == '1' and (emergencyFund > plannedEmergencyFund or emergencyFund < plannedEmergencyFund * 0.4): # Jeżeli mamy typ budżetu 1 i fundusz awaryjny spełnia któreś z warunków to rozprowadza fundusz
        allowance, budgetEmergency, repayDebt = distributeFund(emergencyFund, plannedEmergencyFund, allowance, budgetEmergency, debt, repayDebt)
    else:
        budgetEmergency, allowance = checkEmergencyBudget(emergencyFund, plannedEmergencyFund, budgetEmergency, allowance)

    if (debt and allowance) or repayDebt: # Jeżeli istnieje dług oraz dodatek, lub spłata długu to przekazujemy dodatek na spłacenie długu
        allowance, debt = debtRepayment(repayDebt, allowance, debt)
        
    return balance, budgetExpenses, budgetWants, allowance, budgetEmergency, debt, messagesArray
