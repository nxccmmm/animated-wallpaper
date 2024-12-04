import pygame
import sys
from button import Button
import tkinter
from tkinter import filedialog
import glob
import os

pygame.init()
pygame.font.init()

screen_height = 500
screen_width = 800
base_text_color = (223, 67, 111)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

def album_player(filepath):
    print("Album Player started")
    previous_time = pygame.time.get_ticks()
    cooldown = 3000
    screen.fill((245, 198, 215))

    rewind_button_surface = pygame.transform.scale(pygame.image.load("C:/Users/nikki/OneDrive/Desktop/Programming 2024/final/src/rewind_button.png"),(550,550))
    pause_button_surface = pygame.transform.scale(pygame.image.load("C:/Users/nikki/OneDrive/Desktop/Programming 2024/final/src/pause_button.png"),(550,550))
    play_button_surface = pygame.transform.scale(pygame.image.load("C:/Users/nikki/OneDrive/Desktop/Programming 2024/final/src/play_button.png"),(550,550))
    load_new_album_surface = pygame.transform.scale(pygame.image.load("C:/Users/nikki/OneDrive/Desktop/Programming 2024/final/src/load_new_album.png"),(550,550))

    rewind_button = Button(
        image=rewind_button_surface, pos=(screen_width * 0.1, screen_height-60), text_input="",
        font=bold_font(80), base_color=base_text_color)

    pause_button = Button(
        image=pause_button_surface, pos=(screen_width * 0.25, screen_height-60), text_input="",
        font=bold_font(50), base_color=base_text_color)

    play_button = Button(
        image=play_button_surface, pos=(screen_width * 0.40, screen_height-60), text_input="",
        font=bold_font(50), base_color=base_text_color)

    load_new_album_button = Button(
        image=load_new_album_surface, pos=(screen_width * 0.9, screen_height-60), text_input="",
        font=bold_font(50), base_color=base_text_color)

    image_file_paths = []
    image_names = []
    current_image_index = 0
    paused = False
    seek_button_pressed = False
    rewind_button_pressed = False

    try:
        os.chdir(filepath)
    except FileNotFoundError:
        return

    for file in glob.glob("*"):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            current_image_path = f"{filepath}/{file}"
            image_file_paths.append(current_image_path)
            image_names.append(file)

    if not image_file_paths:
        return

    album_selection_opened= False
    running = True
    while running:
        current_mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if rewind_button.is_clicked():
            if current_image_index > 0:
                current_image_index -= 1

        if load_new_album_button.checkForInput(current_mouse_pos) and not album_selection_opened:
            album_selection_opened= True
            filedialogwindow = tkinter.Tk()
            filedialogwindow.withdraw()
            filepath = filedialog.askdirectory(title="Choose your Photo Album")
            filedialogwindow.destroy()
            if filepath:
                album_player(filepath)
                return
            
        if paused:
            if play_button.is_clicked():
                paused = False
        else:
            if pause_button.is_clicked():
                paused = True

        current_time = pygame.time.get_ticks()
        if not paused and current_time - previous_time >= cooldown and not seek_button_pressed and not rewind_button_pressed:
            if current_image_index + 1 < len(image_file_paths):
                current_image_index += 1
            previous_time = current_time

        screen.fill((245, 198, 215))
        rewind_button.draw(screen)
        pause_button.draw(screen) if not paused else play_button.draw(screen)
        load_new_album_button.draw(screen)

        if 0 <= current_image_index < len(image_file_paths):
            try:
                new_image_surface = pygame.image.load(image_file_paths[current_image_index])

                if new_image_surface.get_width() > 800 or new_image_surface.get_height() > 500:
                    new_image_surface = pygame.transform.scale(new_image_surface, (400, 250))

                new_image_rect = new_image_surface.get_rect(center=(screen_width / 2, screen_height / 2))
                screen.blit(new_image_surface, new_image_rect)

                photo_title_text_surface = bold_font(40).render(image_names[current_image_index], True, base_text_color)
                photo_title_text_rect = photo_title_text_surface.get_rect(center=(screen_width / 2, 150-50))
                screen.blit(photo_title_text_surface, photo_title_text_rect)

                image_count_text_surface = bold_font(20).render(f"{current_image_index + 1}/{len(image_names)}", True, base_text_color)
                image_count_text_rect = image_count_text_surface.get_rect(center=(screen_width / 2, 450))
                screen.blit(image_count_text_surface, image_count_text_rect)

                pygame.display.update()

            except pygame.error as e:
                print(f"Error loading image: {e}")
                continue


        pygame.display.update()
        seek_button_pressed= False
        rewind_button_pressed= False


def bold_font(size):
    return pygame.font.Font("C:/Users/nikki/OneDrive/Desktop/Programming 2024/final/src/UpheavalPro.ttf", size)


def main():
    play_img= pygame.image.load("C:/Users/nikki/OneDrive/Desktop/Programming 2024/final/src/start_button.png")
    quit_img= pygame.image.load("C:/Users/nikki/OneDrive/Desktop/Programming 2024/final/src/quit_button.png")  
    start_button = Button(
        image= play_img, pos = (200, 300), text_input="",
        font= bold_font(80), base_color= base_text_color, scale=0.25)

    quit_button = Button(
        image= quit_img, pos= (600,300), text_input= "",
        font= bold_font(100), base_color= base_text_color, scale=0.25)
    running = True
    while running:
        screen.fill((245, 198, 215))
        start_button.draw(screen)
        quit_button.draw(screen)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if start_button.is_clicked():
                    print("start")
                    filedialogwindow = tkinter.Tk()
                    filedialogwindow.withdraw()
                    filepath = filedialog.askdirectory(title="Choose Your Photo Album")
                    print(filepath)
                    filedialogwindow.destroy()
                    if filepath:
                        album_player(filepath)

                if quit_button.is_clicked():
                    print("quit")
                    running = False

        title_surface = bold_font(80).render("Photo Gallery", True, base_text_color)
        title_surface_rect = title_surface.get_rect(center=(screen_width / 2, 175))
        screen.blit(title_surface, title_surface_rect)
        pygame.display.update()

if __name__ == "__main__":
    main()
pygame.quit()