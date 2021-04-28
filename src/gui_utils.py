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

import pygame
pygame.init()


def kmod(key, target_key, ctrl=False, shift=False, alt=False):
    keys = pygame.key.get_pressed()
    ctrl_pressed = (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL])
    shift_pressed = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
    alt_pressed = (keys[pygame.K_LALT] or keys[pygame.K_RALT])

    meets_requires = True
    if ctrl != ctrl_pressed:
        meets_requires = False
    if shift != shift_pressed:
        meets_requires = False
    if alt != alt_pressed:
        meets_requires = False

    if meets_requires and key == target_key:
        return True
    return False
