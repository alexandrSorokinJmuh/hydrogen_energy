import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class CharacteristicFromExcel:

    def __init__(self, *args, **kwargs):
        if len(kwargs) == 0 or kwargs["excel"] is None:
            raise ValueError("excel is None")

        self.max_m = [1 for i in range(17)]
        self.min_m = [0.7, 0.75, 0.6, 0.4, 0.75, 0.3, 0.1, 0.7, 0.2, 0.37, 0.46, 0.67]
        self.min_m[2] = 0.4
        self.max_m[0] = 2
        self.res = {}
        self.init_chars = {}
        self.characteristics_labels = [col_name.replace('\n', '') for col_name in kwargs["excel"].columns[1:]]
        self.char_faks_index = self.characteristics_labels.index('FaK1')
        self.chars = []
        excel_rows = kwargs["excel"].values
        # excel_head = [col_name.replace('\n', '') for col_name in kwargs["excel"].columns[1:]]
        for index_row, excel_row in enumerate(excel_rows):
            name = excel_row[0]
            self.init_chars[name] = {}

            for i, cell in enumerate(excel_row[1:]):
                self.init_chars[name][self.characteristics_labels[i]] = cell

            char_val = list(self.init_chars[name].values())
            self.chars.append(self.Characteristic(index_row + 1, name, char_val[:self.char_faks_index],
                                                  char_val[self.char_faks_index:]))

        self.func_m = {}
        self.fak_f = {'FaK1': fak1, 'FaK2': fak2, 'FaK3': fak3, 'FaK4': fak4}
        for i in self.chars:
            for f in (i.b + i.d):
                name = 'f' + str(len(self.func_m.keys()) + 1)
                self.func_m[name] = lambda t: 1
                i.funcs[f] = name

    class Characteristic:
        def __init__(self, index, label, funcs, faks):
            self.index = index
            self.label = label
            self.b = []
            self.b_fak = []
            self.d_fak = []
            self.d = []
            self.funcs = {}
            for ind, f in enumerate(funcs):
                if f == 1:
                    self.b.append("m" + str(ind + 1))
                elif f == -1:
                    self.d.append("m" + str(ind + 1))

            for ind, fak in enumerate(faks):
                if fak == 1:
                    self.b_fak.append("FaK" + str(ind + 1))
                elif fak == -1:
                    self.d_fak.append("FaK" + str(ind + 1))

        def calculate(self, max_val, funcs, faks):
            res = 0
            res_b_f = list(map(lambda x: funcs[self.funcs[x]], self.b))
            res_d_f = list(map(lambda x: funcs[self.funcs[x]], self.d))

            res_b_fak = list(map(lambda x: faks[x], self.b_fak))
            res_d_fak = list(map(lambda x: faks[x], self.d_fak))

            return lambda y, t: 1 / max_val * (np.prod(list(map(lambda x: x(t), res_b_f))) * sum(
                list(map(lambda x: x(t), res_b_fak))) - np.prod(list(map(lambda x: x(t), res_d_f))) * sum(
                list(map(lambda x: x(t), res_d_fak))))

    def init_par(self, init_par):
        self.func_m['f' + str(init_par['-f0v-'])] = lambda t: f0(t, init_par)
        self.func_m['f' + str(init_par['-f1v-'])] = lambda t: f1(t, init_par)
        self.func_m['f' + str(init_par['-f2v-'])] = lambda t: f2(t, init_par)
        self.func_m['f' + str(init_par['-f3v-'])] = lambda t: f3(t, init_par)
        self.func_m['f' + str(init_par['-f4v-'])] = lambda t: f4(t, init_par)

    def calculate(self, init_params):

        # m1 = 1 / self.max_m[0] * self.func_m['f4'] * ()

        for i, char in enumerate(self.chars):
            t = np.linspace(0, 1, 110)  # vector of time
            y0 = 1  # start value
            m_c = char.calculate(self.max_m[i], self.func_m, self.fak_f)
            init_m_param = float(init_params['-m' + str(char.index) + '-'])
            y = odeint(m_c, init_m_param, t)  # solve eq.
            y = np.array(y).flatten()
            self.res[char.label] = y

        return self.res

    def get_graphics(self):
        fig = plt.figure(figsize=(10, 5))

        # создаём область, в которой будет
        # - отображаться график
        t = np.linspace(0, 1, 110)  # vector of time
        # рисуем график
        legend_labels = []
        for char in self.chars:
            plt.plot(t, self.res[char.label], linewidth=3)
            legend_labels.append(char.label)
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.legend(legend_labels, bbox_to_anchor=(1, 1))
        fig.tight_layout()
        fig.savefig('funcs.png')

    def get_diag(self, t):
        labels = list(self.res.keys())

        t_110 = np.linspace(0, 1, 110)
        res_index = 0
        for i, t_i in enumerate(t_110):
            if t_i > t:
                break
            res_index = i
        stats = [i[res_index] for i in self.res.values()]
        make_radar_chart('T=' + str(t), stats, labels, min_val=self.min_m)


def make_radar_chart(name, stats, attribute_labels, plot_markers=[0, 0.2, 0.4, 0.6, 0.8, 1], min_val=[],
                     plot_str_markers=["0", "0.2", "0.4", "0.6", "0.8", "1"]):
    labels = np.array(attribute_labels)

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    stats = np.concatenate((stats, [stats[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    # max_st = int(max(stats))
    # if max_st > 1:
    #     plot_markers = [i for i in range(0, max_st, max_st / 5)]
    fig = plt.figure(figsize=(13, 8))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2)
    ax.fill(angles, stats, alpha=0.25)
    legend_labels = ['Критерии на текущий момент времени']

    if min_val != []:
        min_stats = np.concatenate((min_val, [min_val[0]]))
        legend_labels.append('Минимальные значения')
        ax.plot(angles, min_stats, linewidth=2)
        ax.fill(angles, min_stats, alpha=0.25)

    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    plt.yticks(plot_markers)
    ax.set_title(name)
    ax.grid(True)
    plt.legend(legend_labels, bbox_to_anchor=(0, 0))
    # fig.tight_layout()
    fig.savefig("diag.png")

    return plt.show()


def f0(t, k):
    return float(k['-f0-a-']) * t ** 3 + float(k['-f0-b-']) * t ** 2 + float(k['-f0-c-']) * t + float(k['-f0-d-'])


def f1(t, k):
    return float(k['-f1-a-']) * t ** 3 + float(k['-f1-b-']) * t ** 2 + float(k['-f1-c-']) * t + float(k['-f1-d-'])


def f2(t, k):
    return float(k['-f2-a-']) * t ** 3 + float(k['-f2-b-']) * t ** 2 + float(k['-f2-c-']) * t + float(k['-f2-d-'])


def f3(t, k):
    return float(k['-f3-a-']) * t ** 3 + float(k['-f3-b-']) * t ** 2 + float(k['-f3-c-']) * t + float(k['-f3-d-'])


def f4(t, k):
    return float(k['-f4-a-']) * t ** 3 + float(k['-f4-b-']) * t ** 2 + float(k['-f4-c-']) * t + float(k['-f4-d-'])


def fak1(t):
    return -t ** 3 + 0.8


def fak2(t):
    return np.cos(1.5 * t) ** 2 / 2 + 0.2


def fak3(t):
    res = np.where(t < 0, -1, t)
    res = np.where(t > 1, -1, res)
    res = np.where(t <= 1, 0.9, res)
    res = np.where(t <= 0.7, 0.8, res)
    res = np.where(t <= 0.2, 0.5, res)
    return res


def fak4(t):
    return np.sin(9 * t) * np.sin(5 * t) * 0.3 + 0.5




excel_file_path = 'TIPiS.xlsx'

excel_source = pd.read_excel(excel_file_path)
chars = CharacteristicFromExcel(excel=excel_source)


def get_faks_image():
    fig = plt.subplots()

    # создаём область, в которой будет
    # - отображаться график
    t = np.linspace(0, 1, 100)

    # рисуем график
    plt.plot(t, fak1(t))
    plt.plot(t, fak2(t))
    plt.plot(t, fak3(t))
    plt.plot(t, fak4(t))

    # показываем график

    plt.ylim([0, 1])
    plt.legend(['FaK1', 'FaK2', 'FaK3', 'FaK4', 'FaK5'], bbox_to_anchor=(1, 1))
    fig[0].tight_layout()
    fig[0].savefig('fak.png')
