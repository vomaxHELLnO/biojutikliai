
def draw_matrix(matrix):
    print '  ',
    for j in range(len(matrix[0])):
        print str(j*h)+ ' ',
    print
    for i, row in enumerate(matrix):
        print i*tau, ' '.join(['%.4f' % e for e in row])

def perkelties_metodas(coef):
    CD = []
    for i in range(len(coef)):
        if i == 0:
            C1 = -coef[i][1] / coef[i][0]
            D1 = coef[i][2] / coef[i][0]
            CD.append([C1, D1])
        else:
            Ci = -(coef[i][2]/(coef[i][1] + (CD[-1][0] * coef[i][0])))
            Di = (coef[i][3] - (CD[-1][1] * coef[i][0])) / (coef[i][1]+(CD[-1][0] * coef[i][0]))
            CD.append([Ci, Di])
    Xn = CD[-1][1]
    X = [Xn]
    for j in range(len(coef)-2, -1, -1):
        Xi = CD[j][0] * X[-1] + CD[j][1]
        X.append(Xi)
    print coef
    X.reverse()
    print Xi
    return X

n = 11 # x - koord erdve
m = 10 # y - koord laikas
S0 = 1 # 1 microM = 0,01KM
Ds = 300 # 300 micro m^2/s
Dp = 300 # 300 micro m^2/s
d = 100 # 0.1 mm maksimalus fermento membranos sluoksnis
h = 10 # x kitimo zingsnis x in [0;d]
Km = 100 #100 microM
Vmax = 100 #100 microM/s
tau_diff = [0.5, 1, 3] # delta time
tau = tau_diff[0]

substrate = []

for i in range(m):
    substrate.append([])
    for j in range(n):
        if i == 0:
            substrate[i].append(0)
        else:
            substrate[i].append(None)
        if j == (n - 1):
            substrate[i][j] = S0

    #padaryk coefs!
    if i != 0:
        coef_c = (h * h) / (tau * Ds)
        coef = []
        b1 = -1 - coef_c
        c1 = 1
       # d1 = 0
        d1 = ((h * h) / (Ds * tau)) * (((Vmax * substrate[i-1][1] * tau) / 
            (Km + substrate[i-1][1])) - substrate[i-1][1])
        coef.append([b1,c1,d1])
        for l in range(1, n - 1):
            al = 1
            bl = -2 - coef_c
            cl = 1
            dl = ((h * h) / (Ds * tau)) * (((Vmax * substrate[i-1][l] * tau)
                /(Km + substrate[i-1][l])) - substrate[i-1][l])
            coef.append([al, bl, cl, dl])
        an = 1
        bn = -2 - coef_c
        cn = 0
        dn = -S0
        coef.append([an, bn, cn, dn])

        X = perkelties_metodas(coef)
        substrate[i][0] = X[0]
        for k in range(1, n - 1):
            substrate[i][k] = X[k - 1]



   #     if j == 0:
   #         coeficients.append( )
   #     if 0 < j and j < (n - 1):
   #         coeficients.append()
   #     if j == (n - 1):
   #         coeficients.append()

# print substrate
draw_matrix(substrate)


