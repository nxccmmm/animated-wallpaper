
import pygame

class Button:
    def __init__(self, image=None, pos=None, text_input="", font=None, base_color=(0, 0, 0), scale=0.25):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.text_input = text_input

        # Render text
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        # Load image and scale it
        if image is not None:
            width, height = image.get_width(), image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        else:
            # If no image is provided, use the text surface as the button background
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.clicked = False

    def checkForInput(self, position):
        """Check if the mouse click is within the button rect."""
        return self.rect.collidepoint(position)

    def draw(self, surface):
        """Draw the button image and text on the surface."""
        surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                return True
        return False