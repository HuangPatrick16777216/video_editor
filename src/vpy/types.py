#
#  Pymixer
#  Video editor with a Python API.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import time
import numpy as np
from typing import Any, Dict, List, Tuple
from datetime import datetime


# Class "declaration" needed for type hinting.
class Scene: pass
class Context: pass
class Data: pass

class Tab: pass
class Area: pass
class Layout: pass

class Operator: pass
class OpCollection: pass
class OpsModule: pass

class Property: pass
class BoolProp: pass
class IntProp: pass
class FloatProp: pass
class StringProp: pass
class EnumProp: pass
class PropertyGroup: pass
class PropCollection: pass


class Scene:
    """
    Scene class. This is saved and loaded from the project file.
    """

    meta: bytes
    time: float
    date: bytes
    is_saved: bool
    is_dirty: bool

    def __init__(self) -> None:
        self.meta = b""
        self.time = time.time()
        self.date = datetime.now().strftime("%Y-%m-%d %H-%M-%S").encode()
        self.is_saved = False
        self.is_dirty = False

    def __getattr__(self, attr: str) -> PropCollection:
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise AttributeError(f"Scene has no attribute {attr}")

class Context:
    """
    Context containing current info in GUI, such as current loaded scene.
    Will be initialized and updated by GUI.
    """

    scene: Scene
    render_result: np.ndarray
    num_changes: int

    last_report: Tuple[str]
    last_report_time: int

    def __init__(self) -> None:
        self.scene = None
        self.render_result = None
        self.num_changes = 0

        self.last_report = None
        self.last_report_time = 0

class Data:
    """
    Stores data information, like keyboard shortcuts.
    """

    # key: lowest 8 bits = ascii of kboard letter, next bits = shift, alt, ctrl
    # value: idname of operator
    kboard_shortcuts: Dict[int, str]

    def __init__(self):
        self.kboard_shortcuts = {}


class Operator:
    """
    Operator class. Displayed as a button in the GUI.
    To create an operator, create a new class that inherits from this.
    Then, you can define your own execute method, which will be run when the operator is called.
    """

    label: str
    description: str
    idname: str

    min_args: int = None
    max_args: int = None
    kwargs_include: Tuple[str] = ()
    kwargs_exclude: Tuple[str] = ()

    # Tuple of (letter, shift, alt, ctrl)
    kboard_shortcuts: Tuple[Tuple[str, bool, bool, bool]] = ()

    def __call__(self, *args, **kwargs) -> str:
        """
        Passes vpy.context to all methods that need it.
        First checks poll(). If it is successfull, then run execute()
        """
        import vpy
        vpy.context.num_changes += 1

        if self.min_args is not None and len(args) < self.min_args:
            self.report("ERROR", f"Too few arguments in Operator {self.idname}")
            return "CANCELLED"
        if self.max_args is not None and len(args) > self.max_args:
            self.report("ERROR", f"Too many arguments in Operator {self.idname}")
            return "CANCELLED"
        for arg in self.kwargs_include:
            if arg not in kwargs:
                self.report("ERROR", f"Must include kwarg {arg} in Operator {self.idname}")
                return "CANCELLED"
        for arg in self.kwargs_exclude:
            if arg in kwargs:
                self.report("ERROR", f"Must exclude kwarg {arg} in Operator {self.idname}")
                return "CANCELLED"

        try:
            poll = self.poll(vpy.context, *args, **kwargs)
        except:
            poll = False

        if poll:
            val = self.execute(vpy.context, *args, **kwargs)
            if val not in ("FINISHED", "CANCELLED"):
                self.report("ERROR", f"Invalid return in Operator {self.idname} call.")
                return "FINISHED"
        else:
            self.report("ERROR", f"Poll in Operator {self.idname} failed.")
            return "CANCELLED"

    def report(self, type: str, msg: str) -> None:
        """
        Sends a message in the status bar.
        :param type: INFO, WARNING, or ERROR.
        :param msg: Message to send.
        """
        import vpy
        vpy.context.last_report = (type, msg)
        vpy.context.last_report_time = time.time()

    def poll(self, context: Context, *args, **kwargs) -> bool:
        """
        The operator should return a bool based on the scene,
        specifying whether requirements, if any, are met (eg scene.fps >= 30)
        :param context: Context during which the operator is executed.
        :param args: Any other arguments the operator needs.
        :param kwargs: Any other arguments the operator needs.
        """
        return True

    def execute(self, context: Context, *args, **kwargs) -> str:
        """
        This function is run when the operator is called,
        usually by the user pressing a button in the GUI.
        The return should be a dictionary, which must have a key "status" with a
            bool specifying whether this operator ran successfully.
            The dictionary may contain other values as well.
        :param context: Context during which the operator is executed.
        :param args: Any other arguments the operator needs.
        :param kwargs: Any other arguments the operator needs.
        """
        return "FINISHED"

class OpCollection:
    """
    A collection of operators, found in vpy.ops.my_collection
    Add operators by calling vpy.utils.register_class(MyOperatorClass)
    """

    operators: Dict[str, Operator]

    def __init__(self) -> None:
        self.operators = {}

    def __getattr__(self, attr) -> Operator:
        if attr in self.operators:
            return self.operators[attr]
        else:
            raise AttributeError(f"OpCollection has no attribute {attr}")

class OpsModule:
    """
    The vpy.ops module.
    Operator collections are automatically added from vpy.utils.register_class()
    """

    colls: Dict[str, OpCollection]

    def __init__(self) -> None:
        self.colls = {}

    def __getattr__(self, attr) -> OpCollection:
        if attr in self.colls:
            return self.colls[attr]
        else:
            raise AttributeError(f"OpsModule has no attribute {attr}")


class Tab:
    idname: str
    label: str

    icon_path: str
    icon: np.ndarray

    def __init__(self) -> None:
        self.icon_path = ""
        self.icon = None

class Area:
    # TODO drawing and layout
    idname: str
    parent_idname: str
    tab_id: str
    label: str

    layout: Layout

    def __init__(self) -> None:
        pass

    def draw(self, context: Context) -> None:
        pass

class Layout:
    def __init__(self) -> None:
        pass

    def label(self, text: str) -> None:
        pass

    def prop(self, group: PropCollection, idname: str) -> None:
        pass

    def operator(self, idname: str, args: Tuple[Any], kwargs: Dict[str, Any]) -> None:
        pass


class Property:
    """
    Base property class. BoolProp, IntProp, ... extend off of this.
    """

    name: str
    description: str

    type: type
    default: type
    value: type

    def get(self) -> type:
        return self.value

    def set(self, value: type) -> None:
        self.value = value

class BoolProp(Property):
    """
    Boolean property.
    """

    type = bool

    def __init__(self, name: str = "", description: str = "", default: type = False) -> None:
        self.name = name
        self.description = description
        self.default = default

        self.value = default

class IntProp(Property):
    """
    Integer property.
    """

    type = int
    min: type
    max: type

    def __init__(self, name: str = "", description: str = "", default: type = 0, min: type = None, max: type = None) -> None:
        self.name = name
        self.description = description
        self.default = default
        self.min = float("-inf") if min is None else min
        self.max = float("inf") if max is None else max

        self.value = default

    def set(self, value: type) -> None:
        if value < self.min:
            value = self.min
        if value > self.max:
            value = self.max
        self.value = value

class FloatProp(Property):
    """
    Float property.
    """

    type = float
    min: type
    max: type

    def __init__(self, name: str = "", description: str = "", default: type = 0, min: type = None, max: type = None) -> None:
        self.name = name
        self.description = description
        self.default = default
        self.min = float("-inf") if min is None else min
        self.max = float("inf") if max is None else max

        self.value = default

    def set(self, value: type) -> None:
        if value < self.min:
            value = self.min
        if value > self.max:
            value = self.max
        self.value = value

class StringProp(Property):
    """
    String property.
    """

    type = str

    def __init__(self, name: str = "", description: str = "", default: type = 0) -> None:
        self.name = name
        self.description = description
        self.default = default

        self.value = default

class EnumProp(Property):
    """
    Enumerate property.
    """

    type = Tuple
    items: Tuple[Tuple[str]]
    idx: int

    def __init__(self, name: str = "", description: str = "", items: Tuple[Tuple[str]] = ()) -> None:
        self.name = name
        self.description = description
        self.items = items
        self.idx = 0

    def get(self) -> str:
        return self.items[self.idx][0]

    def set(self, idx: int) -> None:
        self.idx = min(idx, len(self.items)-1)

class PropertyGroup:
    """
    Group of props.
    Inherit from this and register when adding a property collection to Scene.
    """

    idname: str

class PropCollection:
    """
    Collection of properties, which will be added to Scene when a PropertyGroup is registered.
    Decorators for getting and setting are added at register.
    """

    _values: Dict[str, Property]

    def __init__(self) -> None:
        self._values = {}

    def __getattr__(self, attr: str) -> Property:
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise AttributeError(f"PropCollection has no attribute {attr}")
