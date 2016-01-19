#!/usr/bin/env python
# -*- coding: utf-8 -*-

RECS_DIR = "records"
f_sampling = 44100


class ChartType:
    RAW = u'Sygnał'
    MFCC = 'MFCC'
    STFT = 'STFT'
    FFT = 'FFT'
    STFT3D = 'STFT3D'
    FORMANTS = 'Formanty'
    PSD = 'PSD'