import numpy as np

def Linearize(x,y):
       
    xmean, ymean = np.mean(x), np.mean(y)
    x2mean, xymean = np.mean(x**2), np.mean(x*y)

    s = (xymean - xmean*ymean) / (x2mean - xmean**2)
    i = ymean - s * xmean

    y2mean = np.mean(y**2)
    r2 = (xymean - xmean*ymean)**2/(x2mean- xmean**2)/(y2mean - ymean**2)

    return s,i,r2