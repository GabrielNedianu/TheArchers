import random as r


def genereaza():
    for i in range(1, 5):       #Teste mici
        generator(i, 2*i, 4*i)
    for i in range(5, 9):       #Teste medii si mari
        generator(i, 10*i, 40*i)
    for i in range(9, 11):      #Teste foarte mari
        generator(i, 40*i, 70*i)


# Generatorul principal care genereaza toate variabilele problemei apoi generaza si zidurile si scrie totul in fisierele
#    de input
def generator(nr_test, dimensiune_start, dimensiune_stop):
    dimensiune = r.randint(dimensiune_start, dimensiune_stop)
    arcasi = r.randint(dimensiune, 2 * dimensiune)
    punct_tragere = r.randint(dimensiune // 20, dimensiune)
    nr_ziduri = r.randint(dimensiune // 3, (dimensiune // 3) * 2)
    nume_fisiere_input_test = 'Fisiere_Input\\test' + str(nr_test) + '.txt'

    f = open(nume_fisiere_input_test, mode='w')
    f.write(str(dimensiune)+'\n')
    f.write(str(arcasi) + '\n')
    f.write(str(punct_tragere) + '\n')
    f.write(str(nr_ziduri) + '\n')
    generator_ziduri(nr_ziduri, dimensiune, f)
    f.close()


# Aici se genereaza zidurile in functie de dimensiunea tablei si sunt scrise pe cate un rand in fisier
def generator_ziduri(nr_ziduri, N, f):
    used = []
    nr_ziduri_plasat = nr_ziduri
    for i in range(N):
        used.append(False)

    while nr_ziduri_plasat:
        col = r.randint(0, N - 1)
        if not used[col]:                           # Am considerat ca vom aseza cate un zid pe cate o coloana aleasa aleator
            lin = r.randint(0, N - 1)
            f.write(str(lin)+' '+str(col)+'\n')
            nr_ziduri_plasat = nr_ziduri_plasat - 1
            used[col] = True
