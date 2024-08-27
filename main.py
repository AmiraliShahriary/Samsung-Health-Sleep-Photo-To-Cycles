import cv2
import numpy as np

# Define the path to your image file
image_path = r'/home/amirali/Desktop/amirali/n1.jpg'  # Update this path

# Example for color ranges ( after you found them with detect_color.py)
COLOR_RANGES = {
    'Awake': ([45, 105, 195], [140, 175, 255]),
    'REM': ([208, 172, 85], [255, 199, 150]),
    'Light': ([175, 95, 75], [255, 145, 120]),
    'Deep': ([95, 20, 5], [170, 65, 60])
}



def detect_sleep_segments(image_path, color_ranges, min_segment_width=5):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Could not open or find the image: {image_path}")

    sleep_segments = []

    # Loop over each defined color range to detect sleep stages
    for stage, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # mask for the specific sleep stage color
        mask = cv2.inRange(image, lower, upper)

        # contours of the masked regions
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # through contours to calculate  duration of each detected segment
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # segments that are too small
            if w < min_segment_width:
                continue

            # duration based on the width of the segment
            total_duration_minutes = 240  # example total duration (in minute)
            total_width_pixels = image.shape[1]
            segment_duration = (w / total_width_pixels) * total_duration_minutes

            sleep_segments.append((stage, round(segment_duration, 2), (x, y, w, h)))

    sleep_segments.sort(key=lambda seg: seg[2][0])

    return sleep_segments


def summarize_sleep_segments(segments):
    summary = {}
    for stage, duration, _ in segments:
        if stage in summary:
            summary[stage] += duration
        else:
            summary[stage] = duration

    return summary


segments_filtered = detect_sleep_segments(image_path, COLOR_RANGES, min_segment_width=10)

print("Detected sleep segments and their durations:")
for stage, duration, _ in segments_filtered:
    print(f"{stage}: {duration} minutes")

sleep_summary = summarize_sleep_segments(segments_filtered)

print("\nSummary of total durations for each sleep stage:")
for stage, total_duration in sleep_summary.items():
    print(f"{stage}: {total_duration} minutes")