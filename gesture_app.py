"""
╔══════════════════════════════════════════════════════╗
║   🖐️  Hand Gesture App — Unified Launcher  🖐️       ║
╚══════════════════════════════════════════════════════╝

A single script that lets you choose at startup:
  [1]  Distance Math Calculator  — measure & calculate with fingers
  [2]  AI Virtual Mouse          — control your entire Mac with gestures
  [3]  On-Screen Keyboard        — type using hand gestures
  [Q]  Quit

Run:
    python gesture_app.py
"""
import cv2
import mediapipe as mp
import numpy as np
import math
import time
import pyautogui
import webbrowser
import os
import pyperclip
import shutil

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

try:
    import Quartz

    def _post(event_type, x, y, button=Quartz.kCGMouseButtonLeft):
        pt = Quartz.CGPoint(x, y)
        ev = Quartz.CGEventCreateMouseEvent(None, event_type, pt, button)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, ev)

    def mac_move(x, y):
        _post(Quartz.kCGEventMouseMoved, x, y)

    def mac_left_click(x, y):
        _post(Quartz.kCGEventLeftMouseDown, x, y)
        _post(Quartz.kCGEventLeftMouseUp, x, y)

    def mac_right_click(x, y):
        _post(Quartz.kCGEventRightMouseDown, x, y, Quartz.kCGMouseButtonRight)
        _post(Quartz.kCGEventRightMouseUp, x, y, Quartz.kCGMouseButtonRight)

    def mac_mouse_down(x, y):
        _post(Quartz.kCGEventLeftMouseDown, x, y)

    def mac_mouse_up(x, y):
        _post(Quartz.kCGEventLeftMouseUp, x, y)

    def mac_drag(x, y):
        _post(Quartz.kCGEventLeftMouseDragged, x, y)

    def mac_scroll(dx, dy):
        ev = Quartz.CGEventCreateScrollWheelEvent(
            None,
            Quartz.kCGScrollEventUnitLine,
            2,
            int(dy),
            int(dx)
        )
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, ev)

    def get_screen_size():
        bounds = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
        return int(bounds.size.width), int(bounds.size.height)

except ImportError:
    import ctypes
    import pyautogui

    def mac_move(x, y):
        ctypes.windll.user32.SetCursorPos(int(x), int(y))

    def mac_left_click(x, y):
        ctypes.windll.user32.SetCursorPos(int(x), int(y))
        pyautogui.click()

    def mac_right_click(x, y):
        ctypes.windll.user32.SetCursorPos(int(x), int(y))
        pyautogui.rightClick()

    def mac_mouse_down(x, y):
        ctypes.windll.user32.SetCursorPos(int(x), int(y))
        pyautogui.mouseDown()

    def mac_mouse_up(x, y):
        ctypes.windll.user32.SetCursorPos(int(x), int(y))
        pyautogui.mouseUp()

    def mac_drag(x, y):
        ctypes.windll.user32.SetCursorPos(int(x), int(y))

    def mac_scroll(dx, dy):
        pyautogui.scroll(int(dy * 100))

    def get_screen_size():
        return pyautogui.size()


import HandTrackingModule as htm

CAM_W, CAM_H = 1280, 720
PIXELS_PER_CM = 25.0

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

try:
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
except:
    pass


class Button:

    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

    def draw(self, img):
        x, y = self.pos
        w, h = self.size

        cv2.rectangle(
            img,
            self.pos,
            (x + w, y + h),
            (255, 255, 255),
            -1
        )

        cv2.rectangle(
            img,
            self.pos,
            (x + w, y + h),
            (0, 0, 0),
            2
        )

        font_scale = 1.2 if len(self.text) < 3 else 0.7

        cv2.putText(
            img,
            self.text,
            (x + 20, y + 55),
            cv2.FONT_HERSHEY_DUPLEX,
            font_scale,
            (0, 0, 0),
            2
        )

    def is_over(self, x, y):
        bx, by = self.pos
        bw, bh = self.size

        return bx < x < bx + bw and by < y < by + bh


def get_pt(lm, idx, w, h):
    return int(lm[idx].x * w), int(lm[idx].y * h)


def dist(p1, p2):
    return math.hypot(
        p2[0] - p1[0],
        p2[1] - p1[1]
    )


def mode_selection_screen(cap):
    """Shows a fullscreen menu until user presses 1, 2, or Q."""

    print("\n╔══════════════════════════════════════╗")
    print("║   🖐  Hand Gesture App Launcher      ║")
    print("╠══════════════════════════════════════╣")
    print("║  Press  1  → Math Calculator         ║")
    print("║  Press  2  → AI Virtual Mouse        ║")
    print("║  Press  3  → On-Screen Keyboard      ║")
    print("║  Press  Q  → Quit                    ║")
    print("╚══════════════════════════════════════╝\n")

    while True:
        ok, frame = cap.read()

        if not ok:
            continue

        frame = cv2.flip(frame, 1)

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (CAM_W, CAM_H),
            (15, 15, 15),
            -1
        )

        cv2.addWeighted(
            overlay,
            0.65,
            frame,
            0.35,
            0,
            frame
        )

        cv2.putText(
            frame,
            "🖐  Hand Gesture",
            (200, 120),
            cv2.FONT_HERSHEY_DUPLEX,
            2.0,
            (0, 220, 255),
            3
        )

        cv2.putText(
            frame,
            "Choose your mode:",
            (350, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (200, 200, 200),
            2
        )

        cv2.rectangle(
            frame,
            (150, 280),
            (560, 420),
            (40, 40, 40),
            -1
        )

        cv2.rectangle(
            frame,
            (150, 280),
            (560, 420),
            (0, 220, 255),
            3
        )

        cv2.putText(
            frame,
            "Press  1",
            (220, 340),
            cv2.FONT_HERSHEY_DUPLEX,
            1.4,
            (0, 220, 255),
            3
        )

        cv2.putText(
            frame,
            "Math Calculator",
            (175, 400),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (200, 200, 200),
            2
        )

        cv2.rectangle(
            frame,
            (700, 280),
            (1110, 420),
            (40, 40, 40),
            -1
        )

        cv2.rectangle(
            frame,
            (700, 280),
            (1110, 420),
            (0, 255, 100),
            3
        )

        cv2.putText(
            frame,
            "Press  2",
            (770, 340),
            cv2.FONT_HERSHEY_DUPLEX,
            1.4,
            (0, 255, 100),
            3
        )

        cv2.putText(
            frame,
            "AI Virtual Mouse",
            (715, 400),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (200, 200, 200),
            2
        )

        cv2.rectangle(
            frame,
            (425, 450),
            (835, 590),
            (40, 40, 40),
            -1
        )

        cv2.rectangle(
            frame,
            (425, 450),
            (835, 590),
            (255, 100, 255),
            3
        )

        cv2.putText(
            frame,
            "Press  3",
            (545, 510),
            cv2.FONT_HERSHEY_DUPLEX,
            1.4,
            (255, 100, 255),
            3
        )

        cv2.putText(
            frame,
            "On-Screen Keyboard",
            (480, 570),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (200, 200, 200),
            2
        )

        cv2.putText(
            frame,
            "Press Q to quit",
            (520, 640),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (120, 120, 120),
            1
        )

        cv2.imshow("🖐 Hand Gesture App", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('1'):
            return 'math'

        elif key == ord('2'):
            return 'mouse'

        elif key == ord('3'):
            return 'keyboard'

        elif key in (ord('q'), ord('Q'), 27):
            return 'quit'


STATE_NUM1 = 0
STATE_OP = 1
STATE_NUM2 = 2
STATE_RESULT = 3

STATE_MSG = {
    STATE_NUM1:
        "Step 1: Set Thumb↔Finger distance → PINCH (Index+Middle) to save",

    STATE_OP:
        "Step 2: Press  +  -  *  /  on keyboard to choose operator",

    STATE_NUM2:
        "Step 3: Set new distance → PINCH again to calculate",

    STATE_RESULT:
        "Result shown! Press C to clear or M to go back to menu.",
}


def run_math_calculator(cap):

    mp_hands = mp.solutions.hands

    hd = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.6
    )

    mp_draw = mp.solutions.drawing_utils

    state = STATE_NUM1
    num1 = num2 = result = op = None
    delay = 0

    target_idx = 8
    target_name = "Index"

    print(
        "\n[MATH CALCULATOR] Running. "
        "Press M to go back to menu, Q to quit."
    )

    while True:

        ok, img = cap.read()

        if not ok:
            break

        img = cv2.flip(img, 1)

        rgb = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        results = hd.process(rgb)

        h, w = img.shape[:2]

        cm_dist = 0.0

        if results.multi_hand_landmarks:

            for lm in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    img,
                    lm,
                    mp_hands.HAND_CONNECTIONS
                )

                tx, ty = get_pt(
                    lm.landmark,
                    4,
                    w,
                    h
                )

                fx, fy = get_pt(
                    lm.landmark,
                    target_idx,
                    w,
                    h
                )

                cx, cy = (
                    (tx + fx) // 2,
                    (ty + fy) // 2
                )

                cv2.circle(
                    img,
                    (tx, ty),
                    12,
                    (0, 200, 255),
                    -1
                )

                cv2.circle(
                    img,
                    (fx, fy),
                    12,
                    (0, 200, 255),
                    -1
                )

                cv2.line(
                    img,
                    (tx, ty),
                    (fx, fy),
                    (0, 200, 255),
                    3
                )

                pix = dist(
                    (tx, ty),
                    (fx, fy)
                )

                cm_dist = (
                    0.0
                    if pix < 38
                    else round(pix / PIXELS_PER_CM, 2)
                )

                dot_c = (
                    (0, 255, 0)
                    if pix < 38
                    else (0, 255, 255)
                )

                cv2.circle(
                    img,
                    (cx, cy),
                    14,
                    dot_c,
                    -1
                )

                cv2.putText(
                    img,
                    f"{cm_dist:.1f} cm",
                    (cx - 40, cy - 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 255, 255),
                    3
                )

                cv2.putText(
                    img,
                    f"Thumb→{target_name}",
                    (tx - 20, ty - 18),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 200, 255),
                    2
                )

                ix, iy = get_pt(
                    lm.landmark,
                    8,
                    w,
                    h
                )

                mx2, my2 = get_pt(
                    lm.landmark,
                    12,
                    w,
                    h
                )

                trig = dist(
                    (ix, iy),
                    (mx2, my2)
                )

                tc = (
                    (0, 255, 0)
                    if trig < 35
                    else (180, 180, 180)
                )

                cv2.circle(
                    img,
                    (ix, iy),
                    8,
                    tc,
                    -1
                )

                cv2.circle(
                    img,
                    (mx2, my2),
                    8,
                    tc,
                    -1
                )

                if trig < 35 and delay == 0:

                    if state == STATE_NUM1:

                        num1 = cm_dist
                        state = STATE_OP

                        print(
                            f"Saved Number 1 = {num1:.1f} cm"
                        )

                    elif state == STATE_NUM2:

                        num2 = cm_dist

                        if op == '+':
                            result = num1 + num2

                        elif op == '-':
                            result = num1 - num2

                        elif op == '*':
                            result = num1 * num2

                        elif op == '/':
                            result = num1 / num2 if num2 else 0

                        state = STATE_RESULT

                        print(
                            f"{num1:.1f} {op} "
                            f"{num2:.1f} = {result:.2f}"
                        )

                    delay = 1

        if delay:

            delay += 1

            if delay > 22:
                delay = 0

        cv2.rectangle(
            img,
            (0, 0),
            (w, 210),
            (20, 20, 20),
            -1
        )

        eq = ""

        if num1 is not None:
            eq += f"{num1:.1f} cm"

        if op:
            eq += f" {op} "

        if num2 is not None:
            eq += f"{num2:.1f} cm"

        if result is not None:
            eq += f" = {result:.2f} cm"

        cv2.putText(
            img,
            STATE_MSG[state],
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.62,
            (0, 220, 255),
            2
        )

        cv2.putText(
            img,
            eq if eq else "---",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.6,
            (255, 255, 255),
            4
        )

        cv2.putText(
            img,
            "Keys: 1=Index  2=Middle | C=Clear M=Menu Q=Quit",
            (20, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (130, 130, 130),
            1
        )

        cv2.imshow(
            "🖐 Hand Gesture App",
            img
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            return 'quit'

        elif key == ord('m'):
            return 'menu'

        elif key == ord('c'):
            state, num1, op, num2, result = (
                STATE_NUM1,
                None,
                None,
                None,
                None
            )

        elif key == ord('1'):
            target_idx, target_name = 8, "Index"

        elif key == ord('2'):
            target_idx, target_name = 12, "Middle"

        elif state == STATE_OP:

            if key == ord('+'):
                op = '+'
                state = STATE_NUM2

            elif key == ord('-'):
                op = '-'
                state = STATE_NUM2

            elif key == ord('*'):
                op = '*'
                state = STATE_NUM2

            elif key == ord('/'):
                op = '/'
                state = STATE_NUM2

    return 'quit'


def run_virtual_mouse(cap):

    FRAME_R = 60
    SMOOTH = 4
    CLICK_THRESH = 40
    SCROLL_SPD = 5
    COOLDOWN = 0.35

    detector = htm.handDetector(
        maxHands=1,
        detectionCon=0.5,
        trackCon=0.5
    )

    wScr, hScr = get_screen_size()

    plocX = plocY = 0
    pTime = 0
    last_lclick = 0
    last_rclick = 0
    prev_wrist_y = 0
    scroll_active = False
    drag_active = False

    mode_name = "IDLE"

    fingers = [0, 0, 0, 0, 0]

    try:
        cur_x, cur_y = pyautogui.position()
        plocX, plocY = float(cur_x), float(cur_y)

    except:
        plocX, plocY = 0.0, 0.0

    print(
        f"\n[VIRTUAL MOUSE] Running. Screen: {wScr}x{hScr}"
    )

    print("  ☝️  Index only         → Move cursor")
    print("  ✌️  Index+Middle pinch → Left click")
    print("  🤟  +Ring pinch        → Right click")
    print("  ✋  All 5 open         → Scroll up/down")
    print("  👍  Thumb+Index pinch  → Drag & Drop")
    print("  M → Back to menu  |  Q → Quit\n")

    while True:

        ok, img = cap.read()

        if not ok:
            break

        img = cv2.flip(img, 1)

        h, w = img.shape[:2]

        if not hasattr(run_virtual_mouse, "logged_size"):
            print(
                f"DEBUG: Camera Frame Size: {w}x{h}"
            )
            run_virtual_mouse.logged_size = True

        img = detector.findHands(img)

        lmList, _ = detector.findPosition(
            img,
            draw=False
        )

        h, w = img.shape[:2]

        now = time.time()

        if len(lmList) != 0:

            fingers = detector.fingersUp()

            x1, y1 = lmList[8][1:]

            cv2.rectangle(
                img,
                (FRAME_R, FRAME_R + 80),
                (CAM_W - FRAME_R, CAM_H - FRAME_R),
                (255, 0, 255),
                2
            )

            def to_screen(px, py):

                sx = np.interp(
                    px,
                    (FRAME_R, CAM_W - FRAME_R),
                    (0, wScr)
                )

                sy = np.interp(
                    py,
                    (FRAME_R + 80, CAM_H - FRAME_R),
                    (0, hScr)
                )

                return sx, sy

            upCount = sum(fingers[1:])

            if upCount >= 4:

                mode_name = "SCROLL"

                if drag_active:
                    mac_mouse_up(
                        int(plocX),
                        int(plocY)
                    )
                    drag_active = False

                wrist_y = lmList[0][2]

                if not scroll_active:
                    prev_wrist_y = wrist_y
                    scroll_active = True

                else:

                    delta = prev_wrist_y - wrist_y

                    if abs(delta) > 3:
                        mac_scroll(
                            0,
                            int(delta * SCROLL_SPD / 15)
                        )

                        prev_wrist_y = wrist_y

            elif fingers[0] == 1 and fingers[1] == 1:

                length_d, img, li_d = detector.findDistance(
                    4,
                    8,
                    img
                )

                if length_d < 45:

                    mode_name = "DRAGGING"

                    if not drag_active:
                        mac_mouse_down(
                            int(plocX),
                            int(plocY)
                        )
                        drag_active = True

                    sx, sy = to_screen(x1, y1)

                    clocX = plocX + (
                        sx - plocX
                    ) / SMOOTH

                    clocY = plocY + (
                        sy - plocY
                    ) / SMOOTH

                    mac_drag(
                        int(clocX),
                        int(clocY)
                    )

                    cv2.circle(
                        img,
                        (x1, y1),
                        20,
                        (0, 165, 255),
                        -1
                    )

                    plocX, plocY = clocX, clocY

                else:

                    if drag_active:
                        mac_mouse_up(
                            int(plocX),
                            int(plocY)
                        )

                        drag_active = False
                        mode_name = "DROPPED"

                    mode_name = "DRAG READY"

            elif fingers[1] == 1:

                len_l, img, li_l = detector.findDistance(
                    8,
                    12,
                    img
                )

                if len_l < CLICK_THRESH:

                    mode_name = "CLICKED"

                    if (now - last_lclick) > COOLDOWN:

                        mac_left_click(
                            int(plocX),
                            int(plocY)
                        )

                        last_lclick = now

                else:

                    mode_name = "MOVE"

                    sx, sy = to_screen(x1, y1)

                    clocX = plocX + (
                        sx - plocX
                    ) / SMOOTH

                    clocY = plocY + (
                        sy - plocY
                    ) / SMOOTH

                    try:
                        mac_move(
                            int(clocX),
                            int(clocY)
                        )
                    except:
                        pass

                    plocX, plocY = clocX, clocY

                    cv2.circle(
                        img,
                        (x1, y1),
                        12,
                        (255, 0, 255),
                        -1
                    )

            else:

                if drag_active:
                    mac_mouse_up(
                        int(plocX),
                        int(plocY)
                    )
                    drag_active = False

                scroll_active = False
                mode_name = "IDLE"

        else:

            if drag_active:
                mac_mouse_up(
                    int(plocX),
                    int(plocY)
                )
                drag_active = False

            scroll_active = False
            mode_name = "NO HAND"

        cv2.rectangle(
            img,
            (0, 0),
            (CAM_W, 75),
            (20, 20, 20),
            -1
        )

        cTime = time.time()

        fps = (
            1 / (cTime - pTime)
            if (cTime - pTime) > 0
            else 0
        )

        pTime = cTime

        cv2.putText(
            img,
            f"FPS:{int(fps)}",
            (12, 52),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )

        MODE_COLORS = {
            "MOVE": (255, 0, 255),
            "CLICKED!": (0, 255, 0),
            "R-CLICKED!": (0, 100, 255),
            "LEFT CLICK": (0, 230, 255),
            "RIGHT CLICK": (0, 0, 255),
            "SCROLL": (255, 255, 0),
            "DRAG": (0, 165, 255),
            "DRAGGING": (0, 165, 255),
            "DROPPED": (180, 180, 180),
            "IDLE": (120, 120, 120),
            "NO HAND": (80, 80, 80),
        }

        col = MODE_COLORS.get(
            mode_name,
            (255, 255, 255)
        )

        cv2.putText(
            img,
            f"Mode: {mode_name}",
            (130, 52),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            col,
            3
        )

        cv2.putText(
            img,
            f"Fingers: {fingers}",
            (CAM_W - 300, 52),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        gest_hint = (
            "☝Move  ✌LClick  🤟RClick  "
            "✋Scroll  👍Drag  |  M=Menu  Q=Quit"
        )

        cv2.putText(
            img,
            gest_hint,
            (12, 720 - 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (100, 100, 100),
            1
        )

        cv2.imshow(
            "🖐 Hand Gesture App",
            img
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            return 'quit'

        elif key == ord('m'):
            return 'menu'

    return 'quit'


def run_virtual_keyboard(cap):

    detector = htm.handDetector(
        maxHands=1,
        detectionCon=0.5,
        trackCon=0.5
    )

    screen_w, screen_h = get_screen_size()

    plocX, plocY = 0, 0
    last_lclick = 0
    last_rclick = 0
    prev_wrist_y = 0
    scroll_active = False

    mode_name = "IDLE"
    target_mode = "IDLE"
    mode_count = 0

    HYST_THRESH = 3

    l_pinched = False
    r_pinched = False
    l_pinch_start = 0
    last_click_time = 0
    is_dragging = False

    text_buffer = ""

    CLICK_THRESH = 50
    CLICK_THRESH_MOUSE = 45
    COOLDOWN = 0.4
    SMOOTH = 8

    pyautogui.PAUSE = 0

    locked_btn = None
    is_mini = False

    cv2.namedWindow(
        "Hand Gesture App",
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        "Hand Gesture App",
        CAM_W,
        CAM_H
    )

    keys = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
    ]

    buttonList = []

    for r, row in enumerate(keys):

        for i, key in enumerate(row):

            buttonList.append(
                Button(
                    [100 * i + 50, 100 * r + 150],
                    key
                )
            )

    buttonList.append(
        Button([50, 450], "BACKSPACE", [240, 85])
    )

    buttonList.append(
        Button([300, 450], "SPACE", [350, 85])
    )

    buttonList.append(
        Button([660, 450], "CLEAR", [130, 85])
    )

    buttonList.append(
        Button([800, 450], "ENTER", [140, 85])
    )

    buttonList.append(
        Button([950, 450], "MINI", [120, 85])
    )

    def is_local_item(query):
        """Checks if the query matches an app, command, or file.
        Returns the path if found."""

        if not query:
            return None

        cmd_path = shutil.which(query)

        if cmd_path:
            return cmd_path

        query = query.lower().strip()

        search_paths = []

        if "ProgramData" in os.environ:

            search_paths.append(
                os.path.join(
                    os.environ["ProgramData"],
                    "Microsoft",
                    "Windows",
                    "Start Menu",
                    "Programs"
                )
            )

        if "AppData" in os.environ:

            search_paths.append(
                os.path.join(
                    os.environ["AppData"],
                    "Roaming",
                    "Microsoft",
                    "Windows",
                    "Start Menu",
                    "Programs"
                )
            )

        user_home = os.path.expanduser("~")

        search_paths.extend([
            os.path.join(user_home, "Desktop"),
            os.path.join(user_home, "Documents"),
            os.path.join(user_home, "Downloads"),
        ])

        for path in search_paths:

            if not os.path.exists(path):
                continue

            try:

                for item in os.listdir(path):

                    if query in item.lower():
                        return os.path.join(path, item)

            except:
                pass

        return None

    print("\n" + "═" * 50)
    print("  🖐  VIRTUAL MOUSE & KEYBOARD - GESTURE GUIDE")
    print("═" * 50)

    print("  [MOUSE MODE] (1-2 Fingers up)")
    print("  • Move Cursor   : Move Hand")
    print("  • Left Click    : Pinch Index + Thumb")
    print("  • Right Click   : Pinch Middle + Thumb")
    print("  • Double Click  : Pinch Index + Thumb twice")
    print("  • Drag & Drop   : Pinch and Hold Index + Thumb")

    print("-" * 50)

    print("  [SCROLL MODE] (3-5 Fingers up)")
    print("  • Scroll Up/Down: Move Flat Palm Up/Down")

    print("-" * 50)

    print("  [KEYBOARD MODE]")
    print("  • Type Key      : Hover + Pinch Index + Thumb")
    print("  • Smart Search  : Pinch ENTER (Auto-hides keyboard)")
    print("  • Open Keyboard : Pinch 'KEYBOARD' button in corner")

    print("═" * 50 + "\n")

    while True:

        success, img = cap.read()

        if not success:
            break

        img = cv2.flip(img, 1)

        h, w = img.shape[:2]

        now = time.time()

        img = detector.findHands(
            img,
            draw=True
        )

        lmList, _ = detector.findPosition(
            img,
            draw=False
        )

        if not is_mini:

            for btn in buttonList:
                btn.draw(img)

            cv2.rectangle(
                img,
                (50, 50),
                (1010, 130),
                (30, 30, 30),
                cv2.FILLED
            )

            cv2.rectangle(
                img,
                (50, 50),
                (1010, 130),
                (200, 200, 200),
                2
            )

            cv2.putText(
                img,
                text_buffer + (
                    "|" if (now % 1 > 0.5)
                    else ""
                ),
                (70, 110),
                cv2.FONT_HERSHEY_DUPLEX,
                1.8,
                (255, 255, 255),
                3
            )

        else:

            for btn in buttonList:

                if btn.text == "KEYBOARD":

                    btn.pos = [10, 10]
                    btn.size = [150, 60]
                    btn.draw(img)

                    break

        has_hand = len(lmList) != 0

        status_text = (
            "HAND DETECTED"
            if has_hand
            else "NO HAND"
        )

        status_col = (
            (0, 255, 0)
            if has_hand
            else (0, 0, 255)
        )

        cv2.putText(
            img,
            status_text,
            (350, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            status_col,
            2
        )

        if has_hand:

            x1, y1 = lmList[8][1:]

            fingers = detector.fingersUp()

            raw_mode = "MOUSE"
            curr_hover = None

            for btn in buttonList:

                if is_mini:

                    if (
                        btn.text == "KEYBOARD"
                        and btn.is_over(x1, y1)
                    ):
                        curr_hover = btn
                        raw_mode = "KEYBOARD"
                        break

                else:

                    if btn.is_over(x1, y1):

                        curr_hover = btn
                        raw_mode = "KEYBOARD"
                        break

            upCount = sum(fingers[1:])

            if raw_mode == "MOUSE" and upCount >= 3:
                raw_mode = "SCROLL"

            if not is_mini:

                cv2.putText(
                    img,
                    f"Fingers: {upCount}",
                    (20, h - 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

            if raw_mode == target_mode:

                mode_count += 1

            else:

                target_mode = raw_mode
                mode_count = 0

            if mode_count >= HYST_THRESH:

                if mode_name != target_mode:

                    print(
                        f"[MODE] Stable Switch to: {target_mode}"
                    )

                    mode_name = target_mode
                    scroll_active = False

            if mode_name == "KEYBOARD" or locked_btn:

                target = (
                    locked_btn
                    if locked_btn
                    else curr_hover
                )

                if target:

                    bx, by = target.pos
                    bw, bh = target.size

                    cv2.rectangle(
                        img,
                        target.pos,
                        (bx + bw, by + bh),
                        (0, 255, 0),
                        cv2.FILLED
                    )

                    cv2.putText(
                        img,
                        target.text,
                        (bx + 20, by + 55),
                        cv2.FONT_HERSHEY_DUPLEX,
                        (
                            1.2
                            if len(target.text) < 3
                            else 0.7
                        ),
                        (0, 0, 0),
                        2
                    )

                    length, img, line_info = detector.findDistance(
                        4,
                        8,
                        img
                    )

                    dist_col = (
                        (0, 255, 0)
                        if length < CLICK_THRESH
                        else (0, 0, 255)
                    )

                    cv2.putText(
                        img,
                        f"Dist: {int(length)}",
                        (w - 150, 110),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        dist_col,
                        2
                    )

                    if length < CLICK_THRESH:

                        if not locked_btn and curr_hover:
                            locked_btn = curr_hover

                        if (
                            now - last_lclick
                        ) > COOLDOWN and locked_btn:

                            last_lclick = now

                            val = locked_btn.text

                            if val == "BACKSPACE":
                                text_buffer = text_buffer[:-1]

                            elif val == "SPACE":
                                text_buffer += " "

                            elif val == "CLEAR":
                                text_buffer = ""

                            elif val == "MINI" or val == "KEYBOARD":

                                is_mini = not is_mini

                                if is_mini:

                                    cv2.resizeWindow(
                                        "Hand Gesture App",
                                        320,
                                        240
                                    )

                                    cv2.moveWindow(
                                        "Hand Gesture App",
                                        10,
                                        10
                                    )

                                else:

                                    cv2.resizeWindow(
                                        "Hand Gesture App",
                                        CAM_W,
                                        CAM_H
                                    )

                                    cv2.moveWindow(
                                        "Hand Gesture App",
                                        100,
                                        100
                                    )

                                    for b in buttonList:

                                        if b.text in [
                                            "MINI",
                                            "KEYBOARD"
                                        ]:

                                            b.text = "MINI"
                                            b.pos = [950, 450]
                                            b.size = [120, 85]

                            elif val == "ENTER":

                                query = text_buffer.strip()

                                if query:

                                    print(
                                        f"[SEARCH] Triggering Smart Search: '{query}'"
                                    )

                                    is_mini = True

                                    cv2.resizeWindow(
                                        "Hand Gesture App",
                                        320,
                                        240
                                    )

                                    cv2.moveWindow(
                                        "Hand Gesture App",
                                        10,
                                        10
                                    )

                                    found_path = is_local_item(query)

                                    if found_path:

                                        try:
                                            os.startfile(found_path)

                                        except:

                                            pyautogui.press('win')
                                            time.sleep(0.4)

                                            pyautogui.write(query)
                                            time.sleep(0.3)

                                            pyautogui.press('enter')

                                    else:

                                        url = (
                                            "https://www.google.com/search?q="
                                            + query.replace(" ", "+")
                                        )

                                        webbrowser.open(url)

                                    text_buffer = ""

                            else:

                                text_buffer += val

                            cv2.circle(
                                img,
                                (line_info[4], line_info[5]),
                                20,
                                (0, 255, 255),
                                cv2.FILLED
                            )

                    if locked_btn:

                        bx, by = locked_btn.pos

                        cv2.rectangle(
                            img,
                            locked_btn.pos,
                            (
                                bx + locked_btn.size[0],
                                by + locked_btn.size[1]
                            ),
                            (0, 255, 255),
                            3
                        )

                else:

                    locked_btn = None

                    for b in buttonList:

                        if b.text in ["MINI", "KEYBOARD"]:

                            if is_mini:

                                b.text = "KEYBOARD"
                                b.pos = [10, 10]
                                b.size = [150, 60]

                            else:

                                b.text = "MINI"
                                b.pos = [950, 450]
                                b.size = [120, 85]

            elif mode_name in ["SCROLL", "MOUSE"]:

                sx = np.interp(
                    x1,
                    (20, w - 20),
                    (0, screen_w)
                )

                sy = np.interp(
                    y1,
                    (120, h - 20),
                    (0, screen_h)
                )

                clocX = plocX + (
                    sx - plocX
                ) / SMOOTH

                clocY = plocY + (
                    sy - plocY
                ) / SMOOTH

                clocX, clocY = int(clocX), int(clocY)

                pyautogui.moveTo(
                    clocX,
                    clocY
                )

                plocX, plocY = clocX, clocY

                cv2.circle(
                    img,
                    (x1, y1),
                    8,
                    (255, 0, 255),
                    -1
                )

                cv2.line(
                    img,
                    (x1 - 15, y1),
                    (x1 + 15, y1),
                    (255, 0, 255),
                    2
                )

                cv2.line(
                    img,
                    (x1, y1 - 15),
                    (x1, y1 + 15),
                    (255, 0, 255),
                    2
                )

                if mode_name == "SCROLL":

                    wrist_y = lmList[0][2]

                    if not scroll_active:

                        prev_wrist_y = wrist_y
                        scroll_active = True

                    else:

                        delta = prev_wrist_y - wrist_y

                        if abs(delta) > 2:

                            scroll_val = int(delta * 6)

                            pyautogui.scroll(scroll_val)

                            prev_wrist_y = wrist_y

                    cv2.putText(
                        img,
                        "SCROLL MODE",
                        (w - 200, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 0),
                        2
                    )

                    cv2.line(
                        img,
                        (w - 50, 100),
                        (w - 50, 400),
                        (0, 255, 255),
                        2
                    )

                    cv2.circle(
                        img,
                        (
                            w - 50,
                            250 - int(wrist_y / 2)
                        ),
                        10,
                        (0, 255, 255),
                        -1
                    )

                else:

                    len_l, img, line_l = detector.findDistance(
                        4,
                        8,
                        img
                    )

                    len_r, img, line_r = detector.findDistance(
                        4,
                        12,
                        img
                    )

                    cv2.putText(
                        img,
                        f"L: {int(len_l)} R: {int(len_r)}",
                        (w - 200, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        1
                    )

                    if len_l < CLICK_THRESH_MOUSE:

                        if not l_pinched:

                            l_pinched = True
                            l_pinch_start = now

                        if (
                            not is_dragging
                            and (now - l_pinch_start) > 0.6
                        ):

                            print("[MOUSE] Drag Started")

                            pyautogui.mouseDown()

                            is_dragging = True

                        cv2.circle(
                            img,
                            (line_l[4], line_l[5]),
                            15,
                            (0, 255, 0),
                            cv2.FILLED
                        )

                        if is_dragging:

                            cv2.putText(
                                img,
                                "DRAGGING",
                                (w - 200, 170),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (0, 255, 0),
                                2
                            )

                    else:

                        if l_pinched:

                            if is_dragging:

                                print("[MOUSE] Drop (MouseUp)")

                                pyautogui.mouseUp()

                                is_dragging = False

                            else:

                                if (
                                    now - last_click_time
                                ) < 0.4:

                                    print("[MOUSE] Double Click")

                                    pyautogui.click(
                                        clicks=2,
                                        interval=0.1
                                    )

                                    cv2.circle(
                                        img,
                                        (x1, y1),
                                        40,
                                        (255, 255, 0),
                                        3
                                    )

                                else:

                                    print("[MOUSE] Left Click")

                                    pyautogui.mouseDown()
                                    time.sleep(0.12)
                                    pyautogui.mouseUp()

                                    cv2.circle(
                                        img,
                                        (x1, y1),
                                        30,
                                        (0, 255, 0),
                                        3
                                    )

                                last_click_time = now

                            l_pinched = False

                    if len_r < CLICK_THRESH_MOUSE:

                        if not r_pinched:

                            r_pinched = True

                        cv2.circle(
                            img,
                            (line_r[4], line_r[5]),
                            15,
                            (0, 0, 255),
                            cv2.FILLED
                        )

                    else:

                        if r_pinched:

                            print("[MOUSE] Right Click")

                            pyautogui.mouseDown(button='right')
                            time.sleep(0.12)
                            pyautogui.mouseUp(button='right')

                            cv2.circle(
                                img,
                                (x1, y1),
                                30,
                                (0, 0, 255),
                                3
                            )

                            r_pinched = False

                    cv2.putText(
                        img,
                        "MOUSE MODE",
                        (w - 200, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 0, 255),
                        2
                    )

            cv2.putText(
                img,
                "M=Menu  Q=Quit",
                (20, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (200, 200, 200),
                1
            )

        cv2.imshow(
            "Hand Gesture App",
            img
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            return 'quit'

        elif key == ord('m'):
            return 'menu'

    return 'quit'


def main():

    cap = cv2.VideoCapture(0)

    cap.set(3, CAM_W)
    cap.set(4, CAM_H)

    print("\n🖐 Hand Gesture App — Starting up...")

    if os.name == 'nt':

        print(
            "✅ Windows PyAutoGUI loaded — mouse control active"
        )

    else:

        print(
            "✅ macOS Quartz loaded — native zero-lag mouse control active"
        )

        print(
            "   (Note: If clicks don't register, "
            "macOS may still need Accessibility permission)"
        )

    print("")

    while True:

        result = mode_selection_screen(cap)

        if result == 'quit':
            break

        elif result == 'math':

            action = run_math_calculator(cap)

            if action == 'quit':
                break

        elif result == 'mouse':

            action = run_virtual_mouse(cap)

            if action == 'quit':
                break

        elif result == 'keyboard':

            action = run_virtual_keyboard(cap)

            if action == 'quit':
                break

    cap.release()

    cv2.destroyAllWindows()

    print(
        "\n✅ Hand Gesture App closed. Goodbye!"
    )


if __name__ == "__main__":
    main()
