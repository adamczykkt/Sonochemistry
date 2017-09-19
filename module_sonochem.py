from auxiliarymodule import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.optimize import curve_fit
import os
from math import ceil


def create(*args):
    if len(args) == 1:
        return BasicSet(args[0])
    elif len(args) == 2:
        return ExtendedSet(args[0], args[1])
    else:
        raise ValueError


class MeasurementList:
    def __init__(self, objects_list):
        self.content = objects_list

    def print(self):
        print('Current series:')
        for item in self.content:
            print('\t' + item.label)

    def plot_kinetics(self, option):
        if option == 5:
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(5.5, 4), gridspec_kw={'height_ratios':[10, 52]})
            ax1.set_ylim(0.95, 1.05)
            ax2.set_ylim(0.05, 0.57)
            ax1.spines['bottom'].set_visible(False)
            ax1.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
            ax1.set_yticks(ax1.get_yticks()[1::3])
            ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            ax2.spines['top'].set_visible(False)
            d1 = 0.015 * 52 / 10
            d2 = 0.015
            kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
            ax1.plot((1 - d2, 1 + d2), (-d1, +d1), **kwargs)
            ax1.plot((-d2, +d2), (-d1, d1), **kwargs)
            kwargs.update(transform=ax2.transAxes)
            ax2.plot((1 - d2, 1 + d2), (1 - d2, 1 + d2), **kwargs)
            ax2.plot((-d2, +d2), (1 - d2, 1 + d2), **kwargs)
            for i, item in enumerate(self.content):
                ax1.errorbar(item.time, item.opt_dens_norm, fmt='-o', lw='1',
                             yerr=item.opt_dens_norm_err, label=item.legend, capsize=5, color='C' + str(i))
                ax2.errorbar(item.time, item.opt_dens_norm, fmt='-o', lw='1',
                             yerr=item.opt_dens_norm_err, label=item.legend, capsize=5, color='C' + str(i))
            box2 = ax2.get_position()
            ax2.set_position([box2.x0, box2.y0, box2.width, box2.height * 0.95])
            box1 = ax1.get_position()
            ax1.set_position([box1.x0, box1.y0 - 0.05, box1.width, box1.height * 0.95])
            ax1.legend(loc='lower center', bbox_to_anchor=(0.5, 1), ncol=3)
        else:
            plt.figure(figsize=(5.5, 3.8))
            ax = plt.subplot(111)
            if option == 1:
                for i, item in enumerate(self.content):
                    xdata = np.linspace(0, item.time[-1], 2000)
                    plt.errorbar(item.time, item.opt_dens_norm, fmt='o', yerr=item.opt_dens_norm_err,
                                 label=item.legend, capsize=5, color='C' + str(i))
                    plt.plot(xdata, decay(xdata, *item.kin_fit_par), '-', color='C' + str(i))
            elif option == 2:
                for i, item in enumerate(self.content):
                    plt.errorbar(item.time, item.opt_dens_norm,
                                 fmt='o', yerr=item.opt_dens_norm_err, label=item.legend, capsize=5, color='C' + str(i))
            elif option == 3:
                for i, item in enumerate(self.content):
                    ax.errorbar(item.time, item.opt_dens_norm, fmt='-o',
                                yerr=item.opt_dens_norm_err, label=item.legend, capsize=5, color='C' + str(i))
            elif option == 4:
                style_list = ['--', '-']
                for i, item in enumerate(self.content):
                    plt.errorbar(item.time, item.opt_dens_norm, fmt=style_list[i % 2] + 'o',
                                 yerr=item.opt_dens_norm_err, label=item.legend,
                                 lw=1, capsize=5, color='C' + str(i // 2))
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width, box.height * 0.92])
            ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1), ncol=4)
        plt.xlabel('Czas $t$ [min]')
        plt.ylabel('Absorbancja $A$ [a.u.]')
        #plt.tight_layout()
        plt.show()

    def show_info(self):
        for item in self.content:
            item.show_info()
            print()
        for item in self.content:
            print('$' + str(round(item.rate_const, 4)) + '\pm ' + str(round(item.rate_const_err, 4)) + '$')
        for item in self.content:
            if isinstance(item, ExtendedSet):
                print('$' + str(round(item.counts_mean, 1)) + '\pm ' + str(round(item.counts_mean_err, 1)) + '$')
        for item in self.content:
            if isinstance(item, ExtendedSet):
                print(item.legend + '\t' + '$' + str(round(item.rate_const, 4)) + '\pm '
                      + str(round(item.rate_const_err, 4)) + '$' + '\t' + '$' + str(round(item.counts_mean, 1))
                      + '\pm ' + str(round(item.counts_mean_err, 1)) + '$')


    def plot_counts_raw(self):
        for item in self.content:
            if isinstance(item, ExtendedSet):
                plt.plot(item.counts_raw, '-', label=item.legend)
            else:
                print('No counts data for ' + item.label + ', skipping this series')
        plt.legend()
        plt.xlabel('Czas $t$ [a.u]')
        plt.ylabel('Zliczenia $n$ [s$^{-1}$]')
        plt.show()

    def plot_counts_raw(self):
        for item in self.content:
            if isinstance(item, ExtendedSet):
                plt.plot(item.counts_raw, '-', label=item.legend)
            else:
                print('No counts data for ' + item.label + ', skipping this series')
        plt.legend()
        plt.xlabel('Czas $t$ [a.u]')
        plt.ylabel('Zliczenia $n$ [s$^{-1}$]')
        plt.show()

    def plot_counts_intervals(self):
        for item in self.content:
            if isinstance(item, ExtendedSet):
                plt.figure(figsize=(4 * ceil(len(item.counts_interval) / 2), 5))
                plt.suptitle(item.label)
                for index, interval in enumerate(item.counts_interval):
                    plt.subplot(2, ceil(len(item.counts_interval) / 2), index + 1)
                    plt.plot(interval, '-', label='data')
                    plt.axhline(y=item.counts[index], c='r', label='fitted value')
                    plt.title('Interval ' + str(index + 1))
                    plt.legend()
                    plt.xlabel('Time $t$ [a.u]')
                    plt.ylabel('Counts $n$ [s$^{-1}$]')
                plt.tight_layout()
                plt.subplots_adjust(top=0.88)
            else:
                print('No counts data for ' + item.label + ', skipping this series')
        plt.show()

    def plot_counts_rate_const(self, option):
        counts = []
        rate_const = []
        counts_err = []
        rate_const_err = []
        for item in self.content:
            if isinstance(item, ExtendedSet):
                counts.append(item.counts_mean)
                rate_const.append(item.rate_const)
                counts_err.append(item.counts_mean_err)
                rate_const_err.append(item.rate_const_err)
            else:
                print('No counts data for ' + item.label + ', skipping this series')
        plt.figure(figsize=(5.5, 3.5))
        if option == 1:
            plt.plot(rate_const, counts, 'ko', ms=4)
        elif option == 2:
            plt.errorbar(rate_const, counts, fmt='o', ms=4, yerr=counts_err, xerr=rate_const_err, capsize=3, elinewidth=1, color='k')
        plt.xlabel('Stała szybkości $k$ [min$^{-1}$]')
        plt.ylabel('Zliczenia $n$ [s$^{-1}$]')
        plt.tight_layout()
        plt.show()


class BasicSet:
    def __init__(self, *args):
        assert len(args) in (1, 2)
        peak_file = args[0]

        # info and kinetics data loading
        file = open(peak_file, 'r')
        self.time = []
        self.opt_dens = []
        for line in file:
            if 'label' in line:
                self.label = line.split(' = ')[1].split('\n')[0]
            elif 'legend' in line:
                self.legend = line.split(' = ')[1].split('\n')[0]
            elif 'date' in line or 'data' in line:
                self.date = line.split(' = ')[1].split('\n')[0]
            elif 'lambda' in line:
                self.wavelength = float(line.split(' = ')[1].split('\n')[0])
            else:
                line_tab = line.split()
                self.time.append(float(line_tab[0]))
                self.opt_dens.append(float(line_tab[1]))
        file.close()
        self.opt_dens_norm = list(map(lambda x: x / self.opt_dens[0], self.opt_dens))
        self.opt_dens_norm_err = [0.000000001 # 0.02 / self.opt_dens[0] * np.sqrt(1 + (element / self.opt_dens[0]) ** 2)
                                  for element in self.opt_dens]

        log_file = peak_file[:-3] + 'kinfit'
        if os.path.isfile(log_file):  # simply load if already processed
            fit_file = open(log_file, 'r')
            self.rate_const = float(fit_file.readline())
            self.rate_const_err = float(fit_file.readline())
            self.kin_fit_par = [float(i) for i in fit_file.readline()[1:-2].split(', ')]
            fit_file.close()
        else:  # if .fit file does not exist
            popt_k, pcov_k = curve_fit(decay, self.time, self.opt_dens_norm, sigma=self.opt_dens_norm_err,
                                       p0=(0.0001, 1.0, 0.2), bounds=([0, 0.8, 0], [0.2, 1.1, 2]))
            err_k = np.sqrt(np.diag(pcov_k))
            print('\t\t\tofffset\t\t\tfactor\t\t\talpha')
            print('values =', popt_k)
            print('errors =', err_k)
            plt.errorbar(self.time, self.opt_dens_norm, fmt='o', yerr=self.opt_dens_norm_err, label='data',
                         capsize=5)
            xdata = np.linspace(0, self.time[-1], 2000)
            plt.plot(xdata, decay(xdata, *popt_k), '-', label='fitted curve')
            plt.xlabel('Time $t$ [min]')
            plt.ylabel('Optical density $A$ [a.u.]')
            plt.legend()
            plt.title(self.label)
            plt.show()
            accept = input(self.label + ' - kinetics fit correct? [y/n]: ')
            if accept != 'y':
                raise ValueError('Fitting unsuccessful')
            self.rate_const = popt_k[2]
            self.rate_const_err = err_k[2]
            self.kin_fit_par = list(popt_k)
            fit_file = open(log_file, 'w')
            fit_file.write(str(self.rate_const) + '\n')
            fit_file.write(str(self.rate_const_err) + '\n')
            fit_file.write(str(self.kin_fit_par) + '\n')
            fit_file.close()

    def show_info(self):
        print('Label =', self.label)
        print('Date =', self.date)
        print('Rate const =', self.rate_const, '+-', self.rate_const_err, '[1/min]')



class ExtendedSet(BasicSet):
    def __init__(self, *args):
        assert len(args) == 2
        BasicSet.__init__(self, *args)
        counts_file = args[1]

        # counts data loading and pre-processing
        self.counts_raw = []
        file = open(counts_file, 'r')
        for line in file:  # load raw data
            self.counts_raw.append(int(line))
        file.close()
        self.counts_interval = []  # divide data into intervals
        detector = False
        threshold = 50
        temp = []
        for value in self.counts_raw:
            if not detector:
                if value > threshold:
                    detector = True
                    temp = []
                    temp.append(value)
            elif detector:
                if value <= threshold:
                    detector = False
                    self.counts_interval.append(temp)
                else:
                    temp.append(value)

        log_file = counts_file[:-3] + 'ctsfit'
        if os.path.isfile(log_file):  # simply load if already processed
            fit_file = open(log_file, 'r')
            self.counts = [float(i) for i in fit_file.readline()[1:-2].split(', ')]
            self.counts_mean = float(fit_file.readline())
            self.counts_mean_err = float(fit_file.readline())
            fit_file.close()
        else:  # if .fit file does not exist
            self.counts = []
            self.counts_mean_err = 0
            plt.figure(figsize=(4 * ceil(len(self.counts_interval) / 2), 5))
            for index, item in enumerate(self.counts_interval):
                xdata = np.arange(len(item))
                popt_c, pcov_c = curve_fit(decay, xdata, item,
                                           p0=(500, 500, 0.1), bounds=([200, 50, 0], [800, 1500, 1]))
                err = np.sqrt(np.diag(pcov_c))
                print('Interval ' + str(index + 1) + '\t\t\tofffset\t\t\tfactor\t\t\talpha')
                print('\tvalues =', popt_c)
                print('\terrors =', err)
                self.counts.append(popt_c[0])
                self.counts_mean_err += err[0]
                plt.subplot(2, ceil(len(self.counts_interval) / 2), index + 1)
                plt.plot(xdata, decay(xdata, *popt_c), 'r-', label='Fitted curve')
                plt.plot(xdata, item, 'b-', label='Data')
                plt.xlabel('Time $t$ [a.u.]')
                plt.ylabel('Counts [s$^{-1}$]')
                plt.title(self.label + ': interval ' + str(len(self.counts)))
                plt.legend()
            plt.tight_layout()
            plt.show()
            self.counts_mean = np.mean(self.counts)
            self.counts_mean_err = self.counts_mean_err / 4
            accept = input(self.label + ' - counts fit correct? [y/n]: ')
            if accept != 'y':
                raise ValueError('Fitting unsuccessful')
            fit_file = open(log_file, 'a')
            fit_file.write(str(self.counts) + '\n')
            fit_file.write(str(self.counts_mean) + '\n')
            fit_file.write(str(self.counts_mean_err) + '\n')
            fit_file.close()

    def show_info(self):
        BasicSet.show_info(self)
        print('Counts mean =', round(self.counts_mean, 1), '+-', round(self.counts_mean_err, 1), '[1/s]')
