# Vehicle Detection in Specific Areas

## Overview
This script processes images to detect vehicles within specific areas using OpenCV and NumPy. It performs image resizing, applies spatial algorithms, and integrates with a SQL Server database to store results. The processing adapts based on whether the image is taken during the day or night.

## Features
- **Vehicle Detection:** Detects vehicles within predefined areas of the image.
- **Spatial Algorithm:** Uses spatial algorithms to analyze and process images based on time of day.
- **Day/Night Processing:** Applies different algorithms for vehicle detection based on brightness to handle varying lighting conditions.
- **Database Integration:** Saves detection results to a SQL Server database. Database connection details are not shown in the script for security reasons.
- **Image Management:** Processes images from a specified directory and removes them after processing.

## Usage
1. **Prepare Your Images:** Place your images in the designated input folder.

2. **Run the Script:**
    ```bash
    python vehicle_detection.py
    ```

3. **Database Configuration:** Ensure that the database connection details are configured correctly. The connection string is hidden for security reasons.

4. **Check Results:** The script processes images to detect vehicles and saves results to the database. It will also print timestamps and file names of processed images.

## Details
- **Image Resizing:** Resizes images to a smaller size for efficient processing.
- **Vehicle Detection:** Utilizes morphological operations and other image processing techniques to detect vehicles within specified areas.
- **Day/Night Algorithm:** Determines if the image is taken during the day or night and applies appropriate vehicle detection algorithms.
- **Database Queries:** Constructs SQL queries to store detection results, though the exact queries are not shown for security reasons.
- **File Management:** Deletes processed images to maintain a clean input directory.

## Code Explanation
- **Image Resizing:** Scales images to reduce processing time.
- **Spatial Algorithm:** Applies spatial processing to focus on specific areas where vehicles are likely to be detected.
- **Day/Night Detection:** Uses brightness to determine the time of day and adjusts vehicle detection methods accordingly.
- **Database Integration:** Stores vehicle detection results in a SQL Server database. Connection details are abstracted for security.
