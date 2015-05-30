# coding: utf-8
from matplotlib import pyplot as plt
from numpy import array, arange


def print_matrix(matrix):
    print 'micro m: ',
    for j in range(len(matrix[0])):
        print str(j*h)+ '    ',
    print
    for i, row in enumerate(matrix):
        print str(i*tau)+'s', ' '.join(['%.4f' % e for e in row])

def draw_matrix(substrate, n, label='S, micro M', dim=1):
    #x = [i*h/1000. for i in range(n)]
    plt.xlim([0, 1])
    if label == 'S, micro M':
        x = [(i*h + d0) / dim for i in range(n)]
        plt.plot(x, substrate[int(0.5/tau)], 'm')
        plt.plot(x, substrate[int(1/tau)], 'r')
        plt.plot(x, substrate[int(3/tau)], 'b')
        plt.plot(x, substrate[int(5/tau - 1)], 'g')
        plt.ylabel('$\hat{S}$')
    if label == 'P, micro M':
        x = [i*h/(dim) for i in range(n)]
        plt.plot(x, substrate[int(0.5/tau)], 'm')
        plt.plot(x, substrate[int(1/tau)], 'r')
        plt.plot(x, substrate[int(3/tau)], 'b')
        plt.plot(x, substrate[int(5/tau - 1)], 'g')
        plt.ylabel('$\hat{P}$')
    plt.xlabel('$\hat{x}$')
    #plt.xticks(arange(min(x), max(x)+ (0.01), 0.01))
    #plt.xticks(arange(min(x), max(x)+ (0.01), 0.01))
    #plt.yticks(arange(0, 1 + 0.1, 0.1))
    plt.legend(['0.5s','1s','3s','5s'],loc = 'left')
  #  plt.show()

def get_current(product, nn):
    return (array(product) *nn)/(Km)

def draw_T05_d0(srove):
    plt.plot([e[0] for e in srove], [e[1] for e in srove],'bo')
    plt.xlabel('$d_0 / (d_1 - d_0)$')
    plt.ylabel('$i$')
    plt.show()
    plt.plot([e[0] for e in srove], [e[2] for e in srove],'bo')
    plt.xlabel('$d_0 / (d_1 - d_0)$')
    plt.ylabel('$T_{0.5}$')
    plt.show()

def draw_dif_d0(srove):
    plt.plot([e[0] for e in srove], [e[1] for e in srove], 'bo')
    plt.xlabel('$D_{1P} / D_{2P}$')
    plt.ylabel('$i$')
    plt.show()
    plt.plot([e[0] for e in srove], [e[2] for e in srove],'bo')
    plt.xlabel('$D_{1P} / D_{2P}$')
    plt.ylabel('$T_{0.5}$')
    plt.show()

def draw_current(product, response_time, label, color):
    # time = [tau*i for i in range(m)]
    time = [((tau * i) * Ds /((d0 + d2) *(d0 + d2))) for i in range(int(response_time/h))]
    plt.xlabel('$\hat{t}$')
    plt.ylabel(label)
    #plt.xticks(arange(min(time), max(time)+ (0.01), 1))
    #plt.yticks(arange(0, 1.2 + 0.1, 0.1))
    # import ipdb; ipdb.set_trace()
    plt.plot(time, get_current(array(product)[0:int(response_time/tau), 1]), color)
    legend = []
    for k in range(4):
        legend.append('$d_0$ = ' + str(d0lengs[0]/1000.) + 'mm'+ ', $d_1$ = '+ str((d1lengs[k]+d0lengs[0])/1000.)+'mm')
    plt.legend(legend, loc = 'upper left')
    plt.title(u'Srov$ė$, su ' + r' T($d_1$ =' + str(d1lengs[3] + d0lengs[0]) + r'mm), $\epsilon$ = '+ str(epsilon))
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

S0 = 50 # 1 microM = 0,01KM
P0 = 0 #
ne = 2
#N = ~200, 1% paklaida, 303p del laiko
F = 96485 # faradejaus konstanta
Ds = 300. # 300 micro m^2/s
Dp = 300. # 300 micro m^2/s D2p
D1p = 1000.
#d = 100 # 0.1 mm maksimalus fermento membranos sluoksnis
h = 0.1 # x kitimo zingsnis x in [0;d]
#n = int(d / h + 1) # erdves zingsniu skaicius
Km = 100. #100 microM
Vmax = 100. #100 microM/s
tau = 0.1 # delta time
T = 80. # maksimalus stebejimo laikas
m = int(T / tau)#laiko zingsniu skaicius
epsilon = 0.10
d1 = 100.          #fermento sluoksnis
d2 = 100.
n1 = int(d1 / h)
d0 = 20.           #selektyvios membranos sluoksnis
n0 = int(d0 / h)
d1lengs = [10, 15, 100, 150]             # fermento sluoksniai
d0lengs = [20]
#I = ne*F*Vmax*d/2 #max i, (59) knygos formule
#Bedimensio modelio parametrai
hatx = 0.01
hatt = (Ds * T) / (1 * 1)
h1x = d1/h
hd1lengs = list(array(d1lengs) / h)
hd0lengs = d0 / h
ht = 0
hS = 0
hP = 0
sigma = 0

def get_substrate_matrix(Vmax, S0):
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

def get_product_matrix(substrate, n, n0, D1p, Vmax):
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
            coef_d = (h * h) / (tau * D1p)
            coef = []
            b1 = -2 - coef_d
            c1 = 1
            d1 = -1 * ((h * h) / (D1p * tau)) * product[i-1][1]
          #  d1 = -1 * ((h * h) / (Dp * tau)) * (((Vmax * substrate[i-1][1] * tau) / 
          #      (Km + substrate[i-1][1])) + product[i-1][1])
            coef.append([b1,c1,d1])
            for l in range(1, n - 1):
                al = 1
                cl = 1
             #   if n <= n0:
             #       dl = -1 * ((h * h) / (D1p * tau)) * product[i-1][l]
                if l <= n0:
                    bl = -2 - coef_d
                    dl =-1 * ((h * h) / (D1p * tau)) *  product[i-1][l]
                if l > n0:
                    bl = -2 - coef_c
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
    i1 = get_current(array(product)[:, 1], 1)
    for t in range(int(T/tau)):
        if time == 0 and (t*tau) > 1.:
            if ((t*tau)/i1[t])*abs((i1[t]-i1[t-1])/((t*tau)-((t-1)*tau))) < epsilon:
                time = t * tau # t- laiko zingsnis
    return time


def get_T05(product, T_, d):
    time = 0
    i1 = get_current(array(product)[:, 1], 1)
    for t in range(int(T_/tau)):
        if time == 0:
            if (i1[t]/i1[(T_/tau)-1]) > 0.5:
                time = t * tau # * Ds) / (d * d)  # t- laiko zingsnis
    return time

def get_Dep_T05_d0(substrate_):
    '''Grazina masyva, kuriame talpinamos priklausomybes puslaikio nuo
    selektyvios membranos storio pagal apsibreztus parametrus'''
    intervalo_daznis = 10.
    hatd0_intervalas = 2.
    zingsnio_dydis = hatd0_intervalas / intervalo_daznis
    sroves = []
    for Vmax_ in [1, 10, 100]:
        srove = []
        for t in range(int(intervalo_daznis)):
            n0_ = int((zingsnio_dydis + (zingsnio_dydis * t))*d1/h)
            n_ = n0_ + n1
            product_ = get_product_matrix(substrate_, n_, n0_, 1000, Vmax_)
            T_ = get_T(product_, (zingsnio_dydis + (zingsnio_dydis * t))*d1)
            T05_ = (get_T05(product_, T_, (n0_ + n1) * h)) *Ds  / (n_ *h* n_ *h)
            current_ = get_current(product_[int(T_ / h)][1], n_)
            srove.append([(zingsnio_dydis + (zingsnio_dydis * t)) / 3, current_, T05_])
        sroves.append(srove)

    # for S0_ in [0.5, 1, 5]:
    #     srove = []
    #     for t in range(int(intervalo_daznis)):
    #         substrate_ = get_substrate_matrix(Vmax, S0)
    #         n0_ = int((zingsnio_dydis + (zingsnio_dydis * t))*d1/h)
    #         n_ = n0_ + n1
    #         product_ = get_product_matrix(substrate_, n_, n0_, 1000, 100)
    #         T_ = get_T(product_, (zingsnio_dydis + (zingsnio_dydis * t))*d1)
    #         T05_ = get_T05(product_, T_, (n0_ + n1) * h)
    #         # TODO hati
    #         current_ = get_current(product_[int(T_ / h)][1] / Km)
    #         srove.append([zingsnio_dydis + (zingsnio_dydis * t), current_, T05_])
    #     sroves.append(srove)
    # skirtingi sigma
    plt.plot([e[0] for e in sroves[0]], [e[1] for e in sroves[0]],'bo-')
    plt.plot([e[0] for e in sroves[1]], [e[1] for e in sroves[1]],'rv-')
    plt.plot([e[0] for e in sroves[2]], [e[1] for e in sroves[2]],'gs-')

    legend = []
    legend.append('$\sigma^2$ = 0.33')# + str(int((d1 * d1 * 1)/(Km * Ds))))
    legend.append('$\sigma^2$ = 3.3')# + str(int((d1 * d1 * 10)/(Km * Ds))))
    legend.append('$\sigma^2$ = 33')# + str(int((d1 * d1 * 100)/(Km * Ds))))

    plt.legend(legend, loc = 'upper right')
    plt.xlabel('$\hat{d}_0$', fontsize = 20)
    plt.ylabel('$\hat{i}$', fontsize = 20)
    plt.show()

    plt.plot([e[0] for e in sroves[2]], [e[2] for e in sroves[2]],'gs-')
    plt.plot([e[0] for e in sroves[0]], [e[2] for e in sroves[0]],'bo-')
    plt.plot([e[0] for e in sroves[1]], [e[2] for e in sroves[1]],'rv-')

    legend = []
    legend.append('$\sigma^2$ = 33')# + str(int((d1 * d1 * 100)/(Km * Ds))))
    legend.append('$\sigma^2$ = 0.33')# + str(int((d1 * d1 * 1)/(Km * Ds))))
    legend.append('$\sigma^2$ = 3.3')# + str(int((d1 * d1 * 10)/(Km * Ds))))

    plt.legend(legend, loc = 'upper right')
    plt.xlabel('$\hat{d}_0$', fontsize = 20)
    plt.ylabel('$\hat{T}_{0.5}$', fontsize = 20)
    plt.show()
    # skirtingi s0
    # plt.plot([e[0] for e in sroves[3]], [e[1] for e in sroves[3]],'bo')
    # plt.plot([e[0] for e in sroves[4]], [e[1] for e in sroves[4]],'rv')
    # plt.plot([e[0] for e in sroves[5]], [e[1] for e in sroves[5]],'gs')
    #
    # plt.xlabel('$d_0 / (d_1 - d_0)$')
    # plt.ylabel('$i$')
    # plt.show()
    #
    # plt.plot([e[0] for e in sroves[3]], [e[2] for e in sroves[3]],'bo')
    # plt.plot([e[0] for e in sroves[4]], [e[2] for e in sroves[4]],'rv')
    # plt.plot([e[0] for e in sroves[5]], [e[2] for e in sroves[5]],'gs')
    #
    # plt.xlabel('$d_0 / (d_1 - d_0)$')
    # plt.ylabel('$T_{0.5}$')
    # plt.show()
    return srove

def get_Dep_dif_d0(substrate_):
    '''Grazina masyva, kuriame talpinamos priklausomybes puslaikio nuo
    selektyvios membranos storio pagal apsibreztus parametrus'''
    intervalo_daznis = 40.
    hatd0_intervalas = 1.
    zingsnio_dydis = hatd0_intervalas / intervalo_daznis
    sroves = []
    for Vmax_ in [1, 10, 100]:
        srove = []
        for t in range(int(intervalo_daznis)):
            D1p_ = int((zingsnio_dydis + (zingsnio_dydis * t))*Ds)
            product_ = get_product_matrix(substrate_, 1200, 200, D1p_, Vmax_)
            T_ = get_T(product_, (zingsnio_dydis + (zingsnio_dydis * t))*d1)
            T05_ = (get_T05(product_, T_, 1200)) * Ds / ((1200 * h)*(1200 * h))

            # TODO hati
            current_ = get_current(product_[int(T_ / h)][1], 1200)
            srove.append([zingsnio_dydis + (zingsnio_dydis * t), current_, T05_])
        sroves.append(srove)

    # for S0_ in [0.5, 1, 5]:
    #     srove = []
    #     for t in range(int(intervalo_daznis)):
    #         substrate_ = get_substrate_matrix(Vmax, S0)
    #         D1p_ = int((zingsnio_dydis + (zingsnio_dydis * t))*Ds)
    #         product_ = get_product_matrix(substrate_, 1200, 200, D1p_, Vmax_)
    #         T_ = get_T(product_, (zingsnio_dydis + (zingsnio_dydis * t))*d1)
    #         T05_ = get_T05(product_, T_, 1200)
    #         # TODO hati
    #         current_ = get_current(product_[int(T_ / h)][1] / Km)
    #         srove.append([zingsnio_dydis + (zingsnio_dydis * t), current_, T05_])
    #     sroves.append(srove)
    # skirtingi sigma
    plt.plot([e[0] for e in sroves[0]], [e[1] for e in sroves[0]],'bo-')
    plt.plot([e[0] for e in sroves[1]], [e[1] for e in sroves[1]],'rv-')
    plt.plot([e[0] for e in sroves[2]], [e[1] for e in sroves[2]],'gs-')

    legend = []
    legend.append('$\sigma^2$ = 0.33')#+ str(int((d1 * d1 * 1)/(Km * Ds))))
    legend.append('$\sigma^2$ = 3.3')#+ str(int((d1 * d1 * 10)/(Km * Ds))))
    legend.append('$\sigma^2$ = 33')#+ str(int((d1 * d1 * 100)/(Km * Ds))))

    plt.legend(legend, loc = 'upper right')
    plt.xlabel('$\hat{D}_{1P}$', fontsize = 20)
    plt.ylabel('$\hat{i}$', fontsize = 20)
    plt.show()

    plt.plot([e[0] for e in sroves[2]], [e[2] for e in sroves[2]],'gs-')
    plt.plot([e[0] for e in sroves[0]], [e[2] for e in sroves[0]],'bo-')
    plt.plot([e[0] for e in sroves[1]], [e[2] for e in sroves[1]],'rv-')

    legend = []
    legend.append('$\sigma^2$ = 33')#+ str(int((d1 * d1 * 100)/(Km * Ds))))
    legend.append('$\sigma^2$ = 0.33')#+ str(int((d1 * d1 * 1)/(Km * Ds))))
    legend.append('$\sigma^2$ = 3.3')#+ str(int((d1 * d1 * 10)/(Km * Ds))))

    plt.legend(legend, loc = 'upper right')
    plt.xlabel('$\hat{D}_{1P}$', fontsize = 20)
    plt.ylabel('$\hat{T}_{0.5}$', fontsize = 20)
    plt.show()
    # skirtingi s0
    # plt.plot([e[0] for e in sroves[3]], [e[1] for e in sroves[3]],'bo')
    # plt.plot([e[0] for e in sroves[4]], [e[1] for e in sroves[4]],'rv')
    # plt.plot([e[0] for e in sroves[5]], [e[1] for e in sroves[5]],'gs')
    #
    # plt.xlabel('$d_0 / (d_1 - d_0)$')
    # plt.ylabel('$i$')
    # plt.show()
    #
    # plt.plot([e[0] for e in sroves[3]], [e[2] for e in sroves[3]],'bo')
    # plt.plot([e[0] for e in sroves[4]], [e[2] for e in sroves[4]],'rv')
    # plt.plot([e[0] for e in sroves[5]], [e[2] for e in sroves[5]],'gs')
    #
    # plt.xlabel('$d_0 / (d_1 - d_0)$')
    # plt.ylabel('$T_{0.5}$')
    # plt.show()
    return srove

if __name__ == '__main__':
    substrate = get_substrate_matrix(Vmax, S0)
  #  draw_matrix(substrate, n1, 'S, micro M')
  #  plt.show()
    # n = n1 + n0
    # product = get_product_matrix(substrate, n, n0, D1p)
    # hatsubstrate = list(array(substrate) / Km)
    # hatproduct = list(array(product) / Km)
   # draw_matrix(product, n, 'P, micro M')
   # plt.plot([d0/1000., d0/1000.], [0, 0.5], 'm--')
    # draw_matrix(hatsubstrate, n1, 'S, micro M', (d0 + d1))
    # plt.plot([d0 / (d0+d1),d0 / (d0+d1)], [0, d0 / (d0+d1)/16], 'm--')
    # plt.show()
    # draw_matrix(hatproduct, n, 'P, micro M', (d0 + d1))
    # plt.plot([d0 / (d0+d1),d0 / (d0+d1)], [0, d0 / (d0+d1)/35], 'm--')
    # plt.show()

    get_Dep_T05_d0(substrate)
    #get_Dep_dif_d0(substrate)
   # exit()
   # print_matrix(product)
    colors = ['m','r','b','g']
    for i1, d1 in enumerate(d1lengs):
        for i0, d0 in enumerate(d0lengs):
            n0 = int(d0 / h + 1) # erdves zingsniu skaicius selektyvioj membranoj
            n1 = int(d1 / h + 1) # erdves zingsniu skaicius fermente
            n = n1 + n0
            substrate = get_substrate_matrix(Vmax)
            product = get_product_matrix(substrate, n, n0, D1p)
   #     print( product[0][10])
   #     print( product[1][10])
   #     print( product[2][10])
   #     print( product[3][10])
            draw_current(product, T, 'i, nA/mm$^2$', colors[i1])
    hatt = Ds /((d0 + d2) *(d0 + d2))
   # T_{0.5} (d_0)
   # pasipildyti modeli hat d_0=d_1/d_0 ir hat i
   #+ getT papildyti T_{05}
   # apskaiciuoti T_{05} bedimensiniame modelyje dugeliui hat d_0 get_Dep_T05_d0

   # i{d_0}
   # bedimensini modeli apsibrezti, pakeisti i i hati
   # apskaiciuoti hati bedimensiniame modelyje daugeliui hat d_0
    T_response = get_T(product, 50) * hatt
    plt.xlim(0, T_response)
    plt.ylim(0, 1.2)
    plt.show()

# def get_Dep_T05_d0(substrate_):
#     '''Grazina masyva, kuriame talpinamos priklausomybes puslaikio nuo
#     selektyvios membranos storio pagal apsibreztus parametrus'''
#     intervalo_daznis = 30.
#     hatd0_intervalas = 2.
#     zingsnio_dydis = hatd0_intervalas / intervalo_daznis
#     srove = []
#     get_current
#     for t in range(int(intervalo_daznis)):
#         n0 = int((zingsnio_dydis + (zingsnio_dydis * t))*d1/h)
#         n = n0 + n1
#         product_ = get_product_matrix(substrate_, n, n0)
#         T_ = get_T(product_, (zingsnio_dydis + (zingsnio_dydis * t))*d1)
#         T05_ = get_T05(product, T_)
#         # TODO hati
#         current_ = get_current(product_[int(T_ / h)][1])
#         srove.append([zingsnio_dydis + (zingsnio_dydis * t), current_, T05_])
#     return srove
#
# def get_Dep_dif_d0(substrate_):
#     '''Grazina masyva, kuriame talpinamos priklausomybes puslaikio nuo
#     selektyvios membranos storio pagal apsibreztus parametrus'''
#     intervalo_daznis = 20.
#     hatd0_intervalas = 1.
#     zingsnio_dydis = hatd0_intervalas / intervalo_daznis
#     srove = []
#     get_current
#     for t in range(int(intervalo_daznis)):
#         n0 = int((zingsnio_dydis + (zingsnio_dydis * t))*d1/h)
#         n = n0 + n1
#         product_ = get_product_matrix(substrate_, n, n0)
#         T_ = get_T(product_, (zingsnio_dydis + (zingsnio_dydis * t))*d1)
#         T05_ = get_T05(product, T_)
#         # TODO hati
#         current_ = get_current(product_[int(T_ / h)][1])
#         srove.append([zingsnio_dydis + (zingsnio_dydis * t), current_, T05_])
#     return srove
#
