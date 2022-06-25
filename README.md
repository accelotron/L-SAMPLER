# L+SAMPLER
Neural Sampler for mixing two sounds together.

![l+synth interface](https://user-images.githubusercontent.com/36171138/175765146-17308de7-3de2-4b2d-94aa-0a8cf0bc4bb8.png)

## Installation
Download repo and then install requirements:
'''
pip install -r requirements.txt
'''

## Usage
You can: select two samples using two file viewers, preview a sample by clicking on it's name, press generate button to generate a new sample,
preview generated sample by pressing on piano roll using keyboard or mouse, export your file by pressing export button

You can add your own samples, but there is a couple of details, that you should keep in mind: files that you mix must be equal lenght (can be different sample rate) and samples path must contain at least one file

## RAVE
This project uses pre-trained RAVE model (trained on NSynth dataset), but doesn't include any parts of RAVE source code.
[Check out RAVE](https://github.com/acids-ircam/RAVE)

## NSynth
This project uses files from NSynth dataset as an example. [Check out NSynth](https://magenta.tensorflow.org/datasets/nsynth)
