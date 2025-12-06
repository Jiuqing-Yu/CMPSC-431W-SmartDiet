import pygame
import sys
from Default import *
from page import *
from connection import *
running = True
clock = pygame.time.Clock()
db_connection = None
try:
    init_tables()
    db_connection = get_connection()
    current_page = HomePage(screen,db_connection)
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                new_page = current_page.handle_event(event)
                if new_page:
                    current_page = new_page
        current_page.draw()
        pygame.display.flip()
        clock.tick(60)
except Exception as e:
    print(f"💥 Unexpected error: {e}", file=sys.stderr)
finally:
    if db_connection and db_connection.open:
        db_connection.close()
        print("🔒 Database connection closed safely.")
    pygame.quit()
    sys.exit()