import pygame
import sys

# Define the stations and their coordinates (adjusted for Pygame)
stations = {
    'Howard': (20, 20),
    'Jarvis': (20, 50),
    'Morse': (20, 80),
    'Loyola': (20, 110),
    'Granville': (20, 140),
    'Thorndale': (20, 170),
    'Bryn Mawr': (20, 200),
    'Berwyn': (20, 230),
    'Argyle': (20, 260),
    'Lawrence': (20, 290),
    'Wilson': (20, 320),
    'Sheridan': (20, 350),
    'Addison': (20, 380),
    'Belmont': (20, 410),
    'Fullerton': (20, 440),
    'North/Clybourn': (20, 470),
    'Clark/Division': (20, 500),
    'Chicago/State': (20, 530),
    'Grand/State': (20, 560),
    'Lake/State': (20, 590),
    'Monroe/State': (20, 620),
    'Jackson/State': (20, 650),
    'Harrison': (20, 680),
    'Roosevelt': (20, 710),
    'Cermak-Chinatown': (20, 740),
    'Sox-35th': (20, 770),
    '47th': (20, 800),
    'Garfield': (20, 830),
    '63rd': (20, 860),
    '69th': (20, 890),
    '79th': (20, 920),
    '87th': (20, 950),
    '95th/Dan Ryan': (20, 980),
}

# Padding between dots and station names
padding = 10

# Create a function to draw the map
def draw_map(surface):
    # Drawing the stations
    for station, (x, y) in stations.items():
        pygame.draw.circle(surface, (255, 0, 0), (int(x), int(y)), 3)
        font = pygame.font.Font(None, 15)
        text_surface = font.render(station, True, (0, 0, 0))
        surface.blit(text_surface, (x + padding, y))

    # Drawing the line
    pygame.draw.lines(surface, (0, 0, 0), False, list(stations.values()), 1)

# Initialize Pygame
pygame.init()

# Set up the Pygame window
width, height = 200, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chicago Red Line CTA Train Map')

map_open = False

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                map_open = not map_open

    # Fill the background
    screen.fill((255, 255, 255))

    # Draw the map if it's open
    if map_open:
        draw_map(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
