import pygame
import sys
import random
import time
import serial
import serial.tools.list_ports
import threading

print("Connecting to Arduino Serial...")


ports = list(serial.tools.list_ports.comports())

print("List of Ports")
for p in ports:
    print(p)

# Assume the first port is the Arduino (you might need a selection mechanism here)
if ports:
    ser = serial.Serial(ports[0].device, 9600, timeout=1)
else:
    print("No Arduino found")
    ser = None

# Thread for reading serial data
def read_serial():
    while ser and ser.is_open:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').rstrip()
            print("read_serial : ",line)
            return line

if ser:
    threading.Thread(target=read_serial, daemon=True).start()


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def send_thrust_to_arduino(A):

    if ser:
        ser.write(f"{A}\n".encode())

pygame.init()

# Set up display
screen_width, screen_height = 1080, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Real-Time Propeller Test")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up font
font_size = 20
font = pygame.font.Font(None, font_size)

# Set up graph parameters
graph_rect = pygame.Rect(50, 100, screen_width - 100, screen_height - 150)
x_values = []
y_values = []
max_data_points = graph_rect.width
x_scale = 200 # For example, every 500 RPM
y_scale = 20   # For example, every 10 grams
max_x_axis_value = 1400  # Adjust this as needed for the expected RPM range
max_y_axis_value = 130

# Node and text parameters
node_radius = 5
blink_interval = 500
show_node = True
last_blink_time = 0

# Test mode
current_test_mode = None
test_modes = {'1': 'Propeller A', '2': 'Propeller B', '3': 'Propeller C'}

# Flags to control testing state
testing = False
test_finished = False
test_data_points = 12
current_data_point = 0
last_data_time = None
max_thrust_value = 0

zerot = 0

def draw_axis_scales():
    # Draw X-axis scales
    for x in range(0, max_x_axis_value, x_scale):
        scaled_x = (x / max_x_axis_value) * graph_rect.width
        pygame.draw.line(screen, WHITE, (graph_rect.left + scaled_x, graph_rect.bottom), 
                         (graph_rect.left + scaled_x, graph_rect.bottom + 5))
        scale_text = font.render(str(x), True, WHITE)
        screen.blit(scale_text, (graph_rect.left + scaled_x - scale_text.get_width() // 2, graph_rect.bottom + 10))

    # Draw Y-axis scales
    for y in range(0, max_y_axis_value, y_scale):
        scaled_y = (y / max_y_axis_value) * graph_rect.height
        pygame.draw.line(screen, WHITE, (graph_rect.left, graph_rect.bottom - scaled_y), 
                         (graph_rect.left - 5, graph_rect.bottom - scaled_y))
        scale_text = font.render(str(y), True, WHITE)
        screen.blit(scale_text, (graph_rect.left - scale_text.get_width() - 10, graph_rect.bottom - scaled_y - scale_text.get_height() // 2))


# Function to update the graph
def update_graph():
    global last_blink_time, show_node

    if x_values and y_values:
        # Scale data points to fit the graph
        scaled_x_values = [(x / max_x_axis_value) * graph_rect.width for x in x_values]
        scaled_y_values = [(y / max_y_axis_value) * graph_rect.height for y in y_values]

        # Draw lines between points
        for i in range(1, len(x_values)):
            pygame.draw.line(screen, WHITE,
                             (graph_rect.left + scaled_x_values[i - 1], graph_rect.bottom - scaled_y_values[i - 1]),
                             (graph_rect.left + scaled_x_values[i], graph_rect.bottom - scaled_y_values[i]), 2)

        # Update the blinking node
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > blink_interval:
            last_blink_time = current_time
            show_node = not show_node

        if show_node and testing:
            print("SHOW NODE")
            node_x = graph_rect.left + scaled_x_values[-1]
            node_y = graph_rect.bottom - scaled_y_values[-1]
            pygame.draw.circle(screen, RED, (node_x, node_y), node_radius)

            # Display the current data value
            data_text = font.render(f"RPM: {x_values[-1]}  Thrust: {y_values[-1]}", True, WHITE)
            screen.blit(data_text, (node_x + 10, node_y - font_size))
# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and not testing:
            key = event.unicode
            if key in test_modes:
                current_test_mode = test_modes[key]
                x_values.clear()
                y_values.clear()
                testing = True
                current_data_point = 0
                last_data_time = time.time()
                max_thrust_value = 0
                zerot = 0

    # Clear the screen
    screen.fill(BLACK)

    # Draw the graph
    pygame.draw.rect(screen, WHITE, graph_rect, 2)

    # Draw the axis scales
    draw_axis_scales()
    
    # Graph title and axes labels
    title_text = font.render(f"Graph for {current_test_mode}", True, WHITE)
    screen.blit(title_text, (graph_rect.centerx- title_text.get_width() // 2, 60))
    x_axis_label = font.render("RPM", True, WHITE)
    screen.blit(x_axis_label, (graph_rect.right - x_axis_label.get_width(), graph_rect.bottom + 10))
    y_axis_label = font.render("Thrust (g)", True, WHITE)
    screen.blit(y_axis_label, (10, graph_rect.top))

    update_graph()
    
    if testing:
        
        if current_data_point ==0 and zerot == 0: 
            data = read_serial().split(' ')
            if len(data) != 2:
                continue
            #make it into rpm.
            zerot = int(float(data[1]))
            print("fuck")
            
        if time.time() - last_data_time >= 1 and current_data_point < test_data_points:
            #read data from arduino
            #power rpm thrust:power rpm thrust:power rpm thrust (A, B, C)
            data = read_serial().split(' ')

            if len(data) != 2:
                continue
            #make it into rpm.
            new_rpm = int(data[0])
            new_thrust = -int(float(data[1])-zerot)

            #new_rpm = random.randint(1000, 5000)
            #new_thrust = random.randint(50, 150)


            x_values.append(new_rpm)
            y_values.append(new_thrust)

            # Update maximum thrust value
            max_thrust_value = max(max_thrust_value, new_thrust)

            last_data_time = time.time()  # Update the time of the last data point
            current_data_point += 1

            #send data to arduino

            #arduino power : current_data_point*10 가 thrust
            #powerA powerB powerC로 전송

            send_thrust_to_arduino(1*current_data_point+60)

            print(1*current_data_point+60)

    # Check if test is finished
    if current_data_point == test_data_points:
        testing = False
        test_finished = True
        send_thrust_to_arduino(0)
        #turn off arduino
        #arduino power : 0


    if test_finished:
        send_thrust_to_arduino(0)
        # Calculate the maximum lift coefficient after the test is finished
        max_lift_coefficient = 0
        for rpm, thrust in zip(x_values, y_values):
            if rpm != 0:  # To avoid division by zero
                lift_coefficient = thrust / (rpm ** 2)
                max_lift_coefficient = max(max_lift_coefficient, lift_coefficient)

        # Display the maximum thrust value
        max_thrust_text = font.render(f"Maximum Thrust: {max_thrust_value} g, Max Lift Coefficient: {max_lift_coefficient:e}", True, WHITE)
        screen.blit(max_thrust_text, (graph_rect.centerx - max_thrust_text.get_width() // 2, graph_rect.bottom + 30))
    pygame.display.flip()

 
