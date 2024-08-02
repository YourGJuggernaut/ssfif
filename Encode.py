import os
from PIL import Image
import gzip
import sys

def compress_hex_data(hex_data, output_filename):
    hex_string = '\n'.join(hex_data)  # Join hex data with newline for each row
    bytes_data = hex_string.encode('utf-8')
    compressed_data = gzip.compress(bytes_data)
    with open(output_filename, 'wb') as file:
        file.write(compressed_data)
    return output_filename

def process_image(input_filename):
    try:
        with Image.open(input_filename) as img:
            rgb_img = img.convert('RGB')  # Convert image to RGB format
            width, height = rgb_img.size
            rgb_data = list(rgb_img.getdata())  # Convert to list for easier manipulation

            hex_data = []
            for i, (r, g, b) in enumerate(rgb_data):
                hex_value = f"#{r:02x}{g:02x}{b:02x}"
                hex_data.append(hex_value)
                if (i + 1) % width == 0:  # End of a row
                    hex_data.append('<ROW_END>')  # Add <ROW_END> tag at the end of each row
                else:
                    continue

            imga = os.path.splitext(input_filename)[0] + '.ssfif'

            with open(imga, 'w') as file:
                file.write('\n'.join(hex_data))

            compressed_file = compress_hex_data(hex_data, imga)

            # Move the processed file to the Output folder
            folder = 'Output'
            os.makedirs(folder, exist_ok=True)
            destination_file = os.path.join(folder, os.path.basename(compressed_file))
            os.replace(compressed_file, destination_file)
            
            print(f'Image {input_filename} processed and saved as {destination_file}.')
    except FileNotFoundError:
        print(f'The image file {input_filename} was not found.')
    except Exception as e:
        print(f'An error occurred while processing the image: {e}')

def main():
    if len(sys.argv) > 1:
        # If command line argument is provided, use it as filename
        filename = sys.argv[1]
        process_image(filename)
    else:
        # Otherwise, ask the user for the path to the image file
        filename = input('Enter the path to the image file (include extension): ').strip()
        process_image(filename)

if __name__ == "__main__":
    main()
