import pygame


def handle_name_input(max_len: int, name: str,
                      event: pygame.event.Event) -> str:
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            return name[:-1] if name else ''
        letter: str = event.unicode
        if letter.isalnum() or letter == " ":
            return name + letter if len(name) < max_len else name
        elif event.key == pygame.K_RETURN:
            return name
    return name
