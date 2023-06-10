import streamlit as st
import cv2
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import os
import ffmpeg

class my_dictionary(dict):
 
  def __init__(self):
    self = dict()
 
  def add(self, key, value):
    self[key] = value


def main():
    # Streamlit configuration
    st.set_page_config(page_title='Ship Water Level Detection App')

    # Title and description
    st.title('Ship Water Level Detection App')
    st.write('Upload a video file to get the Survay')

    # Video file upload
    video_file = st.file_uploader('', type=['mp4', 'avi'])

    if video_file is not None:
        # Read video file
        video = cv2.VideoCapture(video_file.name)
        font = cv2.FONT_HERSHEY_SIMPLEX

        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        output_path = "./output.mp4"  # Replace with the desired output video file path
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs as well
        output_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        reader = easyocr.Reader(['en'], gpu=True)

        frame_count = 0
        text_dict = my_dictionary()
        frame_count = 0
        while video.isOpened():
            ret, frame = video.read()
            if frame_count % 3 == 0:
                text1 = ''
                frame_count = frame_count + 1
                spacer = 10

                if not ret:
                    break

                result = reader.readtext(frame)

                if result:
                    for detection in result:
                        spacer += 15

                if detection:
                    top_left = tuple(detection[0][0])
                    bottom_right = tuple(detection[0][2])

                    if detection[1].isdigit():
                        if int(detection[1]) != 0:
                            text = detection[1]
                            print(text)

                        if text in text_dict:
                            text_dict[text] += 1
                        else:
                            text_dict[text] = 1
                    else:
                        text1 = 'Detecting..'

                    if text_dict == {}:
                        avg_list = 'Detecting...'
                    else:
                        avg_list = 'Detecting...'

                    frame = cv2.rectangle(frame, (int(top_left[0]), int(top_left[1])), (int(bottom_right[0]), int(bottom_right[1])), (0, 255, 0), 3)
                    if text1 == '':
                        frame = cv2.putText(frame, text, (20, spacer), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    elif text1 == 'Detecting..':
                        frame = cv2.putText(frame, text1, (20, spacer), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    frame = cv2.putText(frame, "Displacement: 543,2341 mt", (20, spacer + 30), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    frame = cv2.putText(frame, "Exported: 4356,23 M Tonne", (20, spacer + 45), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    frame = cv2.putText(frame, "Remarks: 874,34 mt", (20, spacer + 60), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    
                    # st.image(frame, channels='BGR', caption='Video Frame')
                    # st.write('Extracted Text:', text)
                    # st.write('Water Density:', 12345)
                    # st.write('Exported:', 12345)
                    # st.write('Misplacement:', 122312)
                    # st.write(text_dict)

            else:
                frame_count = frame_count + 1
            output_video.write(frame)
        
        # # Check if there are any two-digit keys in the dictionary
        # has_two_digit_keys = any(key >= 10 for key in my_dict)

        # # Filter the dictionary based on the condition
        # filtered_dict = {key: value for key, value in my_dict.items() if not (key < 10 and has_two_digit_keys)}

        max_values = sorted(text_dict.values(), reverse=True)[:2]
        
        max_keys = [key for key, value in text_dict.items() if value in max_values]

        key_list = []
        for key in max_keys:
            value = text_dict[key]
            key_list.append(key)
            # print("Key:", key, "Value:", value)

        if len(max_keys) == 2:
            # top = max(max_keys, key=text_dict.get)
            # max_keys.remove(top)
            # low = max_keys[0]
            top = max(key_list)
            low = min(key_list)

        elif len(max_keys) == 1:
            top = key_list[0]
            low = key_list[0]

        top_occr = int(text_dict[top])
        low_occr = int(text_dict[low])

        st.write("top = ",int(top))
        st.write("low = ",int(low))
        avg = ((int(top) * top_occr) + (int(low) * low_occr)) / (top_occr + low_occr)
        st.write(int(top), " occured: ",int(top_occr)," times" )
        st.write(int(low), " occured: ",int(low_occr)," times" )
        st.write("Average", avg)

        if video_file != None:
            if not os.path.isfile(output_path):
                st.error("Video file not found!")
            else:
                # Display the video using Streamlit
                # print(output_path)
                # input_path = output_path
                # output_path = 'enc_op.mp4'
                # ffmpeg.input(input_path).output(output_path, vcodec='libx264', y='1').run()
                # # os.system('ffmpeg -y -i {} -vcodec libx264 {}'.format(output_path, 'enc_op.mp4'))
                op_file = open(output_path, 'rb')
                # op_bytes = op_file.read()
                # st.video(op_bytes)
                st.download_button('Download Processed File', data = op_file)

        video.release()
        output_video.release()
#         cv2.destroyAllWindows()

    
#     print(video_file)
    
    
if __name__ == '__main__':
    main()
