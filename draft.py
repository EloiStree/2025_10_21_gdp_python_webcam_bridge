import cv2
import os

# List available webcams
def list_webcams(max_devices=3):
    available = []
    for i in range(max_devices):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available

# List webcams
webcams = list_webcams()
print("Available webcams:", webcams)

if not webcams:
    print("No webcams found.")
else:
    # Open first webcam
    cam_index = webcams[0]
    cap = cv2.VideoCapture(cam_index)



        # Try to set high resolution (e.g., 4K)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

    # Read back the actual resolution (camera may adjust to supported max)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Using resolution: {width} x {height}")


    if not cap.isOpened():
        print("Failed to open webcam.")
    else:

        # Query and print common capture properties using cap.get(propId)
        properties = {
            "FRAME_WIDTH": cv2.CAP_PROP_FRAME_WIDTH,
            "FRAME_HEIGHT": cv2.CAP_PROP_FRAME_HEIGHT,
            "FPS": cv2.CAP_PROP_FPS,
            "FOURCC": cv2.CAP_PROP_FOURCC,
            "BRIGHTNESS": cv2.CAP_PROP_BRIGHTNESS,
            "CONTRAST": cv2.CAP_PROP_CONTRAST,
            "SATURATION": cv2.CAP_PROP_SATURATION,
            "HUE": cv2.CAP_PROP_HUE,
            "EXPOSURE": cv2.CAP_PROP_EXPOSURE,
            "AUTO_EXPOSURE": cv2.CAP_PROP_AUTO_EXPOSURE,
        }

        for name, pid in properties.items():
            val = cap.get(pid)
            if name == "FOURCC":
                f = int(val)
                # decode fourcc (may contain non-printable chars)
                fourcc = "".join([chr((f >> (8 * i)) & 0xFF) for i in range(4)]).strip()
                print(f"{name}: {fourcc!r} ({f})")
            else:
                print(f"{name}: {val}")

        
        # Read one frame
        ret, frame = cap.read()
        byte_arrays_color_32f = frame.tobytes()
        print(f"Captured frame size: {len(byte_arrays_color_32f)} bytes")
        image_length = len(byte_arrays_color_32f)
        chunk_count = image_length / 32768
        print(f"Chunk count (32768 bytes each): {chunk_count}")
        # create liste of byte arrays with chunk size +4 bytes in front
        # copy the byte in the array after the 4 bytes
        array_chunk_bytes = []
        for i in range(int(chunk_count) + 1):
            start_index = i * 32768
            end_index = start_index + 32768
            chunk = byte_arrays_color_32f[start_index:end_index]
            chunk_size = len(chunk)
            byte_array_with_size = chunk_size.to_bytes(4, byteorder='little') + chunk
            array_chunk_bytes.append(byte_array_with_size)
        print(f"Total chunks created: {len(array_chunk_bytes)}")
        

        if ret:
            # Save screenshot
            filename = "webcam_screenshot.jpg"
            cv2.imwrite(filename, frame)
            print(f"Screenshot saved as {filename}")
        else:
            print("Failed to capture image.")

        cap.release()
