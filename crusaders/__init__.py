from __future__ import print_function

from autopy import mouse
from autopy import screen
from autopy import key
import time
from datetime import datetime

p0_click_monsters = (1352, 407)
p1_level_crusaders = (1440, 747)
p2_confirm_upgrade = (870, 485)
p3_buy_upgrades = (1441, 651)
p4_next_page = (1443, 704)
p5_reset_upgrade = (1276, 770)
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
special_chars="""\
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



def run_forever(skip_initial=False, skip_main=False, normal_campaing=True, 
        event_ongoing=True, skip_seconds=0, play_seconds=5200):
    """plays forever
    
    :param bool skip_initial: whether to skip the initial sequence
    :param bool skip_main: whether to skip the main sequence
    :param bool normal_campaing: try to play the normal campaign
    :param bool event_ongoing: if there currently an ongoing event?
    :param int skip_seconds: from the main sequence, skip this many seconds
    :param int play_seconds: play the main sequence for this many seconds
    """
    t1 = None
    try:
        while True:
            if not skip_initial:
                initial_sequence()
            else:
                skip_initial = False
            
            if not skip_main:
                t1 = int(time.time())
                print("Started main sequence at {}".format(str(datetime.now())))
                while int(time.time()) - t1 < play_seconds - skip_seconds:
                    try:
                        main_sequence()
                    except KeyboardInterrupt:
                        print("Interrupted, but taking a pause only")
                        print("Hit Ctrl+C again, to quit, or return, to continue")
                        _ = raw_input('')
                skip_seconds = 0
            else:
                skip_main = False

            print("Started to reset at {}".format(str(datetime.now())))
            reset_world(normal_campaing, event_ongoing)
    except KeyboardInterrupt:
        if t1 is not None:
            t2 = int(time.time())
            print("Interrupted. Played for {}. Remaining {}"
                    .format(t2-t1, play_seconds-skip_seconds - (t2 - t1)))


def main_sequence():
    """This buys levels and upgrades"""
    click_and_wait(p1_level_crusaders, 2)
    click_and_wait(p2_confirm_upgrade, 2)  # it was a 22 sec wait
    for _ in range(5):
        sweep_items(4)
    click_and_wait(p3_buy_upgrades, 7)
    click_and_wait(p2_confirm_upgrade, 2)  # it was a 20 sec wait
    for _ in range(5):
        sweep_items(4)

def click_and_wait(position=None, seconds=0, click=True):
    """Go to `position`, click and wait a number of `seconds`.

    Extra: only move and click if the mouse is on the right of the screen!!!
    """
    screen_resolution_x = screen.get_size()[0]
    mouse_pos_x = mouse.get_pos()[0]
    
    if mouse_pos_x >= screen_resolution_x / 2:
        if position:
            mouse.smooth_move(*position)
        if click:
            mouse.click()

    sleep(seconds)


def repeat_action(positions, times, wait):
    def is_single_position(position):
        if not isinstance(position, (tuple, list)):
            return False
        if not len(position) == 2:
            return false
        if not set((type(pos) for pos in position)) == {int}:
            return False
        return True


    for _ in range(times):
        if is_single_position(positions):
            click_and_wait(positions, wait)
        else:
            for position in positions:
                click_and_wait(position, float(wait)/len(positions))


def reset_world(normal_campaign, event_ongoing):
    """This resets the world, after a certain amount of time

    @param bool `normal_campaign`: if true, farms the normal campaign, 
        otherwise the event's free play
    @param bool event_ongoing: if true, it means theres an event going on 
        currently
    """

    repeat_action(p4_next_page, 40, 1)
    
    repeat_action(p5_reset_upgrade, 10, 3)

    repeat_action(p6_confirm_reset_1, 3, 3)

    repeat_action(p7_blow_up_world_buttom, 3, 1)

    repeat_action(p8_continue_to_mission_screen, 2, 10)

    if not normal_campaign:
        repeat_action(p10_gardeners_free_play, 2, 5)
        repeat_action(p12_start_mission, 2, 1)
        repeat_action(p10_gardeners_free_play, 2, 5)
        repeat_action(p12_start_mission, 2, 1)
    elif event_ongoing:
        repeat_action(p9_free_play_during_event, 1, 2)
        repeat_action(p12_start_mission, 1, 2)
        repeat_action(p9_free_play_during_event, 1, 2)
        repeat_action(p12_start_mission, 1, 2)
    else:
        repeat_action(p11_free_play_outside_event, 1, 2)
        repeat_action(p12_start_mission, 1, 2)
        repeat_action(p11_free_play_outside_event, 1, 2)
        repeat_action(p12_start_mission, 1, 2)

def initial_sequence():
    """Starts to click, in order to kill the first monsters, and get some gold
    """
    for _ in range(30):
        repeat_action(p2_confirm_upgrade, 10, 0.3)
        repeat_action(p1_level_crusaders, 3, 1)
        repeat_action(p2_confirm_upgrade, 1, 1)
    
    
def restart_browser(refresh=True, start_game=True):
    """restarts the browser and sets the game window to be where expected"""
    if refresh:
        click_and_wait(p14_browser_refresh, 20)
    else:
        click_and_wait()
    tap(key.K_F12)
    sleep(4)
    click_and_wait(p15_js_console, 3)
    for char in ' '.join(js_setup.splitlines()):
        if char in special_chars:
            key.tap(char, key.K_SHIFT)
        else:
            key.tap(char)
    sleep(2)
    key.tap(key.K_RETURN)
    sleep(3)
    key.tap(key.K_F12)
    click_and_wait(p16_close_feedback_div, 2)
    click_and_wait(p17_close_chat, 2)
    if start_game:
        click_and_wait(p18_start_flash_app, 20)

def sleep(seconds):
    """I'll use this for reportin how much time i'm waiting i guess"""
    # Divide seconds into N x 1 second intervals + 1 0.X interval
    whole_seconds = int(seconds)
    remaining_seconds = seconds - whole_seconds
    for _ in range(whole_seconds):
        time.sleep(1)
        #then report...somehow
    time.sleep(remaining_seconds)

def report(text):
    import sys
    sys.stdout.flush()
    print('\r' + text, end="")

def tap(key_to_tap):
    """Wraps autopy.key.tap, for reporting reporting"""
    key.tap(key_to_tap)

def sweep_items(wait=0):
    click_and_wait(p0_click_monsters, wait/2.0, click=False)
    click_and_wait(p2_confirm_upgrade, wait/2.0, click=False)
