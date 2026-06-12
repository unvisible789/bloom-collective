#!/usr/bin/env python3
"""
Bloom Collective - GUIControlCell

Initial version for mouse and keyboard control using pyautogui.
This is a starting point and should be used with caution.
"""

import time
from typing import Any, Dict, List, Optional

try:
    import pyautogui
except ImportError:
    pyautogui = None

try:
    from base_cell import BaseCell
    from epigenetic_state import EpigeneticState
except ImportError:
    BaseCell = object
    EpigeneticState = None


class GUIControlCell(BaseCell):
    """
    Cell for controlling mouse and keyboard.
    Safety is very important here.
    """

    def __init__(self, epigenetic: Optional[EpigeneticState] = None, fail_safe: bool = True):
        super().__init__(name="GUIControlCell", epigenetic=epigenetic)
        self.fail_safe = fail_safe

        if pyautogui:
            pyautogui.FAILSAFE = fail_safe
            pyautogui.PAUSE = 0.3  # Small pause between actions for safety

        self._internal_state = {
            "actions_performed": 0,
            "last_action": None,
        }

    @property
    def supported_tasks(self) -> List[str]:
        return ["gui", "mouse", "keyboard", "click", "type", "move", "screenshot"]

    def is_safe_to_act(self) -> bool:
        # Basic safety check - can be expanded later
        return True

    def move_mouse(self, x: int, y: int) -> Dict[str, Any]:
        if not pyautogui:
            return {"status": "error", "reason": "pyautogui not installed"}

        if not self.is_safe_to_act():
            return {"status": "blocked", "reason": "Safety check failed"}

        try:
            pyautogui.moveTo(x, y, duration=0.2)
            self._internal_state["actions_performed"] += 1
            self._internal_state["last_action"] = f"move_mouse({x}, {y})"
            return {"status": "success", "action": "move_mouse", "x": x, "y": y}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def click(self, button: str = "left") -> Dict[str, Any]:
        if not pyautogui:
            return {"status": "error", "reason": "pyautogui not installed"}

        if not self.is_safe_to_act():
            return {"status": "blocked", "reason": "Safety check failed"}

        try:
            pyautogui.click(button=button)
            self._internal_state["actions_performed"] += 1
            self._internal_state["last_action"] = f"click({button})"
            return {"status": "success", "action": "click", "button": button}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def type_text(self, text: str, interval: float = 0.05) -> Dict[str, Any]:
        if not pyautogui:
            return {"status": "error", "reason": "pyautogui not installed"}

        if not self.is_safe_to_act():
            return {"status": "blocked", "reason": "Safety check failed"}

        try:
            pyautogui.write(text, interval=interval)
            self._internal_state["actions_performed"] += 1
            self._internal_state["last_action"] = f"type_text(len={len(text)})"
            return {"status": "success", "action": "type_text", "length": len(text)}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def press_key(self, key: str) -> Dict[str, Any]:
        if not pyautogui:
            return {"status": "error", "reason": "pyautogui not installed"}

        if not self.is_safe_to_act():
            return {"status": "blocked", "reason": "Safety check failed"}

        try:
            pyautogui.press(key)
            self._internal_state["actions_performed"] += 1
            self._internal_state["last_action"] = f"press_key({key})"
            return {"status": "success", "action": "press_key", "key": key}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def take_screenshot(self, filename: Optional[str] = None) -> Dict[str, Any]:
        if not pyautogui:
            return {"status": "error", "reason": "pyautogui not installed"}

        try:
            if filename is None:
                filename = f"screenshot_{int(time.time())}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            self._internal_state["actions_performed"] += 1
            self._internal_state["last_action"] = f"screenshot({filename})"
            return {
                "status": "success",
                "action": "screenshot",
                "filename": filename,
                "size": screenshot.size,
            }
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive", "message": "GUIControlCell is currently silenced."}

        action = input_data.get("action", "").lower()

        if action == "move":
            return self.move_mouse(input_data.get("x", 0), input_data.get("y", 0))
        elif action == "click":
            return self.click(input_data.get("button", "left"))
        elif action == "type":
            return self.type_text(input_data.get("text", ""))
        elif action == "press":
            return self.press_key(input_data.get("key", ""))
        elif action == "screenshot":
            return self.take_screenshot(input_data.get("filename"))
        else:
            return {"status": "error", "reason": f"Unknown action: {action}"}

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
