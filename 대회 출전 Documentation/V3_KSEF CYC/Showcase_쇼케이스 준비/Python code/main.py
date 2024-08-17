import pygame
import serial
import serial.tools.list_ports
import threading
import time
import sys
# Initialize Pygame
pygame.init()
# Constants
# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
BG_COLOR = (50, 50, 50)
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 100, 100)

pygame.display.set_caption("Arduino Serial Interface")
font = pygame.font.Font(None, 36)

# List available serial ports
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

# Assume the first port is the Arduino (you might need a selection mechanism here)
if ports:
    ser = serial.Serial(ports[0].device, 115200, timeout=1)
else:
    print("No Arduino found")
    ser = None

# Thread for reading serial data
def read_serial():
    while ser and ser.is_open:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').rstrip()
            return line

if ser:
    threading.Thread(target=read_serial, daemon=True).start()

def send_thrust_to_arduino(power):

    print(power)
    min_ = 60
    max_ = 90

    mapped = (max_ - min_) * (int(power) / 100) + min_

    if ser:
        ser.write(f"{mapped}\n".encode())

# Thrust value
power = 0

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up font
font_size_small = 24
font_size_medium = 36
font_size_large = 48
font = pygame.font.Font(None, font_size_large)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if (power < 100) : 
                    power+= 10
                    # Send the new thrust value to Arduino
                    send_thrust_to_arduino(power)
            elif event.key == pygame.K_DOWN:
                if (power >0):
                    power -= 10
                    # Send the new thrust value to Arduino
                    send_thrust_to_arduino(power)

    data = read_serial().split('_')

    try : 
        rpm = data[1].split(' ')[1]
    except : 
        rpm = -1
    
    try : 
        thrust = data[3].split(' ')[1]
    except : 
        thrust = -1

    # Draw the interface
    screen.fill(BG_COLOR)

    # Display the current thrust value
    # Render text with different sizes and colors
    power_text = font.render(f"Power: {power}", True, RED)
    rpm_text = font.render(f"RPM: {rpm}", True, GREEN)
    thrust_text = font.render(f"Thrust (g): {thrust}", True, BLUE)

    # Calculate box heights
    box_height = screen_height // 3

    # Blit texts to the screen
    screen.blit(power_text, (50, 0))
    screen.blit(rpm_text, (50, box_height))
    screen.blit(thrust_text, (50, 2 * box_height))

    pygame.display.flip()


# Close the serial connection on exit
if ser:
    ser.close()

# Quit Pygame
pygame.quit()
