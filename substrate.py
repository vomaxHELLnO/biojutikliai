
def draw_matrix(matrix):
    print '  ',
    for j in range(len(matrix[0])):
        print str(j)+ ' ',
    print
    for i, row in enumerate(matrix):
        print i, row

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
    print X
    return X 

n = 5 # x - koord
m = 5 # y - koord
S0 = 1 # 1 microM = 0,01KM
Ds = 300 # micro m^2/s
Dp = 300 # micro m^2/s
d = 0.1 # mm maksimalus fermento membranos sluoksnis
h = 0.01 # x kitimo zingsnis x in [0;d]
Km = 100 # microM
Vmax = 100 # microM/s
d = 0 # tristrizainiu matricu lygties reiksme x1 + x2 = d.
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
        d1 = 0
        coef.append([b1,c1,d1])
        for l in range(1, n - 1):
            al = 1
            bl = -2 - coef_c
            cl = 1
            dl = 0
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


