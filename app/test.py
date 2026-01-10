from PIL import Image, ImageDraw, ImageFont

def get_max_font_size(text, font_path, max_width, max_height, max_size=200):
    """
    Finds the maximum font size that fits within the specified width and height.

    Args:
        text (str): The text to fit.
        font_path (str): Path to the TrueType font file (e.g., 'arial.ttf').
        max_width (int): The maximum allowed width in pixels.
        max_height (int): The maximum allowed height in pixels.
        max_size (int): The upper limit for the font size search.

    Returns:
        ImageFont: A Pillow ImageFont object with the optimal size.
    """
    # Use binary search to find the largest font size that fits
    low, high = 1, max_size
    best_font = None

    while low <= high:
        mid = (low + high) // 2
        try:
            # Load font with the current size
            font = ImageFont.truetype(font_path, mid)
            # Measure the text size
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            if text_width <= max_width and text_height <= max_height:
                # Text fits, try a larger size
                best_font = font
                low = mid + 1
            else:
                # Text is too big, try a smaller size
                high = mid - 1
        except IOError:
            print(f"Error loading font at size {mid}. Check font path.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # If no font was found (e.g., text too big even at size 1), return the smallest
    if best_font is None:
      return ImageFont.truetype(font_path, 1)

    return best_font

# --- Example Usage ---

# Define constraints
TARGET_WIDTH = 1536
TARGET_HEIGHT = 100
TEXT_TO_DRAW = "Hello, World!"
FONT_FILE = "arial.ttf" # Make sure this file exists in your directory

# 1. Create a blank image to draw on
image = Image.new('RGB', (TARGET_WIDTH + 20, TARGET_HEIGHT + 20), color='white')
draw = ImageDraw.Draw(image)

# 2. Find the optimal font size
# We pass the target width/height as constraints
optimal_font = get_max_font_size(
    text=TEXT_TO_DRAW,
    font_path=FONT_FILE,
    max_width=TARGET_WIDTH,
    max_height=TARGET_HEIGHT
)

# 3. Draw the text with the optimal font
# The position (x, y) can be adjusted for centering/alignment
draw.text((10, 10), TEXT_TO_DRAW, font=optimal_font, fill='black')

# (Optional) Draw a rectangle around the target area for visualization
draw.rectangle([(10, 10), (10 + TARGET_WIDTH, 10 + TARGET_HEIGHT)], outline='red')

# 4. Save the image
image.save("biggest_text.png")
print(f"Image 'biggest_text.png' created with text size: {optimal_font.size}pt")