# L+SAMPLER
Neural Sampler for mixing two sounds together.


<p align="center">
  <img src="https://user-images.githubusercontent.com/36171138/178837912-df01029c-ddd1-4276-a6f4-e6351407bd79.png" />
</p>

## Installation
Download repo and then install requirements:
```
pip install -r requirements.txt
```

## Usage
Run app.py with:
```
python3 app.py
```

You can: select two samples, preview a sample by clicking on it's name, press generate button to generate a new sample,
 press random button to sample random sound, preview generated sample by pressing on piano roll using keyboard or mouse, export your file by pressing export button

You can add your own samples in /samples directory.

## RAVE
This project uses RAVE model (trained on NSynth dataset).
[Check out RAVE](https://github.com/acids-ircam/RAVE)

## NSynth
This project uses files from NSynth dataset as an example. [Check out NSynth](https://magenta.tensorflow.org/datasets/nsynth)
