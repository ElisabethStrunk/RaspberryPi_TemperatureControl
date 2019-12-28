#!/usr/bin/env python3


def test_hysteresis():
    from hysteresis import check_level

    lower_boundary = 18
    upper_boundary = 24

    test_tuples = [(20, None),  # Current value within boundaries -> should return None
                   (15, 1),     # Current value under lower boundary -> should return 1
                   (27, 0),     # Current value over upper boundary -> should return 0
                   (18, 1),     # Current value equal to lower boundary -> should return 1
                   (24, 0)]     # Current value equal to upper boundary -> should return 0

    print("***** HYSTERESIS TEST *****")
    for value_pair in test_tuples:
        current_value = value_pair[0]
        result = check_level(current_value, lower_boundary, upper_boundary)
        if result is not value_pair[1]:
            print("Hysteresis Test failed!\n"
                  "Current value: {}\n"
                  "Lower boundary: {}\n"
                  "Upper boundary: {}\n"
                  "Expected result of check_level: {}\n"
                  "Result of check_level: {}\n"
                  .format(current_value, lower_boundary, upper_boundary, value_pair[1], result))

    print("Hysteresis Test finished.")


if __name__ == '__main__':
    test_hysteresis()
