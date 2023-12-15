import numpy as np
import matplotlib.pyplot as plt

def dump_selection(pp0, ads, ids_selected, xlabel='pp0', ylabel='ads'):
    ids_selected = np.array(ids_selected)
    ids_not_selected = np.array(np.ones(len(pp0)), dtype=bool) ^ ids_selected
    
    pp0_selected, ads_selected = pp0[ids_selected], ads[ids_selected]
    pp0_not_selected, ads_not_selected = pp0[ids_not_selected], ads[ids_not_selected]
    
    plt.plot(pp0, ads, 'k')
    plt.scatter(pp0_selected, ads_selected, c='green')
    plt.scatter(pp0_not_selected, ads_not_selected, c='red')
    plt.title('selection')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    
def dump_linearization(x, y, s, i, xlabel='x', ylabel='y'):
    x_lin = np.linspace(min(x), max(x), 2)
    y_lin = x_lin * s + i
    plt.scatter(x, y, c='black')
    plt.plot(x_lin, y_lin, '--k')
    plt.title('linearization')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()