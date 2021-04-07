import json
import time

from settings import REDIS_URL
from .storage import Redis

storage = Redis(url=REDIS_URL)


def split_psp_token(psp_token: str) -> tuple:
    token_type = None
    pay_error = None
    error_times = 0
    error_code = False
    error_delay = 0

    if len(psp_token) > 7:
        trigger = psp_token[0:3]
        try:
            token_type = ("ERR", "REQ").index(trigger)
        except ValueError:
            token_type = None

    unique_token = psp_token
    items = [""]
    if token_type == 0:
        items = psp_token[3:].split('_', 1)
        error_code = items[1]
        pay_error = 1
    elif token_type == 1:
        items = psp_token[3:].split('_', 6)
        error_code = items[1]
        if error_code.isdigit():
            error_code = int(error_code)
        pay_error = int(items[2])
        error_times = int(items[3])
        error_delay = int(items[4])
        unique_token = items[5]

    return pay_error, token_type, error_times, error_code, error_delay, unique_token, items[0]


def check_token(action_code: str, psp_token: str) -> tuple:
    """
    The action_code passed in must match the code in the token to activate the check, otherwise standard response is
    returned.

    For Error simulation (ERR & REQ):

        ERR prefix will error and return a given error code:
            e.g. ERR{code}_#1
            where {code} is a string such as ADD (see codes below) and #1 is the returned payment error string if
            applicable

        REQ code is used to simulate repeated and delayed requests:
            REQ{code}_#1_#2_#3_unique string
            #1 = error code may be HTTP error or Payment error code see #2
            #2 = set to 0 for HTTP error or 1 for Payment error code
            #3 = number of times the instruction will be applied when action code matches. Must be >0 to work
            #4 = Delay in seconds before responding when action code matches and before number of times is reached
            #5 = Unique part of token - must be changed on each request using same code to ensure a reset of times
            counter

        If token does not start with ERR or REQ or if the action code does not match or if number of times exceeded
        the token behaves as normal.
        Only the unique part is checked so the instruction part can be changed. This allows the token to be changed
        to test various failure scenarios eg with an action code of DEL the failure will occur only when deleting

        Examples where RET code is used to define an error during retain:

            Fail retain next 4 times requests will return normal error after 0 seconds and on 5th and subsequent pass
             normally (special case with retain is that there is no pay _error so xxx will never be used) - with this
             error the calling code will not retry:
                REQRET_xxx_1_4_0_uniqueString

                could have used to same effect because default error is 404:
                REQRET_404_0_4_0_uniqueString

            Fail retain next 4 times requests will return 500 after 0 seconds and on 5th and subsequent pass normally:
                REQRET_500_0_4_0_uniqueString

            Fail retain next 2 times returning 504 after 20 seconds and on 3rd and subsequent pass normally:
                REQRET_504_0_2_20_uniqueString

            Succeed retain without retry returning 200 after 10s delay:
                REQRET_200_0_1_10_uniqueString

            Fail ADD and return payment error code RTMENRE0003 next 4 times with a delay of 2s then pass normally
                REQADD_RTMENRE0003_1_4_2_uniqueString

            Fail ADD and return http error code 404 next 4 times with a delay of 2s then pass normally.
                REQADD_404_0_4_2_uniqueString

    For persistence:

        PER prefix will simulate persistence in Redis, allowing Pelops to store the results of some calls (such as ADD
        and DEL) in a cache for testing purposes:
            e.g. PER_uniqueString

        Codes are:

        RET  - Retain Spreedly request
        ADD  - Add/Enrol Spreedly request
        DEL  - Delete/Unenrol Spreedly (AMEX or MasterCard) or VOP request
        ACT  - Activation VOP request
        DEACT - De-Activation VOP request

    :param action_code:  one of 'RET', 'ADD', 'DEL', 'ACT', 'DEACT' to determine when action matches token code
    :param psp_token:    psp token ie payment token retained by Spreedly
    :return: tuple ( ErrorActive:bool , Pay_error:bool, error_code: string, unique_token_part:string)
    """

    pay_error, token_type, error_times, error_code, error_delay, unique_token, token_action = split_psp_token(psp_token)

    if token_action != action_code:
        return False, pay_error, error_code, unique_token

    if token_type == 0:
        return True, pay_error, error_code, unique_token

    key = f"repeat_{unique_token}"

    try:
        last_try = json.loads(storage.get(key))
        if last_try.get('code') != action_code:
            raise storage.NotFound
    except (json.JSONDecodeError, storage.NotFound):
        last_try = {'code': action_code, 'repeats': error_times}
        storage.set_expire(key, json.dumps(last_try))

    if last_try.get('repeats') > 0:
        if error_delay:
            time.sleep(error_delay)
        last_try['repeats'] -= 1
        storage.set_expire(key, json.dumps(last_try))
        if pay_error == 0 and 200 <= error_code <= 299:
            return False, pay_error, error_code, unique_token
        return True, pay_error, error_code, unique_token
    else:
        storage.delete(key)
        return False, pay_error, error_code, unique_token
