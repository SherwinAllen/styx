"""
human_interaction.py
--------------------
Drop-in helpers for generateCookies.py to defeat Amazon's bot detection
during the email/password login flow.

USAGE
-----
1. Place this file next to generateCookies.py.
2. In generateCookies.py, add this import near the top (after the existing
   Selenium imports):

       from human_interaction import human_type, human_click

   That's it — the modified perform_full_authentication() and handle_re_auth()
   in generateCookies.py already call human_type() and human_click() directly.

WHY THIS WORKS
--------------
Amazon's bot-detection JS observes:
  • Inter-keystroke timing  — uniform ms gaps = bot, log-normal = human
  • Whether mousemove/mouseenter fired BEFORE a click
  • Whether focus events precede input events

send_keys(full_string) fires every character in a single burst with zero
timing variance and no prior mouse movement — trivially identifiable.
human_type() and human_click() fix both signals with minimal overhead.
"""

import random
import time

from selenium.webdriver.common.action_chains import ActionChains


# ---------------------------------------------------------------------------
# Tuning constants  (adjust if needed)
# ---------------------------------------------------------------------------

# Log-normal inter-keystroke delay: median ~122 ms, realistic spread.
_TYPING_MU    = -2.1
_TYPING_SIGMA =  0.55

# Occasional mid-word pause (thinking / muscle-memory hiccup).
_PAUSE_PROBABILITY  = 0.06
_PAUSE_DURATION_MIN = 0.35
_PAUSE_DURATION_MAX = 1.10

# Typo + backspace correction — set to 0.0 to disable entirely.
_TYPO_PROBABILITY = 0.03

# Adjacent keys on a standard QWERTY layout.
_NEIGHBOURS: dict[str, str] = {
    'a': 'sqwz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wsdr',
    'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'i': 'ujko', 'j': 'huikm',
    'k': 'jiol', 'l': 'kop', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
    'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgy',
    'u': 'yhij', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
    'z': 'asx',
    '0': '9', '1': '2', '2': '13', '3': '24', '4': '35', '5': '46',
    '6': '57', '7': '68', '8': '79', '9': '80',
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _keystroke_delay() -> float:
    """Log-normal inter-keystroke delay in seconds."""
    return random.lognormvariate(_TYPING_MU, _TYPING_SIGMA)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def human_click(driver, element) -> None:
    """
    Click *element* in a human-like way.

    Fires mouseenter/mousemove via ActionChains.move_to_element() — the
    minimum Amazon's JS needs to see before a click — then waits a short
    random pause that mimics human reaction time before clicking.
    """
    ActionChains(driver).move_to_element(element).perform()
    time.sleep(random.uniform(0.08, 0.30))   # hover → click reaction time
    element.click()
    time.sleep(random.uniform(0.10, 0.25))   # brief post-click pause


def human_type(driver, element, text: str, *, click_first: bool = True) -> None:
    """
    Type *text* into *element* one character at a time with realistic timing.

    Features:
      • Log-normal inter-keystroke delays (matches empirical typing studies).
      • Random mid-word pauses (distraction / muscle-memory hesitation).
      • Optional typo + backspace correction to further break uniformity.
      • Clicks the element first (triggering mouseenter/focus) unless
        click_first=False.
    """
    if click_first:
        human_click(driver, element)

    element.clear()
    time.sleep(random.uniform(0.10, 0.25))

    for char in text:
        # Optional typo + immediate correction
        if (
            char.isalpha()
            and char.lower() in _NEIGHBOURS
            and random.random() < _TYPO_PROBABILITY
        ):
            wrong = random.choice(_NEIGHBOURS[char.lower()])
            if char.isupper():
                wrong = wrong.upper()
            element.send_keys(wrong)
            time.sleep(_keystroke_delay())
            time.sleep(random.uniform(0.18, 0.55))  # "notice" the mistake
            element.send_keys('\ue003')              # Backspace
            time.sleep(_keystroke_delay())

        # Type the real character
        element.send_keys(char)

        # Inter-keystroke delay, with occasional longer pause
        delay = _keystroke_delay()
        if random.random() < _PAUSE_PROBABILITY:
            delay += random.uniform(_PAUSE_DURATION_MIN, _PAUSE_DURATION_MAX)
        time.sleep(delay)

    # Post-field pause — humans glance at what they typed before moving on.
    time.sleep(random.uniform(0.3, 0.8))