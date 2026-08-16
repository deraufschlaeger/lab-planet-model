```
vdef TransformTXT(txtname):
    data = open(txtname)

    # jede Zeile wird als array in Array H ausgegeben
    Tp = [] # K & GPa
    # jede Spalte wird in ein eigenes Array geschrieben
    rho = [] # in g/cm^3
    E = [] # kJ/g specific internal energy

    liste = data.readlines()
    for i in range(len(liste)):
        a = [float(x) for x in liste[i].split()]
        rho.append(math.log(a[0]))
        Tp.append([math.log(a[1]), math.log(a[2])])
        E.append(math.log(a[3]))

    data.close()

    return rho, Tp, E

...

rho_H, Tp_H, E_H = TransformTXT(EOSFilename)
# Initialisieren Interpolation
interpolator = scipy.interpolate.LinearNDInterpolator(Tp_H, rho_H)

...

math.exp(interpolator([math.log(T[i]),math.log(p[i] / 1e9)])))
```