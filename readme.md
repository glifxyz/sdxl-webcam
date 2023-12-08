# SDXL turbo virtual webcam

This script passes your webcam feed into SDXL turbo img2img and streams it to a virtual cam you can use.
Around 15 fps on a 3080.

![Alt text](demo.gif)

## Quickstart

At the least:
```shell
sudo apt-get install v4l2loopback-dkms
sudo apt-get install python3-dev
```

Then clone this repo.

```shell
poetry install
```

Download the wheel from https://github.com/chengzeyi/stable-fast/releases/tag/v0.0.13.post3

```shell
poetry shell
pip install <sd-fast wheel>
```

Go to `img2img.py` and update the `CACHE_DIR`


```shell
python cam.py
```

You should now have a virtual cam. Use the keymap popup to activate keybindings.

Disclaimer: this is only tested on Linux. Prepare to fight some drivers and missing libs. This command will be your ally in dark times:

```shell
sudo modprobe -r v4l2loopback && sudo modprobe v4l2loopback devices=1 video_nr=4 card_label="Virtual" exclusive_caps=1 max_buffers=2
```

## Acknowledgements

- SDXL turbo: https://huggingface.co/stabilityai/sdxl-turbo
- stable-fast: https://github.com/chengzeyi/stable-fast
- tiny autoencoder: https://huggingface.co/madebyollin/taesd
