import os
import gzip
import pygame
import sys

def decompress_hex_data(compressed_file):
    with open(compressed_file, 'rb') as file:
        compressed_data = file.read()

    decompressed_data = gzip.decompress(compressed_data)
    hex_string = decompressed_data.decode('utf-8').strip()

    hex_lines = []
    current_line = []

    for hex_value in hex_string.split():
        if hex_value == '<ROW_END>':
            if current_line:  # Append current line if not empty
                hex_lines.append(current_line)
                current_line = []
        else:
            current_line.append(hex_value.strip('[],'))

    if current_line:  # Append the last line if not empty
        hex_lines.append(current_line)

    return hex_lines

def main(filename=None):
    if filename is None:
        # No filename specified, ask the user for input
        filename = input('Enter the path to the .ssfif file: ').strip()

    try:
        hex_lines = decompress_hex_data(filename)
        pygame.init()

        display_width = 5000
        display_height = 5000
        screen = pygame.display.set_mode((800, 600))

        image_surface = pygame.Surface((display_width, display_height))

        y = 0
        for line in hex_lines:
            x = 0
            for hex_value in line:
                if hex_value == '<ROW_END>':
                    continue  # Skip <ROW_END> tags
                r = int(hex_value[1:3], 16)
                g = int(hex_value[3:5], 16)
                b = int(hex_value[5:7], 16)
                image_surface.set_at((x, y), (r, g, b))
                x += 1
            y += 1

        zoom_factor = 1.0
        zoom_speed = 0.1

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:  # Zoom in
                        zoom_factor += zoom_speed
                    elif event.key == pygame.K_MINUS:  # Zoom out
                        zoom_factor -= zoom_speed
                        if zoom_factor < 0.1:
                            zoom_factor = 0.1

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Calculate zoomed dimensions centered on mouse position
            zoomed_width = int(display_width * zoom_factor)
            zoomed_height = int(display_height * zoom_factor)

            # Adjust zoomed dimensions to stay centered on mouse
            zoomed_x = mouse_x - (mouse_x * zoom_factor)
            zoomed_y = mouse_y - (mouse_y * zoom_factor)

            # Fill screen with gray before drawing zoomed image
            screen.fill((128, 128, 128))

            # Scale image surface to zoomed dimensions
            zoomed_image_surface = pygame.transform.scale(image_surface, (zoomed_width, zoomed_height))

            # Draw zoomed image on screen
            screen.blit(zoomed_image_surface, (zoomed_x, zoomed_y))

            # Update display
            pygame.display.flip()

        pygame.quit()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If command line argument is provided, use it as filename
        filename = sys.argv[1]
        main(filename)
    else:
        # Otherwise, run main() without arguments to prompt for filename
        main()
