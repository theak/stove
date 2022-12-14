# Stove: Detect whether or not a light is on using openCV and optionally send values to Home Assistant
Detect whether or not a certain colored light exists within a camera frame. E.g. if your stove has a light you can use this to detect the on state and send it to Home Assistant by mounting a camera above the light.

## First install requirements
- pip3 install opencv-python hassapi [flask]
- Ideally do this from virtualenv
- For certain OSes (e.g. Ubuntu), you can use "sudo apt install" instead of pip

## Next edit "config.json"
- type: url or file 
  - Requires specifying either "url" (stream URL- e.g. from an IP camera) or "file" (.jpg file path) field
- debug: whether or not to preview image (set to false for headless)
- hassurl: Optional Home Assistant URL for updating values in Home Assistant
  - Requires specifying "hasstoken" and "hassboolean" to toggle on state change
  - "num_on_frames" and "num_off_frames" are number of frames to verify before changing the state- higher number prevents fluctuations
  - "delay" is how long to wait between each frame in seconds (decimal values like 0.1 are ok)
- lower/upper: Lower/upper bounds for color of region to search for in image (B, G, R)
- max_area: Max area of region to search for. Start by setting this arbitrarily high (e.g. 9999999) then narrowing down for your use case
- min_max: Bounds to search within: [[min_x, min_y], [max_x, max_y]]. No need to specify this in the config- just use "python get_bounds.py" to autopopulate based on QR code location in the frame.

## Then run "python get_bounds.py"
Place a QR code within the frame and run "python get_bounds.py" to update config.json with the region to scan.

## Now run "python main.py"
Returns whether or not the region is detected and optionally updates Home Assistant

## detect.sh
Runs main.py in a loop. Perfect for running in a cronjob every minute. Eg:
    * 08-22 * * * cd [path_to_dir] && ./detect.sh

## app.py
Optional flask server for recording images and recallibrating QR code. "flask run" to start. Deploy w/ gunicorn and nginx.

## save.py [on/off]
Saves current image to img/ folder with on/off state prepended. Usage: "python save.py [on/off]"

## test.py
Runs detection on all of the saved images in the img/ folder. Ideal for tweaking config values and getting them work reliably.