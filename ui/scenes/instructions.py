import pygame
from consts import COMMOM_TEXT_COLOR


class Instructions:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.title_font = pygame.font.SysFont(
            None,
            int(screen.get_height() * 0.08)
            )
        self.instructions_font = pygame.font.SysFont(
                    None,
                    int(screen.get_height() * 0.03)
                    )

    def render_instructions(self) -> None:
        self._render_title()
        self._render_instructions()
        pygame.display.update()

    def _render_title(self) -> None:
        title = self.title_font.render(
                "INSTRUCTIONS", 0, COMMOM_TEXT_COLOR
                )
        x, y = self.screen.get_size()
        self.screen.blit(title, title.get_rect(center=(x // 2, y // 6)))

    def _render_instructions(self) -> None:
        instructions_array = [
            "W / Arraw Up     --     Move Up",
            "W / Arraw Left     --     Move Left",
            "W / Arraw Down     --     Move Down",
            "W / Arraw Right     --     Move Right"
        ]
        x, y = self.screen.get_size()
        for i, instruction_txt in enumerate(instructions_array, 1):
            instruction = self.instructions_font.render(
                instruction_txt,
                0,
                COMMOM_TEXT_COLOR
            )
            line_heigth = self.instructions_font.get_linesize() + 10
            self.screen.blit(
                instruction,
                instruction.get_rect(
                    center=(x // 2, (y // 3) + (line_heigth * i))
                    )
            )
