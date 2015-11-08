import numpy as np


def decode(raw_data, d_type, samples_per_channel, num_of_channels):
    '''
    :param raw_data: bytestring - kazda probka to 2 bajty. Probki na zmiane, tj. [Left(n-1), Right(n-1), Left(n), ...]
    :param d_type: Typ z biblioteki numpy okreslajacy dlugosc probki oraz format odkodowania hexa (tutaj 16 bitow, int)
    :param samples_per_channel: Ilosc probek na kanal oraz ilosc wierszy macierzy
    :param num_of_channels: Ilosc kanalow oraz ilosc kolumn macierzy
    :return: Macierz numpy integerow dla obu kanalow
    '''
    result = np.fromstring(raw_data, d_type)
    result = np.reshape(result, (samples_per_channel, num_of_channels))
    return result


def bytestring_to_intarray(bstring):
    bytestring_interleaved = b''.join(bstring)
    int_array = decode(bytestring_interleaved, np.int16, len(bytestring_interleaved)/4, 2)
    return int_array