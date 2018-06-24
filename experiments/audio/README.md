# Audio samples conversions tools

In order to convert a wav file into a raw one:

    sox bleep.wav -t raw -c 1 -r 8000 bleep8.raw
    ./raw2h.py bleep8.raw

