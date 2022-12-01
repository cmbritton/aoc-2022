import time


class Timer:
    """
    Track the elapsed time to solve various parts of the puzzle.
    """

    def __init__(self) -> None:
        """
        Create a new Timer and start it.
        """
        self.start_time = time.perf_counter()
        self.end_time = None

    def stop(self) -> None:
        """
        Stop the Timer.
        """
        self.end_time = time.perf_counter()

    def elapsed_time(self) -> str:
        """
        Format a string that represents the elapsed time.

        Scale the elapsed time value to seconds, milliseconds, microseconds,
        or nanoseconds based on the magnitude of the value.

        Returns:
            The string representation of the elapsed time for this Timer.
        """
        if self.end_time is None:
            self.stop()
        t = self.end_time - self.start_time
        unit = 'seconds'
        if t < 1:
            t = t * 1000
            unit = 'milliseconds'
        if t < 1:
            t = t * 1000
            unit = 'microseconds'
        if t < 1:
            t = t * 1000
            unit = 'nanoseconds'

        return f'{t:.2f} {unit}'
