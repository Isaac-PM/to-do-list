# -*- coding: utf-8 -*-

class Task():
    """This class represents a task in the to-do list.
    """

    def __init__(self, description: str = "", striken: bool = False, is_done: bool = False) -> None:
        """This method initializes the task object.

        Args:
            description (str, optional): Defaults to "".
            striken (bool, optional): Defaults to False.
            is_done (bool, optional): Defaults to False.
        """
        self.description: str = description
        self.stricken: bool = striken
        self.is_done: bool = is_done