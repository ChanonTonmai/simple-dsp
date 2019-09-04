# -*- coding: utf-8 -*-

from filter_design_main import filter_design
from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show

taps_fir = filter_design(128, [30.0],'FIR','lowpass',100.0,'hamming')

taps_fir.filter_visualize(None)

sample_rate = 100.0
nsamples = 400
t = arange(nsamples) / sample_rate
x = 5*sin(2*pi*0.5*t) + 2*sin(2*pi*2.5*t+0.1) + \
        0.2*sin(2*pi*15.3*t) + 0.1*sin(2*pi*16.7*t + 0.1) + \
            0.1*sin(2*pi*23.45*t+.8)

            
            
figure(1)
clf()
plot(t,x)

x_f = taps_fir.signal_conv(None,x)
figure(2)
clf()
plot(t,x_f)