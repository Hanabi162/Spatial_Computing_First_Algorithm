# Spatial Algorithm for Image Processing

## Overview
This script performs spatial image processing using OpenCV and NumPy. It includes functionality for detecting and analyzing objects within images and storing results in a SQL Server database. The processing adapts based on whether the image is taken during the day or night.

## Features
- **Image Resizing:** Resizes input images to a scaled size.
- **Polygon and Rectangle Drawing:** Draws polygons and rectangles on images for visual reference.
- **Day/Night Processing:** Applies different algorithms based on the time of day, adjusting detection methods accordingly.
- **Database Integration:** Saves results to a SQL Server database. Database connection details are not shown in the script for security reasons.
- **Image Management:** Processes images from a specified directory, performs analysis, and removes processed images.

## Usage
1. **Prepare Your Images:** Place your images in the designated input folder.

2. **Run the Script:**
    ```bash
    python spatial_algorithm.py
    ```

3. **Database Configuration:** Ensure that the database connection details are configured correctly. The connection string is hidden for security reasons.

4. **Check Results:** The script processes images and saves results to the database. It will also print timestamps and file names of processed images.

## Details
- **Image Processing:** The script performs resizing, drawing of polygons and rectangles, and applies day or night-specific processing algorithms.
- **Day/Night Detection:** Uses mean brightness to determine if the image is taken during the day or night, and applies appropriate algorithms for object detection.
- **Database Queries:** Constructs SQL queries to store results, though the exact queries are not shown for security reasons.
- **File Management:** Deletes processed images to keep the input directory clean.

## Code Explanation
- **Image Resizing:** Scales images to a smaller size for processing.
- **Polygon Drawing:** Draws predefined polygons and rectangles on images.
- **Day/Night Algorithm:** Applies different processing algorithms based on image brightness to handle varying lighting conditions.
- **Database Integration:** Stores processing results in a SQL Server database. Database connection details are abstracted for security.

## Contributing
Feel free to contribute by submitting issues or pull requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or suggestions, please contact [Your Name] at [Your Email].
