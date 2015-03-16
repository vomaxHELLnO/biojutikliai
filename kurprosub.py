from matplotlib import pyplot as plt
from numpy import array, arange


def print_matrix(matrix):
    print 'micro m: ',
    for j in range(len(matrix[0])):
        print str(j*h)+ '    ',
    print
    for i, row in enumerate(matrix):
        print str(i*tau)+'s', ' '.join(['%.4f' % e for e in row])

def draw_matrix(substrate, n, label='S, micro M'):
    x = [i*h/1000. for i in range(n)]
    plt.xlabel('x, mm')
    plt.ylabel(label)
    plt.xticks(arange(min(x), max(x)+ (0.01), 0.01))
    plt.yticks(arange(0, 1 + 0.1, 0.1))
    plt.plot(x, substrate[int(0.5/tau)], 'm')
    plt.plot(x, substrate[int(1/tau)], 'r')
    plt.plot(x, substrate[int(3/tau)], 'b')
    plt.plot(x, substrate[int(5/tau - 1)], 'g')
    plt.legend(['0.5s','1s','3s','5s'],loc = 'left')
  #  plt.show()

def get_current(product):
    return ne*F*Dp*array(product)/h/10**6

def draw_current(product, response_time, label, color):
    # time = [tau*i for i in range(m)]
    time = [tau * i for i in range(int(response_time/h))]
    plt.xlabel('t, s')
    plt.ylabel(label)
    plt.xticks(arange(min(time), max(time)+ (0.01), 1))
    plt.yticks(arange(0, 1.2 + 0.1, 0.1))
    # import ipdb; ipdb.set_trace()
    plt.plot(time, get_current(array(product)[0:int(response_time/tau), 1]), color)
    plt.legend(['d = 0.01mm','d = 0.015mm','d = 0.1mm','d = 0.15mm'],loc = 'upper left')
    plt.title('Current with T(d = 0.15mm), $\mathbf{\delta}$t = 0.1s, h = 0.1$\mu$m, $\epsilon$ = 0.4')
    # plt.xlim(0, response_time)
    # plt.show()

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
    X.reverse()
    return X

S0 = 1 # 1 microM = 0,01KM
P0 = 0 #
ne = 2
#N = ~200, 1% paklaida, 303p del laiko
F = 96485 # faradejaus konstanta
Ds = 300 # 300 micro m^2/s
Dp = 300 # 300 micro m^2/s D2p
D1p = 500
#d = 100 # 0.1 mm maksimalus fermento membranos sluoksnis
h = 0.1 # x kitimo zingsnis x in [0;d]
#n = int(d / h + 1) # erdves zingsniu skaicius
Km = 100 #100 microM
Vmax = 100 #100 microM/s
tau = 0.1 # delta time
T = 50 # maksimalus stebejimo laikas
m = int(T / tau)#laiko zingsniu skaicius
epsilon = 0.40
#I = ne*F*Vmax*d/2 #max i, (59) knygos formule

def get_substrate_matrix():
    substrate = []
    for i in range(m):                  # laiko zingsniai
        substrate.append([])
        for j in range(n1):              # membranos zingsniai
            if i == 0:
                substrate[i].append(0)
            else:
                substrate[i].append(None)
            if j == (n1 - 1):
                substrate[i][j] = S0
        if i != 0:
            coef_c = (h * h) / (tau * Ds)
            coef = []
            b1 = -1 - coef_c
            c1 = 1
           # d1 = 0
            d1 = ((h * h) / (Ds * tau)) * (((Vmax * substrate[i-1][1] * tau) / 
                (Km + substrate[i-1][1])) - substrate[i-1][1])
            coef.append([b1,c1,d1])
            for l in range(1, n1 - 1):
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
            for k in range(1, n1 - 1):
                substrate[i][k] = X[k - 1]
    return substrate

def get_product_matrix(substrate):
    product = []
    for i in range(m):
        product.append([])
        for j in range(n):
            if i == 0:
                product[i].append(0)
            else:
                product[i].append(None)
            if j == (n - 1):
                product[i][j] = P0
        if i != 0:
            coef_c = (h * h) / (tau * Dp)
            coef = []
            b1 = -2 - coef_c
            c1 = 1
            d1 = -1 * ((h * h) / (D1p * tau)) * product[i-1][1]
          #  d1 = -1 * ((h * h) / (Dp * tau)) * (((Vmax * substrate[i-1][1] * tau) / 
          #      (Km + substrate[i-1][1])) + product[i-1][1])
            coef.append([b1,c1,d1])
            for l in range(1, n - 1):
                al = 1
                bl = -2 - coef_c
                cl = 1
             #   if n <= n0:
             #       dl = -1 * ((h * h) / (D1p * tau)) * product[i-1][l]
                if l <= n0:
                    dl =-1 * ((h * h) / (Dp * tau)) *  product[i-1][l]
                if l > n0:
                    dl =-1 * ((h * h) / (Dp * tau)) * (((Vmax * substrate[i-1][l-n0] * tau)
                        /(Km + substrate[i-1][l-n0])) + product[i-1][l])
                coef.append([al, bl, cl, dl])
            an = 1
            bn = -2 - coef_c
            cn = 0
            dn = -P0
            coef.append([an, bn, cn, dn])

            X = perkelties_metodas(coef)
            product[i][0] = X[0]
            for k in range(1, n - 1):
                product[i][k] = X[k - 1]
    return product

def get_T(product, enzyme_width):
    time = 0
    i1 = get_current(array(product)[:, 1])
    for t in range(int(T/tau)):
        if time == 0 and (t*tau) > 2:
            if ((t*tau)/i1[t])*abs((i1[t]-i1[t-1])/((t*tau)-((t-1)*tau))) < epsilon:
                time = t * tau # t- laiko zingsnis
    return time

if __name__ == '__main__':
    d1 = 100          #fermento sluoksnis
    n1 = int(d1 / h + 1)
    d0 = 50           #selektyvios membranos sluoksnis
    n0 = int(d0 / h + 1)
    substrate = get_substrate_matrix()
    draw_matrix(substrate, n1, 'S, micro M')
    plt.show()
    n = n1 + n0
    product = get_product_matrix(substrate)
    draw_matrix(product, n, 'P, micro M')
    plt.plot([d0/1000., d0/1000.], [0, 0.5], 'm--')
    plt.show()
  #  exit() 
   #  print_matrix(product)
    colors = ['m','r','b','g']
    d1lengs = [10, 15, 100, 150]             # fermento sluoksniai
    d0lengs = [50]
    for i1, d1 in enumerate(d1lengs):
        for i0, d0 in enumerate(d0lengs):
            n0 = int(d0 / h + 1) # erdves zingsniu skaicius selektyvioj membranoj
            n = int(d1 / h + 1) # erdves zingsniu skaicius fermente
            substrate = get_substrate_matrix()
            product = get_product_matrix(substrate)
   #     print( product[0][10])
   #     print( product[1][10])
   #     print( product[2][10])
   #     print( product[3][10])
            draw_current(product, T, 'i, nA/mm$^2$', colors[i1])
    T_response = get_T(product, 50)
    plt.xlim(0, T_response)
    plt.ylim(0, 1.2)
    plt.show()
