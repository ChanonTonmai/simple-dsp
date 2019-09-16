# Written by K. Chanon
# 3 Sep 2019
# vDeSi King Mongkut's University of Technology Thonburi
import numpy as np
import scipy.signal as signal
from pylab import *

class filter_design(object):

    def create_tabs(self, N, cutoff, filterDesign, filterType, fs, windowStyle):

        self.filterDesigns = ['IIR','FIR']
        self.filterTypes1 = ['lowpass','highpass','bandpass']
        self.filterTypes2 = ['bandstop','bandpass','Bandstop','Bandpass']

        self.isThereAnError = 1 #if there was no error then it will be set to 0
        self.COEFFS = [0]

        if filterDesign not in self.filterDesigns:
            print('Gave wrong filter design! Remember: IIR or FIR.')
        elif filterType not in self.filterTypes1 and filterType not in self.filterTypes2:
            print('Gave wrong filter type! Remember: lowpass, highpass', 
                  ', bandpass, bandstop.')
        elif fs < 0:
            print('The sampling frequency has to be positive!')
        else:
            self.isThereAnError = 0
        
        #if fs was given then the given cutoffs need to be normalised to Nyquist
        if fs and self.isThereAnError == 0:
            for i in range(len(cutoff)):
                cutoff[i] = float(cutoff[i])/float(fs/2)

        if filterDesign == 'FIR' and filterType == 'lowpass' and self.isThereAnError == 0:
            self.COEFFS = signal.firwin(N, cutoff, window=windowStyle, pass_zero=True)
        elif filterDesign == 'FIR' and filterType == 'highpass' and self.isThereAnError == 0:
            N |= 1
            self.COEFFS = signal.firwin(N, cutoff, window=windowStyle, pass_zero=False)
        elif filterDesign == 'FIR' and filterType == 'bandpass' and self.isThereAnError == 0:
            N |= 1
            self.COEFFS = signal.firwin(N, cutoff,  window=windowStyle, pass_zero=False) 
        elif filterDesign == 'FIR' and filterType == 'bandstop' and self.isThereAnError == 0:
            N |= 1
            self.COEFFS = signal.firwin(N, cutoff, window=windowStyle,) 
        elif filterDesign == 'IIR' and self.isThereAnError == 0:
            self.COEFFS = np.asarray(signal.butter(N, cutoff, btype=filterType, output='ba'))
        else: 
            self.COEFFS = -1
            print('Something Wrong')

        return self.COEFFS

    def __init__(self,N, cutoff, filterDesign, filterType, fs, windowStyle):
        self.COEFFS = self.create_tabs(N, cutoff, filterDesign, filterType, fs, windowStyle)
        self.fs = fs
        self.fc = cutoff[0]*fs/2

    def filter_visualize(self, scale):
        taps = self.COEFFS
        fs = self.fs
        fc = self.fc

        upper = fc*10
        lower = 0
    

        figure(1)
        clf()
        if taps.ndim == 1: 
            w, h = signal.freqz(taps, worN=2**13)
            nyq_rate = float(fs/2)
            mag = (w/pi)*nyq_rate
            if scale=='dB':
                figure(1)
                clf()
                xlim(lower, upper)
                plot(mag, 20*np.log10(absolute(h)), linewidth=2)
                xlabel('Frequency (Hz)')
                ylabel('Gain (dB)')
                title('Frequency Response')
                grid(True)
            else:
                figure(1)
                clf()
                xlim(lower, upper)
                plot(mag, absolute(h), linewidth=2)
                xlabel('Frequency (Hz)')
                ylabel('Gain')
                title('Frequency Response')
                grid(True)
        else: 
            w, h = signal.freqz(taps[0], taps[1], worN=2**13)
            nyq_rate = float(fs/2)
            mag = (w/pi)*nyq_rate
            
            if scale=='dB':
                figure(1)
                clf()
                plot(mag, 20*np.log10(absolute(h)), linewidth=2)
                xlim(lower, upper)
                xlabel('Frequency (Hz)')
                ylabel('Gain (db)')
                title('Frequency Response')
                grid(True)
            else: 
                figure(2)
                clf()
                xlim(lower, upper)
                plot(mag, absolute(h), linewidth=2)
                xlabel('Frequency (Hz)')
                ylabel('Gain')
                title('Frequency Response')
                grid(True)
            
    def coeff_save(self, param):
        taps = self.COEFFS
        if taps.ndim == 1:
            name = 'coeff_' + param + '.csv'
            np.savetxt(name, taps)
        else: 
            name_b = 'coeff_b' + param + '.csv'
            name_a = 'coeff_a' + param + '.csv'
            np.savetxt(name_b, taps[0])
            np.savetxt(name_a, taps[1])
            
    def signal_conv(self, taps, signal_input):
        if taps is None:
            taps = self.COEFFS
        if taps.ndim == 1:
            b = taps
            a = 1.0
        else:
            b = taps[0]
            a = taps[1]
        print(a)
        print(b)
        self.filt_res = signal.lfilter(b,a,signal_input)
        return self.filt_res
        
        
