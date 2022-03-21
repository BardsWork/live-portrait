"""DOCUMENTATION REFERENCE

    OMX Player is the raspberry pi native video player application. It is evoked from the
    command line. For this programs, the documentation is only used to supply the arguments
    during the player initialization.
    LINK: https://www.raspberrypi.org/documentation/raspbian/applications/omxplayer.md

    OMX Player Wrapper is used to provide an easy interface to play, pause, stop, etc.
    LINK: https://python-omxplayer-wrapper.readthedocs.io/en/latest/
"""

import time
from omxplayer.player import OMXPlayer

_PLAYER = None  # placeholder for OMX player
_INIT = False
_SLEEP = 0.55


def initialize(path):
    """Initialize the player with your specific arguments. Please see documentation above
    for additional context.

    The necessary args should be:
    --no-osd to prevent controls from being visible
    --loop to...well, loop the video.

    Returns:
        OMXPlayer instance
    """
    global _PLAYER, _INIT

    _PLAYER = OMXPlayer(path, args=['--no-osd', '--loop'])

    # Sleep is here for the player to have enough time to load the video into the buffer.
    # Different videos may require different buffer time.
    time.sleep(_SLEEP)
    _INIT = True

    return _PLAYER


def close():
    """Verifies that player was actual initialized. Can fail if timing is off
    and/or distance isn't calculated.
    """

    if _PLAYER and hasattr(_PLAYER, 'quit'):
        _PLAYER.quit()
