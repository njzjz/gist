import itertools
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage.filters

__author__ = "Jinzhe Zeng"
__email__ = "jzzeng@stu.ecnu.edu.cn"

plt.switch_backend('Agg')
plt.rcParams["font.family"] = "Times New Roman"

del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Times New Roman'
matplotlib.rcParams['mathtext.it'] = 'Times New Roman:italic'
matplotlib.rcParams['mathtext.bf'] = 'Times New Roman:bold'


def getimage(title, specs, timestep, speciesfile, svgfile):
    spec = {}
    with open(speciesfile) as f:
        for line1, line2 in itertools.zip_longest(*[f]*2):
            s1, s2 = line1.split(), line2.split()
            spec[int(s2[0])*timestep] = dict(zip(s1[4:], [int(x)
                                                          for x in s2[3:]]))

    def getnumber(s):
        num = np.zeros((len(spec)))
        for i, t in enumerate(spec):
            if s in spec[t]:
                num[i] = spec[t][s]
        num = scipy.ndimage.filters.gaussian_filter1d(num, 200)
        num = np.floor(num)
        return num

    nums = [getnumber(x) for x in specs]
    steps = np.array(list(spec.keys()))

    def sub(s):
        for i in range(10):
            s = s.replace(str(i), f"_{{{i}}}")
        for i in range(10):
            s = s.replace(f"{i}}}_{{", str(i))
        return s

    labels = [sub(f"$\mathrm{{{s}}}$") for s in specs]

    figureno = [f"({chr(i)})" for i in range(97, 97+len(specs))]

    fig = plt.figure(figsize=(6, 1*len(specs)))
    for ii, (s, n, l) in enumerate(zip(specs, nums, labels)):
        plt.subplot(100*len(specs)+11+ii)
        plt.plot(steps, n, label=l, color=f'C{ii+1}')
        plt.xlim(0, steps[-1])
        plt.ylim(0, np.floor(np.max(n))+0.5)
        plt.text(np.max(steps)*0.02,
                 (np.floor(np.max(n))+0.5)*0.8, figureno[ii])
        if ii == len(specs)-1:
            plt.xlabel("Time (ps)")
            plt.yticks(range(0, int(np.max(n))+1, math.ceil(np.max(n)/4)))
        else:
            plt.xticks([])
            plt.yticks(range(int(np.max(n))//4, int(np.max(n)) +
                             1, math.ceil(np.max(n)/4)))
        plt.legend(frameon=False, loc=1)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)

    fig.text(0.00, 0.5, "Number of main molecules",
             va='center', rotation='vertical')
    # plt.title(title)
    plt.savefig(svgfile)
    plt.cla()


if __name__ == '__main__':
    getimage("Methane", ['CH3', 'CH3O', 'CHO', 'HO2', 'HO'],
             0.1/1000, "speciesnvt_ch4.txt", "species4.svg")
    # getimage("RP-3", [
    #        'C2H4','CH2O','C2H5O','CH3','HO2','HO'
    #        ],
    #         0.1/1000, "speciesnvt_rp3.txt", "species3.svg")
