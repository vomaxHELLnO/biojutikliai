from matplotlib import pyplot as plt
from numpy import array, arange


def print_matrix(matrix):
    print 'micro m: ',
    for j in range(len(matrix[0])):
        print str(j*h)+ '    ',
    print
    for i, row in enumerate(matrix):
        print str(i*tau)+'s', ' '.join(['%.4f' % e for e in row])

def draw_matrix(substrate, label='S, micro M'):
    x = [i*h/1000. for i in range(n)]
    plt.xlabel('x, mm')
    plt.ylabel(label)
    plt.xticks(arange(min(x), max(x)+ (0.01), 0.01))
    plt.yticks(arange(0, 1 + 0.1, 0.1))
 #   plt.plot(x, substrate[int(0.1/tau)], 'm')
 #   plt.plot(x, substrate[int(0.2/tau)], 'm')
    plt.plot(x, substrate[int(0.3/tau)], 'm')
    plt.plot(x, substrate[int(0.4/tau)], 'm')
    plt.plot(x, substrate[int(0.5/tau)], 'm')
    plt.plot(x, substrate[int(1/tau)], 'r')
    plt.plot(x, substrate[int(3/tau)], 'b')
    plt.plot(x, substrate[int(5/tau - 1)], 'g')
    plt.legend(['0.3s','0.4s','0.5s','1s','3s','5s'],loc = 'left')
    plt.show()

def get_current(product):
    return ne*F*Dp*array(product)/h/10**6

def draw_current(product, response_time, label):

   # time = [tau*i for i in range(m)]
    time = [tau * i for i in range(int(response_time/h))]
    plt.xlabel('t, s')
    plt.ylabel(label)
   # plt.xticks(arange(min(time), max(time)+ (0.01), 0.01))
   # plt.yticks(arange(0, 1 + 0.1, 0.1))
   # import ipdb; ipdb.set_trace()
    plt.plot(time, get_current(array(product)[:int(response_time/tau), 1]), 'm')
   # plt.plot(time, get_current(array(product)[:int(response_time/tau), int(d/h - 10/h)]), 'm')
   # plt.plot(time, get_current(array(product)[:int(response_time/tau), int(d/h - 15/h)]), 'r')
   # plt.plot(time, get_current(array(product)[:int(response_time/tau), int(d/h - 100/h)]), 'b')
   # plt.plot(time, get_current(array(product)[:int(response_time/tau), int(d/h - 130/h)]), 'g')
    plt.legend(['d - 0.01mm = 0.14mm','d - 0.015mm = 0.135mm','d - 0.1mm = 0.05mm','d - 0.13mm = 0.02mm'],loc = 'upper left')
    plt.title('Current when d = 0.15mm and  $\epsilon$ = 0.01')
    plt.xlim(0, response_time)
    plt.show()

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
Dp = 300 # 300 micro m^2/s
d = 100 # 0.1 mm maksimalus fermento membranos sluoksnis
h = 0.1 # x kitimo zingsnis x in [0;d]
n = int(d / h + 1) # erdves zingsniu skaicius
Km = 100 #100 microM
Vmax = 100 #100 microM/s
tau = 0.1 # delta time
T = 50 # maksimalus stebejimo laikas
m = int(T / tau)#laiko zingsniu skaicius
epsilon = 0.05
I = ne*F*Vmax*d/2 #max i, (59) knygos formule

def get_substrate_matrix():
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
            d1 = -1 * ((h * h) / (Dp * tau)) * (((Vmax * substrate[i-1][1] * tau) / 
                (Km + substrate[i-1][1])) + product[i-1][1])
            coef.append([b1,c1,d1])
            for l in range(1, n - 1):
                al = 1
                bl = -2 - coef_c
                cl = 1
                dl = -1 * ((h * h) / (Dp * tau)) * (((Vmax * substrate[i-1][l] * tau)
                    /(Km + substrate[i-1][l])) + product[i-1][l])
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
    i1 = get_current(array(product)[:, int(enzyme_width/h)])
    for t in range(int(T/tau)):
        if time == 0:
            if ((t*tau)/i1[t])*abs((i1[t]-i1[t-1])/((t*tau)-((t-1)*tau))) < epsilon:
                time =t * tau # t- laiko zingsnis
    return time

if __name__ == '__main__':
    substrate = get_substrate_matrix()
    product = get_product_matrix(substrate)
    time = get_T(product, int(d - 130))
    #print_matrix(product)
    draw_matrix(product, 'P, micro M')
    draw_matrix(substrate, 'S, micro M')
    draw_current(product, time, 'i, nA/mm$^2$')
