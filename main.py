import time
import sys
import cv2

video_file = "badappleshort.mp4"
output_width = 30 #in characters
frame_rate = 60

def get_frames(path):
    frames = []
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("Could not open video file.")
        exit()
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            sys.stdout.write("\033[H\033[J")
            sys.stdout.write("◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️100% Done!")
            sys.stdout.flush()
            break
        frame_text = ""
        height, width, channels = frame.shape
        output_height = int(height / width * output_width )
        for row in range(output_height):
            for collumn in range(output_width):
                section = frame[height//output_height * row:height//output_height * (row + 1), width//output_width * collumn:width//output_width * (collumn + 1)]
                bgr_average = section.mean(axis=(0, 1))
                blue, green, red = map(int, bgr_average)
                brightness = (red*0.299 + green*0.587 + blue*0.114) / 255 #0 to 1
                if brightness < 0.2:
                    frame_text += " "
                elif brightness < 0.4:
                    frame_text += (".")
                elif brightness < 0.6:
                    frame_text += ("*")
                elif brightness < 0.8:
                    frame_text += ("#")
                else:
                    frame_text += ("◼️")
                if collumn == output_width - 1:
                    frame_text += "\n "
        frames.append(frame_text)
        frame_number += 1
        sys.stdout.write("\033[H\033[J")
        sys.stdout.write("◼️"*int(frame_number / total_frames * 10)+"-"*(10-int(frame_number / total_frames * 10))+str(int(frame_number / total_frames * 100))+"% ("+str(frame_number)+"/"+str(total_frames)+")")
        sys.stdout.flush()

    return(frames)
            


def main():
    frames = get_frames(video_file)
    ready = input(f"\nPress Enter to start the animation...")
    if ready == "":
        replay = "r"
        while replay == "r":
            for frame in frames:
                sys.stdout.write("\033[H\033[J")
                sys.stdout.write(f"{frame}\n")
                sys.stdout.flush()
                time.sleep(1/frame_rate)
            replay = input("Press r to replay or any other key to exit...")
        

if __name__ == "__main__":
    main()