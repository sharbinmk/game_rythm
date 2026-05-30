import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chart Recorder")

FONT = pygame.font.Font("assets/印品鸿蒙体.ttf", 24)
BIG_FONT = pygame.font.Font("assets/印品鸿蒙体.ttf", 72)

# File paths - To create your own chart, paste the path here.
SONG_PATH = "charts/Fraq/track.mp3"
OUTPUT_FILE = "charts/output.txt"

# Key mapping
TOP_KEYS = (pygame.K_a, pygame.K_s, pygame.K_d)
BOTTOM_KEYS = (pygame.K_j, pygame.K_k, pygame.K_l)
DUAL_KEY = pygame.K_SPACE


def draw_center_text(text):
    # Turn text into img pluh
    img = BIG_FONT.render(text, True, (255, 255, 255))

    # centre, can't you see width//2 and height//2 lol??
    rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(img, rect)


def countdown(clock):
    countdown_nums = ["3", "2", "1"]

    for num in countdown_nums:
        # Save current time so can accurate countdown
        start = pygame.time.get_ticks()

        # Is... 1 second, what is there you don't understand?
        while pygame.time.get_ticks() - start < 1000:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            screen.fill((0, 0, 0))
            draw_center_text(num)
            pygame.display.flip()

    return True


def main():
    clock = pygame.time.Clock()

    notes = []
    started = False
    running = True

    # Start screen
    while running and not started:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Start recording
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    started = True

        screen.fill((0, 0, 0))

        txt = FONT.render("Press ENTER to Start Recording",True,(255, 255, 255))

        screen.blit(txt, (180, 170))
        pygame.display.flip()

    # 3 2 1 countdown
    if not countdown(clock):
        return

    # Start music + timer together
    pygame.mixer.music.load(SONG_PATH)
    pygame.mixer.music.play()

    start_time = pygame.time.get_ticks()

    while running:
        clock.tick(60)
        # Start the time
        current_time = pygame.time.get_ticks() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # If a key press, check what key
            if event.type == pygame.KEYDOWN:
                
                # Stop recording
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Top
                elif event.key in TOP_KEYS:
                    notes.append((current_time, "top"))
                    print(f"{current_time},top")

                # Bot
                elif event.key in BOTTOM_KEYS:
                    notes.append((current_time, "bottom"))
                    print(f"{current_time},bottom")

                # Dual
                elif event.key == DUAL_KEY:
                    notes.append((current_time, "dual"))
                    print(f"{current_time},dual")

        # just UI dude, nothing fancy
        screen.fill((0, 0, 0))

        text = FONT.render(
            "Recording... ESC to stop",True,(255, 255, 255))

        screen.blit(text, (20, 20))

        time_text = FONT.render(f"Time: {current_time}",True,(0, 255, 0))

        screen.blit(time_text, (20, 60))
        pygame.display.flip()

    # Stop song and save fil
    pygame.mixer.music.stop()
    save_chart(notes)
    pygame.quit()

# Save notes and file
def save_chart(notes):
    os.makedirs("charts", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        for t, lane in notes:
            f.write(f"{t},{lane}\n")

    print("\nChart saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()