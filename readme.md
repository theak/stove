# Stove: Detect whether or not a light is on using openCV and optionally send values to Home Assistant
Perfect for detecting whether or not a stove is on, or any other use case.

## First edit "config.json"
- type: url or file 
  - Requires specifying either "url" (stream URL- e.g. from an IP camera) or "file" (.jpg file path) field
- debug: whether or not to preview image (set to false for headless)
- hassurl: Optional Home Assistant URL for updating values in Home Assistant
  - Requires specifying "hasstoken" and "hassboolean" to toggle on state change
- lower/upper: Lower/upper bounds for color of region to search for in image (B, G, R)
- max_area: Max area of region to search for

## Then run "python get_bounds.py"
Place a QR code within the frame and run "python get_bounds.py" to update config.json with the region to scan.

## Now run "python main.py"
Returns whether or not the region is detected and optionally updates Home Assistant

## detect.sh
Runs main.py in a loop. Perfect for running in a cronjob every minute. Eg:
    * 08-22 * * * cd [path_to_dir] && ./detect.sh

## app.py
Optional flask server for recording images and recallibrating QR code. "flask run" to start. Deploy w/ gunicorn and nginx.
