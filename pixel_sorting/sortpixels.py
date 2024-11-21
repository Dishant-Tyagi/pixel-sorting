from PIL import Image, ImageDraw
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Define the sortPixels function
def sortPixels(img_in, direction, order, delta):
    # Get width and height of the source Image
    axis_X, axis_Y = img_in.size
    # Delta variables
    delta = int(delta)
    control_X = axis_X / delta
    control_Y = axis_Y / delta
    # Create the output Image
    img_out = Image.new('RGB', (axis_X, axis_Y))
    draw_img_out = ImageDraw.Draw(img_out)
    # Controls the direction where the algorithm is going to sort
    if direction == 'v':
        axis = axis_X
        control = control_Y
    elif direction == 'h':
        axis = axis_Y
        control = control_X
    else:
        print('No valid direction given')
        return False

    for i in range(delta):
        row = []
        for x in range(axis):
            # Get the pixel rows from the source Image
            for y in range(int(i * control), int((i + 1) * control)):
                if direction == 'v':
                    pixel = img_in.getpixel((x, y))
                elif direction == 'h':
                    pixel = img_in.getpixel((y, x))
                row.append(pixel)
            # Sort the array
            row.sort(reverse=order)
            # Put the sorted pixels on the output Image
            for y in range(int(i * control), int((i + 1) * control)):
                if direction == 'v':
                    draw_img_out.point((x, y), row.pop())
                elif direction == 'h':
                    draw_img_out.point((y, x), row.pop())
    return img_out

# Function to count unique colors in the image
def count_unique_colors(img):
    """
    Count the number of unique colors in the image.
    Returns the number of unique colors.
    """
    # Convert the image to RGB mode in case it's not
    img = img.convert('RGB')
    # Get all the colors used in the image
    colors = img.getcolors(img.size[0] * img.size[1])  # Maximum number of colors
    # Count unique colors
    unique_colors = len(colors)
    return unique_colors

# Main function for sorting and saving the image
def main():
    # Hardcoded input image path
    input_image_path = r"D:\exi\live\img.png"  # Path to the input image
    output_image_path = "sorted_output_image.png"  # Path for the output image

    # Load the input image
    img_in = Image.open(input_image_path)

    # Set the sorting parameters
    orientation = '-v'  # Example: sort vertically
    order = True  # Descending order (-d) is True, Ascending order (-a) is False
    delta = 10  # Number of sections to divide the image for sorting

    # Sort the image based on the parameters
    if orientation == '-h':
        sorted_img = sortPixels(img_in, 'h', order, delta)
    elif orientation == '-v':
        sorted_img = sortPixels(img_in, 'v', order, delta)
    elif orientation == '-hv':
        sorted_img = sortPixels(sortPixels(img_in, 'h', order, delta), 'v', order, delta)
    elif orientation == '-vh':
        sorted_img = sortPixels(sortPixels(img_in, 'v', order, delta), 'h', order, delta)
    else:
        print("Invalid input")
        return

    # Save the output image
    sorted_img.save(output_image_path)
    print(f"Image sorted and saved as {output_image_path}")

    # Get color details of the output image
    unique_colors = count_unique_colors(sorted_img)
    print(f"Number of unique colors: {unique_colors}")

# Run the script
if __name__ == "__main__":
    main()
