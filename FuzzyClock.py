# MIT License

# Copyright (c) 2018 Sarthak Upadhyay

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sublime
import sublime_plugin
from datetime import datetime

TENS_DICT = [
    '', '', 'Twenty', 'Thirty', 'Fourty', 'Fifty', 'Sixty', 'Seventy',
    'Eighty', 'Ninety'
]

ONES_DICT = [
    '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'
]

TEENS = [
    'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen',
    'Seventeen', 'Eighteen', 'Nineteen'
]


def n2a(number):
    if number == 0:
        return 'zero'
    elif number < 10:
        return ONES_DICT[number % 10]
    elif number < 20 and number > 9:
        return TEENS[number - 10]
    elif number % 10 == 0:
        return TENS_DICT[number // 10]
    else:
        return TENS_DICT[number // 10] + ' ' + ONES_DICT[number % 10]


def next(n):
    return 12 if n == 11 else n + 1


def fuzzyTime(hour, minutes):
    cond = ((minutes + 2) % 60) // 5
    if hour != 12:
        hour = hour % 12
    if hour == 0:
        hour = 12
    if minutes > 33:
        hour = next(hour)
    if cond == 0:
        return n2a(hour) + ' o\'clock'
    elif cond == 3:
        return 'Quarter' + ' past ' + n2a(hour)
    elif cond == 6:
        return 'Half' + ' past ' + n2a(hour)
    elif cond == 9:
        return 'Quarter' + ' to ' + n2a(hour)
    elif 0 < cond < 6:
        return n2a(cond * 5) + ' past ' + n2a(hour)
    else:
        return n2a(60 - cond * 5) + ' to ' + n2a(hour)


class FuzzyClock(sublime_plugin.EventListener):
    def on_activated(self, view):
        update_interval = 10000
        Timer().displayTime(view, update_interval)


class Timer():
    status_key = '___fuzzyclock'

    def displayTime(self, view, delay):
        time = datetime.now().timetuple()
        hour = time[3]
        minutes = time[4]
        view.set_status(self.status_key, fuzzyTime(hour, minutes))
        actwin = sublime.active_window()
        if actwin:
            if actwin.active_view() and actwin.active_view().id() == view.id():
                sublime.set_timeout(lambda:
                                    self.displayTime(view, delay),
                                    delay)
        else:
            view.set_status(self.status_key, '')
        return
