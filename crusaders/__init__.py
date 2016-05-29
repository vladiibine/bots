from __future__ import print_function

from datetime import datetime
import sys
import time

from autopy import mouse
from autopy import screen
from autopy import key

p0_click_monsters = (1352, 407)
p1_level_crusaders = (1440, 747)
p2_confirm_upgrade = (870, 485)
p3_buy_upgrades = (1441, 651)
p4_next_page = (1443, 704)
p5_reset_upgrade = (1276, 770)
p5a_reset_upgrade_while_on_mission = (1130, 776)
p6_confirm_reset_1 = (872, 641)
p7_blow_up_world_buttom = (969, 653)
p8_continue_to_mission_screen = (974, 666)
p9_free_play_during_event = (992, 505)
p10_gardeners_free_play = (997, 313)
p11_free_play_outside_event = (994, 351)
p12_start_mission = (1240, 676)
p13_next_level_check_pos = (1381, 333)
                                      
p14_browser_refresh = (880, 71)
p15_js_console = (937, 891)
p16_close_feedback_div = (1273, 166)
p17_close_chat = (1567, 131)
p18_start_flash_app = (958, 653)

js_setup = """\
var children = Array.from($('#content-canvas').children()); 
/* Remove the commercials at the top */
for(let child of children){
    if(['DIV', 'SECTION'].indexOf(child.tagName) !== -1 && child.id !== 'gamearea'){
        child.remove()
    }
    if (child.id === 'gamearea'){
        break;
    }
}
"""

special_chars = """\
~!@#$%^&*()_+{}:\"<>?"""

next_level_check_colors = {           
 '0xb9a363',                          
 '0xb9a566',                          
 '0xbaa465',                          
 '0xbaa566',                          
 '0xbaa567',                          
 '0xbaa76a',                          
 '0xbba76a',                          
 '0xbba86b',                          
 '0xbca86c',                          
 '0xbca96c',                          
 '0xbcaa6d',                          
 '0xbdaa6e',                          
 '0xbdab6f'}                          


class Game(object):
    def get_bot_class(self):
        return Bot

    def __init__(self, offset_x=0, offset_y=0, play_seconds=5100):
        """
        :param bool skip_initial: whether to skip the initial sequence
        :param bool skip_main: whether to skip the main sequence
        :param bool normal_campaing: try to play the normal campaign
        :param bool event_ongoing: if there currently an ongoing event?
        :param int skip_seconds: from the main sequence, skip this many seconds
        :param int play_seconds: play the main sequence for this many seconds
        :param int offset_x: number of pixels by which to offset the bot on OX
        :param int offset_y: number of pixel by which to offset the bot on OY
        """
        self.bot = self.get_bot_class()(offset_x, offset_y)
        self.play_seconds = play_seconds

    def run_forever(self, skip_initial=False, skip_main=False, 
            normal_campaign=True, event_ongoing=True, skip_seconds=0,
            skip_areas=0, expected_max_area=150):
        """plays forever
        :param int skip_levels: the current area... will run the main sequence
            *almost* as if startign from that area.
        :param int expected_max_level: the level at which the reset sequence
            usually starts.... so like 150 or something
        """
        skip_seconds += (skip_areas*1.0) / expected_max_area * self.play_seconds

        t1 = None
        try:
            while True:
                if not skip_initial:
                    self.initial_sequence()
                else:
                    skip_initial = False
                
                if not skip_main:
                    t1 = int(time.time())
                    print("Started main sequence at {}".format(str(datetime.now())))
                    while int(time.time()) - t1 < self.play_seconds - skip_seconds:
                        try:
                            self.main_sequence(
                                    t_init=t1, 
                                    play_for=self.play_seconds - skip_seconds)
                        except KeyboardInterrupt:
                            print("Interrupted, but taking a pause only")
                            print("Hit Ctrl+C again, to quit, or return, to continue")
                            _ = raw_input('')
                    skip_seconds = 0
                else:
                    skip_main = False

                print("Started to reset at {}".format(str(datetime.now())))
                self.reset_world(normal_campaign, event_ongoing)
        except KeyboardInterrupt:
            if t1 is not None:
                t2 = int(time.time())
                print("Interrupted. Played for {}. Remaining {}"
                        .format(t2-t1, self.play_seconds-skip_seconds - (t2 - t1)))

    def main_sequence(self, bot=None, forever=False, t_init=None, play_for=None):
        """This buys levels and upgrades"""
        bot = bot or self.bot

        def format_time(seconds):
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            leftover_seconds = (seconds % 60)
            return "{hours}:{minutes}:{seconds}".format(
                    hours=hours,
                    minutes=minutes,
                    seconds=leftover_seconds)


        def report(t_init=t_init, play_for=play_for):
            seconds_played = int(time.time()) - t_init
            seconds_to_play = play_for-int(time.time()) + t_init 

            bot.report( "\r" + 
                    "Played for {} (raw {} secs). Remaining {} (raw {} secs)"
                    .format(
                            format_time(seconds_played), 
                            seconds_played,
                            format_time(seconds_to_play),
                            seconds_to_play)
                    )
            sys.stdout.flush()

        def run_sequence(report_callback=report):
            bot.click_and_wait(p1_level_crusaders, 0, smooth=False)
            
            bot.tap('g')  # toggle auto-progress anyway
            for _ in range(4):
                self.sweep_items(4)
                bot.tap('g')
                report_callback()
            bot.click_and_wait(p3_buy_upgrades, 0, smooth=False)
            bot.tap('g')
            for _ in range(4):
                self.sweep_items(4)
                bot.tap('g')
                report_callback()

        if forever:
            while True:
                run_sequence()
        else:
            run_sequence()

    def reset_world(self, normal_campaign, event_ongoing, bot=None):
        """This resets the world, after a certain amount of time

        @param bool `normal_campaign`: if true, farms the normal campaign,
            otherwise the event's free play
        @param bool event_ongoing: if true, it means theres an event going on 
            currently
        """
        bot = bot or self.bot

        bot.repeat_action(p4_next_page, 40, 1)
        bot.repeat_action(p5_reset_upgrade, 5, 2)
        bot.repeat_action(p5a_reset_upgrade_while_on_mission, 5, 2)
        bot.repeat_action(p5_reset_upgrade, 5, 2)
        bot.repeat_action(p5a_reset_upgrade_while_on_mission, 5, 2)
        bot.repeat_action(p6_confirm_reset_1, 3, 3)
        bot.repeat_action(p7_blow_up_world_buttom, 3, 1)
        bot.repeat_action(p8_continue_to_mission_screen, 2, 10)

        if not normal_campaign:
            bot.repeat_action(p10_gardeners_free_play, 2, 5)
            bot.repeat_action(p12_start_mission, 2, 1)
            bot.repeat_action(p10_gardeners_free_play, 2, 5)
            bot.repeat_action(p12_start_mission, 2, 1)
        elif event_ongoing:
            bot.repeat_action(p9_free_play_during_event, 1, 2)
            bot.repeat_action(p12_start_mission, 1, 2)
            bot.repeat_action(p9_free_play_during_event, 1, 2)
            bot.repeat_action(p12_start_mission, 1, 2)
        else:
            bot.repeat_action(p11_free_play_outside_event, 1, 2)
            bot.repeat_action(p12_start_mission, 1, 2)
            bot.repeat_action(p11_free_play_outside_event, 1, 2)
            bot.repeat_action(p12_start_mission, 1, 2)

    def initial_sequence(self, bot=None):
        """Starts to click, in order to kill the first monsters, and get some gold
        """
        bot = bot or self.bot
        for _ in range(30):
            bot.repeat_action(p2_confirm_upgrade, 10, 0.3)
            bot.tap('g')  # toggle auto-progress anyway
            bot.repeat_action(p1_level_crusaders, 3, 1)
            bot.tap('g')  # toggle auto-progress anyway
            bot.repeat_action(p2_confirm_upgrade, 1, 1)
            bot.tap('g')  # toggle auto-progress anyway

    def sweep_items(self, wait=0):
        self.bot.click_and_wait(p0_click_monsters, wait/2.0, click=False)
        self.bot.click_and_wait(p2_confirm_upgrade, wait/2.0, click=False)


class Bot(object):
    def __init__(self, offset_x=0, offset_y=0):
        self.offset_x = offset_x
        self.offset_y = offset_y

    def restart_browser(self, refresh=True, start_game=True, feedback=False):
        """restarts the browser and sets the game window to be where expected"""
        if refresh:
            self.click_and_wait(p14_browser_refresh, 20)
        else:
            self.click_and_wait()
        self.tap(key.K_F12)
        self.sleep(4)
        self.click_and_wait(p15_js_console, 3)
        for char in ' '.join(js_setup.splitlines()):
            if char in special_chars:
                self.tap(char, key.K_SHIFT)
            else:
                self.tap(char)
                time.sleep(0.1)
        self.sleep(2)
        self.tap(key.K_RETURN)
        self.sleep(3)
        self.tap(key.K_F12)
        if feedback:
            self.click_and_wait(p16_close_feedback_div, 2)
        self.click_and_wait(p17_close_chat, 2)
        if start_game:
            self.click_and_wait(p18_start_flash_app, 20)

    def sleep(self, seconds):
        """I'll use this for reportin how much time i'm waiting i guess"""
        # Divide seconds into N x 1 second intervals + 1 0.X interval
        whole_seconds = int(seconds)
        remaining_seconds = seconds - whole_seconds
        for _ in range(whole_seconds):
            time.sleep(1)
            #then report...somehow
        time.sleep(remaining_seconds)

    def report(self, text):
        import sys
        sys.stdout.flush()
        print('\r' + text, end="")

    def tap(self, key_to_tap, *modifiers):
        """Wraps autopy.key.tap, for reporting reporting"""
        if self._is_mouse_on_the_right():
            key.tap(key_to_tap, *modifiers)

    def _is_mouse_on_the_right(self):
        screen_resolution_x = screen.get_size()[0]
        mouse_pos_x = mouse.get_pos()[0]

        return mouse_pos_x >= screen_resolution_x / 2

    def click_and_wait(self, position=None, seconds=0, click=True, smooth=True):
        """Go to `position`, click and wait a number of `seconds`.

        Extra: only move and click if the mouse is on the right of the screen!!!
        """
        move_func = mouse.smooth_move if smooth else mouse.move

        if self._is_mouse_on_the_right():
            if position:
                move_func(
                        position[0]+self.offset_x, position[1]+self.offset_y)
            if click:
                mouse.click()

        self.sleep(seconds)

    def repeat_action(self, positions, times, wait):
        def is_single_position(position):
            if not isinstance(position, (tuple, list)):
                return False
            if not len(position) == 2:
                return False
            if not set((type(pos) for pos in position)) == {int}:
                return False
            return True


        for _ in range(times):
            if is_single_position(positions):
                self.click_and_wait(positions, wait)
            else:
                for position in positions:
                    self.click_and_wait(position, float(wait)/len(positions))
