import pygame
from pygame import Surface
from scipy.ndimage import gaussian_filter


class GaussianBlur:
    def __init__(self, kernel=7):
        self.kernel_size = kernel

    def filter(self, surface, x, y, width, height):
        cropped = surface.subsurface((x, y, width, height)).copy()
        pxa = pygame.surfarray.array3d(cropped)
        blurred = gaussian_filter(pxa, sigma=(self.kernel_size, self.kernel_size, 0))
        blurred_surface: Surface = pygame.Surface((width, height))
        pygame.surfarray.blit_array(blurred_surface, blurred)
        del pxa
        return blurred_surface

