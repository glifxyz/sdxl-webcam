import cv2
import pyvirtualcam
import numpy as np
import math
from img2img import process_frame
from PIL import Image
import time

# Capture from the OBS virtual camera
# The index '0' might need to be changed depending on your setup
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# Get the default camera resolution
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Camera resolution: {width}x{height}")

# Define some parameters
prompts = [
    "a man with glasses",
    "a soldier operator with helmet, desert storm",
    "neo from the matrix in cyberspace",
    "an astronaut, interstellar",
    "carbon fiber robot",
    "a king, medieval times",
    "anime girl",
    "dragon born warlock",
    "medusa, stone sculpture",
    "the devil, red skin, horns",
    "santa claus",
]
prompt_suffix = ", headphones"
current_prompt_index = 0
prompt = prompts[current_prompt_index]
strength_steps_combos = [
    (.2, 5),
    (.3, 4),
    (.4, 3),
    (.5, 2),
    (.6, 2),
    (.7, 2),
    (.8, 2),
    (.9, 2),
    (1., 1),
]
current_combo_index = 3
strength, steps = strength_steps_combos[current_combo_index]
strength = 0.5
blend = 0.0
seed = np.random.randint(0, 10000000000)
cycle_seeds = False
show_hud = False

frame_timer = time.time()

# load keymap
keymap = cv2.imread("keymap.png")

# Start the virtual camera
# If you get a v4l2 error, try this:
# sudo modprobe -r v4l2loopback && sudo modprobe v4l2loopback devices=1 video_nr=4 card_label="Virtual" exclusive_caps=1 max_buffers=2
with pyvirtualcam.Camera(width=width, height=height, fps=30, device="/dev/video4") as cam:
    print(f'Using virtual camera: {cam.device}')

    while True:
        # Capture frame-by-frame
        ret, cv_frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        # convert the frame to pillow image
        cv_frame = cv2.cvtColor(cv_frame, cv2.COLOR_BGR2RGB)
        frame = cv_frame / 255.0

        if cycle_seeds:
            seed = np.random.randint(0, 10000000000)
        frame = process_frame(frame, prompt + prompt_suffix, strength, steps, seed)
        frame = (frame * 255).astype(np.uint8)

        # blend the original frame with the processed frame
        frame = cv2.addWeighted(cv_frame, 1.0 - blend, frame, blend, 0)

        if show_hud:
            # calc time real quick
            passed_time = time.time() - frame_timer
            frame_timer = time.time()
            fps = round(1.0 / passed_time)

            font_size = 0.5
            spacing = 20
            cv2.putText(frame, f"[w/s] prompt: {prompt}", (10, spacing), cv2.FONT_HERSHEY_COMPLEX, font_size, (255, 255, 255), 1)
            cv2.putText(frame, f"[e/d] strength: {strength}", (10, 2*spacing), cv2.FONT_HERSHEY_COMPLEX, font_size, (255, 255, 255), 1)
            cv2.putText(frame, f"[e/d[ steps: {steps}", (10, 3*spacing), cv2.FONT_HERSHEY_COMPLEX, font_size, (255, 255, 255), 1)
            cv2.putText(frame, f"[r/f] blend: {blend}", (10, 4*spacing), cv2.FONT_HERSHEY_COMPLEX, font_size, (255, 255, 255), 1)
            cv2.putText(frame, f"[z]   cycle_seeds: {cycle_seeds}", (10, 5*spacing), cv2.FONT_HERSHEY_COMPLEX, font_size, (255, 255, 255), 1)
            cv2.putText(frame, f"[x]   show_hud: {show_hud}", (10, 6*spacing), cv2.FONT_HERSHEY_COMPLEX, font_size, (255, 255, 255), 1)
            cv2.putText(frame, f"fps   {fps}", (10, 7*spacing), cv2.FONT_HERSHEY_COMPLEX, font_size, (255, 255, 255), 1)

        # Output the frame to the virtual camera
        cam.send(frame)
        cam.sleep_until_next_frame()

        # Display the resulting frame (optional)
        cv2.imshow('keymap', keymap)
        
        # # Handle key presses
        key = cv2.waitKey(1)
        if key == ord('w'):
            current_prompt_index = (current_prompt_index + 1) % len(prompts)
            prompt = prompts[current_prompt_index]
            print(f"prompt: {prompt}")
        elif key == ord('s'):
            current_prompt_index = (current_prompt_index - 1) % len(prompts)
            prompt = prompts[current_prompt_index]
            print(f"prompt: {prompt}")
        elif key == ord('e'): # increase strength
            current_combo_index = (current_combo_index + 1) % len(strength_steps_combos)
            strength, steps = strength_steps_combos[current_combo_index]
            print(f"strength_step: {strength_steps_combos[current_combo_index]}")
        elif key == ord('d'): # decrease strength
            current_combo_index = (current_combo_index - 1) % len(strength_steps_combos)
            strength, steps = strength_steps_combos[current_combo_index]
            print(f"strength_step: {strength_steps_combos[current_combo_index]}")
        elif key == ord('r'): # increase blend
            blend = round(blend + 0.1, 1)
            blend = min(blend, 1.0)
            print(f"blend: {blend}")
        elif key == ord('f'): # decrease blend
            blend = round(blend - 0.1, 1)
            blend = max(blend, 0.)
            print(f"blend: {blend}")
        elif key == ord('z'): # cycle seeds
            cycle_seeds = not cycle_seeds
            print(f"cycle_seeds: {cycle_seeds}")
        elif key == ord('x'): # show hud
            show_hud = not show_hud
            print(f"show_hud: {show_hud}")
        elif key == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()