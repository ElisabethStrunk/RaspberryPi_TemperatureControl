#!/usr/bin/env python3


def check_level(current_value, lower_boundary, higher_boundary):
    if current_value <= lower_boundary:
        return 1
    if current_value >= higher_boundary:
        return 0
    else:
        return None
