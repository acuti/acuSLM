"""acuSLM: measure Leq, L90, Lmin, Lmax linear and A-weighted"""
"""work in progress"""
# To be imported (and installed if not in the system): 
# Used for acquiring audio stream:
import pyaudio
# Used for acquiring various operations on data arrays:
from numpy import mean, square, log10, percentile, fromstring 
# Used for A-weighting:
from scipy.signal import lfilter
# included in the package:
from A_weighting import A_weighting 

# Constants
CHUNK = 1024
RECORD_SECONDS = 5
FORMAT = pyaudio.paInt32 # 24 bit enough, but 32 for coherence with numpy dtype 
CHANNELS = 1             # for 1 microphone
RATE = 48000             # for Class 1 measurements
TIMEWEIGHTING = 0.125    # Fast (F) time weighting, s
MAXMV = 5000             # max mV input
MAXINT32 = 2**32/2       # max negative value of numpy dtype="int32"
MVOLTIZE = MAXMV/MAXINT32# convert int32 dtype to mV
PA0 = square(2*10E-5)    # reference pressure squared
SENSITIVITY = 47.9       # my class 1 Dr. Jordan xlr mic
CALIBRATION = 1.3        # should be 0.4 from calibration chart, 10m cable loss?

# we are innterested in pressure squared, not pressure, therefore mean square
def ms2dB(a, sensitivity, re, calibration):
    """Convert mean square mV to dB re 20 microPA"""
    rmsPa = a / sensitivity
    rmsRE = rmsPa / re
    dB = 10 * log10(rmsRE) + calibration
    return dB
    
# Pyaudio import stream
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

l_pressures2 = []
a_pressures2 = []
l_db = []
a_db = []

for j in range(0, int(RECORD_SECONDS / TIMEWEIGHTING)):
    data = stream.read(int(RATE * TIMEWEIGHTING))
    # from int32 dtype to mV
    l_data = fromstring(data, dtype="int32") * MVOLTIZE
    # A frequency filtering /weighting
    b, a = A_weighting(RATE)
    a_data = lfilter(b, a, l_data)
    # mean squaring linear and A-weighted
    l_ms = mean(square(l_data))
    a_ms = mean(square(a_data))
    # append to arrays
    l_pressures2.append(l_ms)
    a_pressures2.append(a_ms)
    # from mean square mV to dB re 20 microPa
    # progressing Leq
    leq_l = ms2dB(mean(l_pressures2),SENSITIVITY,PA0,CALIBRATION)
    leq_a = ms2dB(mean(a_pressures2),SENSITIVITY,PA0,CALIBRATION)
    # instantaneous Leq
    db_lin = ms2dB(l_ms,SENSITIVITY,PA0,CALIBRATION)
    db_a = ms2dB(a_ms,SENSITIVITY,PA0,CALIBRATION)
    # append instantaneous Leq data to arrays
    l_db.append(db_lin)
    a_db.append(db_a)
    # uncomment line below for sample-by-sample CLI output (slowing down processes), keeping indentation
    #print("Li: %.1f" % db_lin + " dB, " + "%.1f" % db_a + " dB(A); " + "Leq: %.1f" % leq_l + " dB, " + "%.1f" % leq_a + " dB(A)")

# Close  stream 
stream.stop_stream()
stream.close()
p.terminate()
# return Leq, L90, Lmin, Lmax
l90_l = percentile(l_db,10)
l90_a = percentile(a_db,10)
lmin_l = min(l_db)
lmin_a = min(a_db)
lmax_l = max(l_db)
lmax_a = max(a_db)

print("Done. Final values:")
print("Leq: %.1f" % leq_l + " dB, " + "%.1f" % leq_a + " dB(A)\n" + "L90: %.1f" % l90_l + " dB, " + "%.1f" % l90_a + " dB(A)\n" + "Lmin: %.1f" % lmin_l + " dB, " + "%.1f" % lmin_a + " dB(A)\n" + "Lmax: %.1f" % lmax_l + " dB, " + "%.1f" % lmax_a + " dB(A)")
