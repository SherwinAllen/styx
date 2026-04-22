import math
import random
import time

from selenium.webdriver.common.action_chains import ActionChains


_TYPING_MU = -2.1
_TYPING_SIGMA = 0.55

_PAUSE_PROBABILITY = 0.06
_PAUSE_DURATION_MIN = 0.35
_PAUSE_DURATION_MAX = 1.10

_TYPO_PROBABILITY = 0.03

_MOUSE_DRIFT_DURING_TYPING_PROB = 0.12
_PRE_CLICK_WANDER_PROB = 0.55

_NEIGHBOURS = {
    'a': 'sqwz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wsdr',
    'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'i': 'ujko', 'j': 'huikm',
    'k': 'jiol', 'l': 'kop', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
    'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgy',
    'u': 'yhij', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
    'z': 'asx',
    '0': '9', '1': '2', '2': '13', '3': '24', '4': '35', '5': '46',
    '6': '57', '7': '68', '8': '79', '9': '80',
}


def _keystroke_delay():
    return random.lognormvariate(_TYPING_MU, _TYPING_SIGMA)


def _bezier_point(p0, p1, p2, p3, t):
    u = 1 - t
    x = (u ** 3) * p0[0] + 3 * (u ** 2) * t * p1[0] + 3 * u * (t ** 2) * p2[0] + (t ** 3) * p3[0]
    y = (u ** 3) * p0[1] + 3 * (u ** 2) * t * p1[1] + 3 * u * (t ** 2) * p2[1] + (t ** 3) * p3[1]
    return x, y


def _generate_curve_offsets(total_steps):
    start = (0.0, 0.0)
    end_jitter_x = random.uniform(-3.0, 3.0)
    end_jitter_y = random.uniform(-3.0, 3.0)
    end = (end_jitter_x, end_jitter_y)

    dx = end[0] - start[0]
    dy = end[1] - start[1]

    perp_x = -dy
    perp_y = dx
    perp_len = math.hypot(perp_x, perp_y) or 1.0
    perp_x /= perp_len
    perp_y /= perp_len

    curve_strength = random.uniform(15.0, 45.0) * random.choice([-1, 1])

    ctrl1 = (
        start[0] + dx * 0.33 + perp_x * curve_strength * random.uniform(0.6, 1.0),
        start[1] + dy * 0.33 + perp_y * curve_strength * random.uniform(0.6, 1.0),
    )
    ctrl2 = (
        start[0] + dx * 0.66 + perp_x * curve_strength * random.uniform(0.4, 0.9),
        start[1] + dy * 0.66 + perp_y * curve_strength * random.uniform(0.4, 0.9),
    )

    points = []
    last_x, last_y = 0.0, 0.0
    for i in range(1, total_steps + 1):
        t = i / total_steps
        t_eased = t * t * (3 - 2 * t)
        px, py = _bezier_point(start, ctrl1, ctrl2, end, t_eased)
        px += random.uniform(-0.8, 0.8)
        py += random.uniform(-0.8, 0.8)
        step_dx = px - last_x
        step_dy = py - last_y
        points.append((step_dx, step_dy))
        last_x, last_y = px, py

    return points


def _curved_move_to_element(driver, element):
    total_steps = random.randint(18, 34)
    offsets = _generate_curve_offsets(total_steps)

    actions = ActionChains(driver)
    actions.move_to_element(element)
    for dx, dy in offsets:
        actions.move_by_offset(dx, dy)
        actions.pause(random.uniform(0.004, 0.018))
    actions.perform()


def human_mouse_wander(driver, anchor_element=None, moves=None):
    try:
        if moves is None:
            moves = random.randint(1, 3)
        actions = ActionChains(driver)
        if anchor_element is not None:
            actions.move_to_element(anchor_element)
        for _ in range(moves):
            dx = random.uniform(-80, 80)
            dy = random.uniform(-50, 50)
            steps = random.randint(4, 9)
            for i in range(steps):
                frac = 1 / steps
                actions.move_by_offset(dx * frac + random.uniform(-1.5, 1.5),
                                       dy * frac + random.uniform(-1.0, 1.0))
                actions.pause(random.uniform(0.008, 0.030))
            actions.pause(random.uniform(0.15, 0.45))
        actions.perform()
    except Exception:
        pass


def human_click(driver, element):
    _curved_move_to_element(driver, element)
    time.sleep(random.uniform(0.12, 0.38))
    element.click()
    time.sleep(random.uniform(0.10, 0.28))


def human_type(driver, element, text, *, click_first=True):
    if click_first:
        human_click(driver, element)

    element.clear()
    time.sleep(random.uniform(0.10, 0.25))

    for idx, char in enumerate(text):
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
            time.sleep(random.uniform(0.18, 0.55))
            element.send_keys('\ue003')
            time.sleep(_keystroke_delay())

        element.send_keys(char)

        if idx > 0 and idx < len(text) - 1 and random.random() < _MOUSE_DRIFT_DURING_TYPING_PROB:
            try:
                actions = ActionChains(driver)
                drift_steps = random.randint(2, 5)
                for _ in range(drift_steps):
                    actions.move_by_offset(random.uniform(-4, 4), random.uniform(-3, 3))
                    actions.pause(random.uniform(0.005, 0.020))
                actions.perform()
            except Exception:
                pass

        delay = _keystroke_delay()
        if random.random() < _PAUSE_PROBABILITY:
            delay += random.uniform(_PAUSE_DURATION_MIN, _PAUSE_DURATION_MAX)
        time.sleep(delay)

    time.sleep(random.uniform(0.3, 0.8))