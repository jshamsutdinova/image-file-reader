#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:31:50 2022

@author: jshamsutdinova
"""
import numpy as np
import spectrum
from astropy.io import fits


class CallistoGetData:
    """ This class operate with FITS file of e-Callisto"""
    
    
    def __init__(self, fpath):
        self.fpath = fpath
        self.hdu_list = fits.open(fpath)
        self.time_diff = self.hdu_list[0].header['CDELT1']
        self.time_start = self.hdu_list[0].header['CRVAL1']
        self.time_end = (self.hdu_list[0].header['NAXIS1'] - 1) * self.time_diff + self.time_start
    
    def get_spectrum(self):
        """ Return array of spectrum data """
        data = self.hdu_list[0].data
        spectrum = np.flipud(data[:192])
        
        return spectrum
    
    def get_freq_value(self):
        """ Return frequency values of instrument """
        ext = self.hdu_list[1].data
        freq = ext['FREQUENCY']
        
        return freq
        
    def time_formatter(self, x, pos):
        """ Create time formatter for X axis """
        return (x*0.25 + self.time_start)

    def freq_formatter(self, x, pos):
        """ Create frequency formatter for Y axis """
        freq = self.get_freq_value()
        freq_diff = abs(freq[:, 1] - freq[:, 0])
        
        return round((x*(freq_diff) + freq[:, -1])[0])
    
    def create_time_array(self):
        """ Create array with time format values """
        time_array = np.arange(self.time_start, self.time_end, self.time_diff)
        
        return time_array
    
    def get_avg_frequency(self, array, freq_from, freq_to):
        """ Return average frequency for specified range """
        avg_freq = []
        freq_avlbl_arr = self.get_freq_value()
        for i in range(array.shape[1]):
            avg_value = 0
            sum_value = []
            for freq in range(freq_from, freq_to):
                index = spectrum.find_nearest_index(freq_avlbl_arr, freq)
                sum_value.append(array[index][i])
            avg_value = (np.mean(sum_value))
            avg_freq.append(avg_value)
        
        return np.array(avg_freq)

