# acuSLM

## Synopsis

This code aims at obtaining various acoustic level parameters from a microphone signal, as a sound level meter (SLM) would.  This is a very early stage in the development, testing and contributions are most welcome.

## Code Example

At present, this code only runs by a call on a CLI. Provided your machine meets all dipendencies (see [Installation](https://github.com/acuti/acuSLM#installation) below), it is as simple as running:
- *python -i acuSLM.py*

in your cloned directory (*-i* option logs you to a python session at the end of the script run where values are stored for variables of the run. etc.).
The first run is meant for calibration.  You need to tweak the constants at the beginning of acuSLM.py, in particular:
- *SENSITIVITY* (mV/Pa) to match your microphone sensitivity
- *CALIBRATION* (dB), for compensation of level drift from calibrator reference level
- possibly *MAXMV*, to convert the normalized array to milliVolts.

I would suggest not touching the other constants.

## Motivation

My aim is to provide a software backend to a class 1 microphone + calibrator I have, so that I can have a properly working SLM.  Once the calculation core is stable and tested, it might be extended to fractional band analysis, sound insulation measurements, impulse response measurements, etc.  Also, it might be developed to a standalone GUI application.
The GPL license will hopefully ease contributions, both for testing and development; it already provides for transparency of operation.

## Installation

At present the code runs on a CLI (see [Code Example](https://github.com/acuti/acuSLM#code-example)).  These are the external python modules it depends on:
- pyaudio
- numpy
- scipy

## API Reference

wip

## Tests

See [Code Example](https://github.com/acuti/acuSLM#code-example) for calibration and testing.  The hardcoded constants in *acuSLM.py* allow for my microphone to be calibrated correctly.  However I have not done any side-by-side testing with a certified SLM yet. If you manage to, any feedback would be  mostly appreciated.
This software comes with no warranty whatsoever, expecially with regards to providing meaningful sound level readings.

## Contributors

- *pieracuti* - Pierpaolo Pilla, *acustica@acuti.net*
- The script *A_weighting.py* is by @endolith, you can find his repository [here](https://gist.github.com/endolith/148112)

## License

[AGPL](https://www.gnu.org/licenses/agpl.html)
