#!/usr/bin/env python
# -*- coding: utf-8 -*-

RECS_DIR = "records"
f_sampling = 44100


class ChartType:
    RAW = u'sygnał'
    MFCC = 'mfcc'
    STFT = 'stft'
    FFT = 'fft'
    STFT3D = 'stft3d'
    ENVELOPE = 'obwiednia'
    FORMANTS = 'formanty'
    PSD = 'psd'
