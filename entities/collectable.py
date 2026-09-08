"""Abstract base class and concrete implementations for collectable items."""

from abc import ABC, abstractmethod
from entities.entity import Entity


class Collectable(ABC, Entity):
    """
    Abstract base class representing an item
        that can be collected in the game.

    Attributes:
        pos (tuple[int, int]): Grid coordinates (x, y) of the item.
        points (int): Score value awarded when collected.
    """

    def __init__(self, pos: tuple[int, int], points: int) -> None:
        """
        Initializes a collectable item.

        Args:
            pos (tuple[int, int]): Grid coordinates (x, y) of the item.
            points (int): Score value awarded when collected.

        Returns:
            None
        """

        super().__init__(pos)
        self.points = points

    @abstractmethod
    def on_collected(self) -> dict[str, int | str]:
        """
        Handles interaction logic when the item is collected by the player.

        Args:
            None

        Returns:
            dict[str, int | str]: Dictionary with points and optional effect.
        """

        pass


class Pacgum(Collectable):
    """Represents a standard pacgum collectable item."""

    def on_collected(self) -> dict[str, int | str]:
        """
        Triggers collection logic for a standard pacgum.

        Returns:
            dict[str, int | str]: Dictionary containing the awarded points.
        """

        return {"points": self.points}


class SuperPacgum(Collectable):
    """Represents a super pacgum item with an associated effect."""

    def on_collected(self) -> dict[str, int | str]:
        """
        Triggers collection logic for a super pacgum.

        Returns:
            dict[str, int | str]: Dictionary containing the awarded points
                and effect type.
        """

        return {"points": self.points,
                "effect": "frighten"}
