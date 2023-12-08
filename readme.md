# SDXL turbo virtual webcam

This script passes your webcam feed into SDXL turbo img2img and streams it to a virtual cam you can use.

## Quickstart

Disclaimer: this is only tested on Linux. Prepare to fight some drivers and missing libs. This command will be your ally in dark times:

```
sudo modprobe -r v4l2loopback && sudo modprobe v4l2loopback devices=1 video_nr=4 card_label="Virtual" exclusive_caps=1 max_buffers=2
```

At the least:
```
sudo apt-get install v4l2loopback-dkms
sudo apt-get install python3-dev
```

Then clone this repo.

```
poetry install
```

Go to `img2img.py` and update the `CACHE_DIR`

```
poetry shell
python cam.py
```

You should now have a virtual cam. Use the keymap popup to activate keybindings.
