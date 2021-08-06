import unicodedata
import timeit

# Variabilele globale ce se reactualizeaza la fiecare test

N = 20  # Dimensiunea tablei NxN
table = [['~' for x in range(N)] for y in range(N)]  # Initializam tabla goala ( cu semnul '~' )
arc_pos = [-1 for x in range(N)]  # Pozitiile de pe coloane pe care se afla arcasii
ok = 0  # Cand gasim solutia corecta, aceasta devine 1
w = 10  # Distanta pana la care pot sa traga arcasii


def startCustomTest (N_tabla, nr_arcasi, distanta_tragere):
    load_custom_test(N_tabla, nr_arcasi, distanta_tragere)
    start = timeit.default_timer()
    searchDFS(0, 1, 'Custom')
    stop = timeit.default_timer()
    file = 'Fisiere_Output\\test' + 'Custom' + '.txt'
    f = open(file, mode='a')
    f.write('Timpul de executie a fost de: ' + str(stop - start) + ' secunde\n')

def startTesting():
    for i in range(1, 11):
        load_test(i)
        start = timeit.default_timer()
        searchDFS(0, 1, i)
        stop = timeit.default_timer()
        file = 'Fisiere_Output\\test' + str(i) + '.txt'
        f = open(file, mode='a')
        f.write('Timpul de executie a fost de: ' + str(stop - start) + ' secunde\n')


def printTable(test):  # Functia care ne afiseaza tabla rezolvata la testul curent
    try:
        file = 'Fisiere_Output\\test' + str(test) + '.txt'
        f = open(file, mode='w')
    except:
        print("ERROR: Can't open the output file")
    else:
        global N
        f.write('Dimensiunea tablei este: ' + str(N) + ' x ' + str(N) + '\n')
        f.write('Distanta pana la care pot trage arcasii pe linii si coloane este: ' + str(w) + '\n')
        if w > 0:
            f.write('Distanta pana la care pot trage arcasii pe diagonale este: ' + str((w//3)*2 + 1) + '\n')
        else:
            f.write('Distanta pana la care pot trage arcasii pe diagonale este: 0 \n')
        for i in range(N):
            for j in range(N):
                f.write(table[i][j] + ' ')
            f.write('\n')
        f.write('\n\n')

        f.write('Arcasii au fost asezati cu succes! ' + '\n')


def searchDFS(index, correct, nr_test):  # functia DFS pentru cautarea arcasilor (aceasta are mai multe verificari ce sunt explicate in raport)
    global ok
    global arc_pos

    if index >= N:
        if check(index):
            if ok == 0:
                print(str(nr_test))
            ok = 1

    if index > 1 and ok == 0:
        if check_last(index):
            correct = 1
        else:
            correct = 0

    if index > 1 and correct == 1 and ok == 0:
        if check(index):
            correct = 1
        else:
            correct = 0

    if index > 0 and correct == 1 and ok == 0:
        if table[arc_pos[index-1]][index-1] == 'Z':
            correct = 0

    if ok == 0 and index < N and correct == 1:
        for col in range(N):
            arc_pos[index] = col
            searchDFS(index + 1, 1, nr_test)


def check_last(index):  # Verificam ultimul arcas introdus cu penultimul
    col_ultimul = index - 2
    col_penultimul = index - 1
    linie_ultimul = arc_pos[col_ultimul]
    linie_penultimul = arc_pos[col_penultimul]
    if threatens(linie_ultimul, col_ultimul, linie_penultimul, col_penultimul):
        return False
    return True


def check(index):  # Verificam toti arcasii introdusi pana acum
    for col_primu in range(index):
        for col_doilea in range(col_primu + 1, index):
            linie_primu = arc_pos[col_primu]
            linie_doilea = arc_pos[col_doilea]
            if threatens(linie_primu, col_primu, linie_doilea, col_doilea):
                return False
    return True


# Verificam daca exista un zid intre 2 arcasi pe aceiasi coloana
def is_wall_col(linie_1, linie_2, coloana):
    for i in range(linie_1, linie_2):
        if table[i][coloana] == 'Z':
            return True
    return False


# Verificam daca exista un zid intre 2 arcasi pe aceiasi linie
def is_wall_linie(coloana_1, coloana_2, linie):
    for i in range(coloana_1, coloana_2):
        if table[linie][i] == 'Z':
            return True
    return False


# Verificam daca exista un zid intre 2 arcasi pe aceiasi diagonala
def is_wall_diag(linie_1, col_1, linie_2, col_2):

    if linie_1 > linie_2:
        ord1 = -1
    else:
        ord1 = 1

    if col_1 > col_2:
        ord2 = -1
    else:
        ord2 = 1

    for i in range(linie_1, linie_2, ord1):
        for j in range(col_1, col_2, ord2):
            if table[i][j] == 'Z':
                return True
    return False


def threatens(linie_i, col_i, linie_j, col_j):  # Verificam daca este o problema in pozitionarea celor 2 arcasi

    if linie_i == linie_j or col_i == col_j or abs(linie_i - linie_j) == abs(col_i - col_j):
        if linie_i == linie_j:                  # Daca arcasii sunt pozitionati pe aceiasi linie verificam daca cumva pot fi totusi pozitionati
            if abs(col_i - col_j) > w:
                return False
            if is_wall_linie(col_i, col_j, linie_i):
                return False
        if col_i == col_j and abs(linie_i - linie_j) > w:
            if abs(linie_i - linie_j) > w:
                return False
            if is_wall_col(linie_i, linie_j, col_i):
                return False
        if abs(linie_i - linie_j) == abs(col_i - col_j):
            if w == 0:                  # Daca distana de tragere este 0, returnam direct ca nu este o problema
                return False
            if abs(col_i - col_j) > ((w//3)*2 + 1):     # Pentru a compensa faptul ca diagonalele sunt mai putine
                return False
            if is_wall_diag(linie_i, col_i, linie_j, col_j):
                return False
        return True
    else:
        return False


# Functia prin care ni se incarca testul respectiv(toate variabilele existente)
def load_custom_test(N_tabla, nr_arcasi, distanta_tragere):
    global N
    N = N_tabla
    N = int(N)
    global w
    w = nr_arcasi
    global table
    table = [['~' for x in range(N)] for y in range(N)]
    global arc_pos
    arc_pos = [-1 for x in range(N)]
    global ok
    ok = 0  # Resetam valoarea ok a testului precedent
    w = distanta_tragere

# Functia prin care ni se incarca testul respectiv(toate variabilele existente)
def load_test(nr_test):
    file = 'Fisiere_Input\\test' + str(nr_test) + '.txt'
    f = open(file, mode='r')
    global N
    N = f.readline()
    N = int(N)
    global w
    w = f.readline()  # Distanta pana la care pot sa traga arcasii
    global table
    table = [['~' for x in range(N)] for y in range(N)]
    global arc_pos
    arc_pos = [-1 for x in range(N)]
    global ok
    ok = 0  # Resetam valoarea ok a testului precedent
    w = f.readline()
    w = int(w)
    nr_ziduri = f.readline()
    for z in range(int(nr_ziduri)):
        aux = f.readline().split()
        table[int(aux[0])][int(aux[1])] = 'Z'       # Punem Z in locurile unde exista un zid


def print(numartest):  # Functia de afisare a tablei
    for i in range(N):
        table[arc_pos[i]][i] = 'A'

    printTable(numartest)

