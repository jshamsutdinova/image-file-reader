#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 13:46:06 2022

@author: jshamsutdinova
"""
import numpy as np
import spectrum
from datetime import datetime


class IRNRGetData:
    """ This class operate with txt file to get IRNR data """
    def __init__(self, fpath):
        self.fpath = fpath
    
    def open_file(self):
       """ Return lines from text file """ 
       with open(self.fpath) as f:
            lines = f.readlines()
            return lines
    
    def  get_flux_data(self):
        """ Create array with flux data derived from txt file """
        flux = np.array([])        
        
        for line in self.open_file()[1:]:
            split_line = line.split('\t')
            flux = np.append(flux, float(split_line[3]))
        
        return flux
    
    def get_time_data(self):
        """ Create array with time data derived from txt file """
        tm_array = np.array([])

        for line in self.open_file()[1:]:
            split_line = line.split('\t')
            tm = split_line[1]
            tm_array = np.append(tm_array, self.convert_to_seconds(tm))
        
        return tm_array
    
    def convert_to_seconds(self, tm):
        """ Convert string time to time object in seconds """
        tm_obj = datetime.strptime(tm, '%H:%M:%S.%f')
        tm_sec = spectrum.time_to_seconds(tm_obj.time())
        
        return tm_sec


    