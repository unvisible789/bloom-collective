#!/usr/bin/env python3
"""
Bloom Collective - GUIControlCell

Mouse, keyboard, and screenshot control with basic safety.
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
    def __init__(self, epigenetic: Optional[EpigeneticState] = None):
        super().__init__(name="GUIControlCell", epigenetic=epigenetic)
        if pyautogui:
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.25

        self._internal_state = {
            "actions_performed": 0,
            "last_action": None,
        }

    @property
    def supported_tasks(self) -> List[str]:
        return ["gui", "mouse", "keyboard", "click", "type", "move", "screenshot"]

    def move_mouse(self, x: int, y: int) -> Dict[str, Any]:
        if not pyautogui:
            return {"status": "error", "reason": "pyautogui not available"}
        try:
            pyautogui.moveTo(x, y, duration=0.2)
            self._internal_state["actions_performed"] += 1
            self._internal_state["last_action"] = f"move({x},{y})"
            return {"status": "success", "x": x, "y": y}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def click(self, button: str = "left") -> Dict[str, Any]:
        if not pyautogui:
            return {"status": "error", "reason": "pyautogui not available"}
        try:
            pyautogui.click(button=button)
            self._internal_state["actions_performed"] += 1
            self._internal_state["last_action"] = f"click({button})"
            return {"status": "success", "button": button}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def type_text(self, text: str) -> Dict[str, Any]:
        if not pyautogui:
            return {"status": "error", "reason": "pyautogui not available"}
        try:
            pyautogui.write(text, interval=0.05)
            self._internal_state["actions_performed"] += 1
            self._internal_state["last_action"] = f"type(len={len(text)})"
            return {"status": "success", "length": len(text)}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def press_key(self, key: str) -> Dict[str, Any]:
        if not pyautogui:
            return {"status": "error", "reason": "pyautogui not available"}
        try:
            pyautogui.press(key)
            self._internal_state["actions_performed"] += 1
            self._internal_state["last_action"] = f"press({key})"
            return {"status": "success", "key": key}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def take_screenshot(self, filename: Optional[str] = None) -> Dict[str, Any]:
        if not pyautogui:
            return {"status": "error", "reason": "pyautogui not available"}
        try:
            if filename is None:
                filename = f"screenshot_{int(time.time())}.png"
            img = pyautogui.screenshot()
            img.save(filename)
            self._internal_state["actions_performed"] += 1
            self._internal_state["last_action"] = f"screenshot({filename})"
            return {"status": "success", "filename": filename, "size": img.size}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            return {"status": "inactive"}

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
            return {"status": "error", "reason": f"Unknown GUI action: {action}"}

    def get_state(self) -> Dict[str, Any]:
        base = super().get_state()
        base.update(self._internal_state)
        return base
