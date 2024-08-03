import cv2
import numpy as np
import os
import time
import datetime
import pyodbc
from pathlib import Path
# I don't want to show the database connection details in this script on GitHub

v_input_path = r"C:\Dataset"
v_sleeptime = 10  # sleep x sec 

def Spatial_Algorithm(image) :
    
    # resize image
    scale_percent = 50 
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    
    # draw polylines
    def draw_Polylines(image, points, color, thickness):
        cv2.polylines(image, [points.reshape((-1, 1, 2))], True, color, thickness)
    
    def draw_RecTangle(image, start_point, end_point, color, thickness):
        cv2.rectangle(image, start_point, end_point, color, thickness)
    
    # define focus point
    vertices = np.array([[470, 640], [450, 600], [1200, 375], [1800, 380], [2025, 410], [2060, 630]], dtype=np.int32) * scale_percent // 100
        
    # draw vertices
    Light_vertices_view1 = (int(1000 * scale_percent // 100), int(350 * scale_percent // 100)), (int(1100 * scale_percent // 100), int(650 * scale_percent // 100))
    Light_vertices_view2 = (int(1250 * scale_percent // 100), int(350 * scale_percent // 100)), (int(1500 * scale_percent // 100), int(650 * scale_percent // 100))
    Light_vertices_view3 = (int(1850 * scale_percent // 100), int(350 * scale_percent // 100)), (int(1950 * scale_percent // 100), int(650 * scale_percent // 100))
    
    # call func
    draw_Polylines(resized_image, vertices, (255, 0, 0), 3)
    
    # create mask
    mask = np.zeros_like(resized_image[:, :, 0])
    cv2.fillPoly(mask, [vertices], 255)
    
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        
    # check day / night
    mean_brightness = np.mean(gray_image[gray_image])
    #print(f"Mean brightness: {mean_brightness:.2f}")
    epsilon = 0.01
    
    if mean_brightness >= 119.93 and not (123.45 - epsilon < mean_brightness < 123.45 + epsilon):
        print("Day time algorithm")
        
        masked_image = cv2.bitwise_and(resized_image, resized_image, mask=mask)
            
        gray_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
        _, thresholded_image = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY)
    
        kernel = np.ones((3, 3), np.uint8)
        morphed_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_CLOSE, kernel)
        morphed_image = cv2.morphologyEx(morphed_image, cv2.MORPH_OPEN, kernel)
            
        # detect containers
        containers = []
        contours, _ = cv2.findContours(morphed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area <= 1000:  
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int64(box)
                cv2.drawContours(resized_image, [box], 0, (0, 0, 255), 2)
                containers.append(box)
        container_area = sum([cv2.contourArea(contour) for contour in containers])
    
        # count pixel 255 (free space) in polyline
        empty_pixel_count = cv2.countNonZero(morphed_image & mask) - container_area
        
        # cal area 
        total_pixel_count = cv2.countNonZero(mask)
        day_empty_percentage = (empty_pixel_count / total_pixel_count) * 100
        day_used_area = 100 - day_empty_percentage
        day_triyangyas = (day_used_area*110)/100
    
        #print(f"Area in used: {day_used_area:.0f}% (Used)")
        #print(f"Truck : {day_triyangyas:.0f}")
        #print(f"Free : {day_empty_percentage:.0f}% (Empty)")

        return {
                'time': 'day',
                'day_triyangyas': day_triyangyas
                }
    
    else:
        print("Night time algorithm")
        draw_RecTangle(resized_image, Light_vertices_view1[0], Light_vertices_view1[1], (0, 255, 0), 3)
        draw_RecTangle(resized_image, Light_vertices_view2[0], Light_vertices_view2[1], (0, 255, 0), 3)
        draw_RecTangle(resized_image, Light_vertices_view3[0], Light_vertices_view3[1], (0, 255, 0), 3)
        
        masked_image = cv2.bitwise_and(resized_image, resized_image, mask=mask)
            
        gray_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
            
        adaptive_thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 10)
            
        # remove noise
        kernel = np.ones((25, 25), np.uint8)
        morphed_image = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)
        morphed_image = cv2.morphologyEx(morphed_image, cv2.MORPH_OPEN, kernel)
    
        # check light
        for vertices in [Light_vertices_view1, Light_vertices_view2, Light_vertices_view3]:
            x1, y1 = vertices[0]
            x2, y2 = vertices[1]
            region = gray_image[y1:y2, x1:x2]
            
            if np.mean(region) > 128.5:
                morphed_image[y1:y2, x1:x2] = 0  # covert to black
        
        # count pixel 255 (free space) in polyline
        used_pixel_count = cv2.countNonZero(morphed_image & mask)
            
        total_pixel_count = cv2.countNonZero(mask)
        night_used_area  = (used_pixel_count / total_pixel_count) * 100
        night_empty_percentage = 100 - night_used_area
        night_triyangyas = (night_used_area*110)/100
            
        #print(f"Area in used: {day_used_area:.0f}% (Used)")
        #print(f"Truck : {day_triyangyas:.0f}")
        #print(f"Free : {day_empty_percentage:.0f}% (Empty)")

        return {
                'time': 'night',
                'night_triyangyas': night_triyangyas
                }

def read_images(v_input_path):
    while True:
        if os.path.exists(v_input_path):
            files = os.listdir(v_input_path)

            # waiting ftp
            time.sleep(2)

            if files:
                for file in files:
                    try:
                        source = Path(v_input_path)
                        cctv_id = os.path.basename(file)[:11]
                                
                        cnxn = pyodbc.connect(# Do Not Show Connection Details)
                        cursor = cnxn.cursor()
                        
                        image_path = os.path.join(v_input_path, file)
                        image = cv2.imread(image_path)

                        result = Spatial_Algorithm(image)

                        if result['time'] == 'day': 
                            triyangyas = int(result['day_triyangyas']) # truck 
                                    
                        else: 
                            triyangyas = int(result['night_triyangyas']) # truck 
                                
                        otra_sqlstr_1 = "String concatenation not shown"
                        otra_sqlstr_2 = "String concatenation not shown"
                        otra_sqlstr_3 = "String concatenation not shown"


                        otran_sqlstr = otran_sqlstr_1+otran_sqlstr_2 + otran_sqlstr_3
                        #print(otran_sqlstr)
                        cursor.execute(otran_sqlstr)
                        time.sleep(2)    
                        cnxn.commit() 
                        os.remove(image_path)
                        v_now = datetime.datetime.now()
                        v_date_time = v_now.strftime("%d/%m/%Y %H:%M:%S")
                        print(v_date_time,',Read:',file)

                        cursor.close()
                        cnxn.close()

                        
                    except Exception as e:
                        print(f"Read image error: {e}")

            else:
                print(f"The folder is empty.")
                time.sleep(v_sleeptime)
        else:
            print("This folder doesn't actually exist.")
            break

if __name__ == "__main__":
    read_images(v_input_path)
