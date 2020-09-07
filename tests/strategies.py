import typing
from uuid import UUID

import hypothesis
from hypothesis import strategies
from src.packages.rescue import Rescue as _Rescue
from src.packages.rat import Rat as _Rat
from src.packages.utils import sanitize, Platforms as _Platforms
import string

# Anything that isn't a whitespace other than the space character, and isn't a control character.
valid_characters = strategies.characters(blacklist_categories=["C", "Zl", "Zp"])
"""
Any character (ASCII / UNICODE) that isn't a control character or whitespace other than ' '.
"""
# Filtered by anything that doesn't make it through the sanitizer.
valid_text = (
    strategies.text(valid_characters, min_size=10)
        .filter(lambda data: sanitize(data) == data)
        .filter(lambda data: data.isprintable())
)
""" 
Generates probably valid text.

Shrinks towards smaller words.
"""

valid_word_chars = strategies.characters(blacklist_categories=["C", "Z"])
"""
Characters that are valid to be in a word
"""

valid_word = strategies.text(valid_word_chars, min_size=1)
"""
a single word (no whitespace)

Shrinks towards smaller words. 
"""

valid_words = strategies.lists(valid_word, max_size=10)
""" 
a list of valid words

Shrinks towards smaller lists and smaller words.
"""
_irc_nick_letters = strategies.characters(
    whitelist_characters=f"{string.ascii_letters}{string.digits}" + r"\/_[]{}",
    whitelist_categories=())


@strategies.composite
def valid_irc_name(draw):
    names = strategies.text(alphabet=_irc_nick_letters, min_size=3).filter(
        lambda word: not word[0].isnumeric()).filter(
        lambda word: not word.startswith(('\\', '_', '[', ']', '{', '}', '/')))

    return draw(names)


platform = strategies.sampled_from([_Platforms.PS, _Platforms.PC, _Platforms.XB])
""" Some platform """
rescue = strategies.builds(
    _Rescue,
    uuid=strategies.uuids(version=4),  # generate some valid uuid4
    client=valid_irc_name(),  # client should always be defined
    # irc nickname may be any valid word, or None.
    irc_nickname=strategies.one_of(valid_irc_name(), strategies.none()),
    platform=platform,
    active=strategies.booleans(),
    code_red=strategies.booleans(),
    board_index=strategies.one_of(strategies.integers(min_value=1), strategies.none())
)
""" Strategy for generating a rescue. Shrinks towards smaller arguments """


def rescues(min_size: int, max_size: int):
    """ builds a list of rescues, shrinks towards smaller lists and smaller rescues """
    return strategies.lists(rescue, min_size=min_size, max_size=max_size,
                            unique_by=(
                                lambda case: case.irc_nickname, lambda case: case.board_index,
                                lambda case: case.client))


@strategies.composite
def rat(draw):
    """ Strategy for generating valid rat objects """
    uuids = strategies.uuids(version=4)
    name = valid_word
    platforms = strategies.one_of(strategies.none(), platform)
    return _Rat(
        uuid=draw(uuids),
        name=draw(valid_word),
        platform=draw(platform)
    )


rats = strategies.lists(rat())
""" a list of rats """


@strategies.composite
def rescue_number(draw):
    # Any version 4 UUID.
    uuids = strategies.uuids(version=4)
    # Either a space or a `#` character.
    leading_integer_literals = strategies.one_of(strategies.just("#"), strategies.just(" "))

    # Either a space or a `@` character.
    leading_uuid_literals = strategies.one_of(strategies.just("@"), strategies.just(" "))

    # Any positive number.
    numbers = strategies.integers(min_value=0)

    # Produce either a number or a UUID
    payload_mux = strategies.one_of(numbers, uuids)
    # Draw from the mux.
    raw_payload = draw(payload_mux)
    # If its a uuid, draw from the uuid prefix strategy as well and mash the two together.
    if isinstance(raw_payload, UUID):
        return f"{draw(leading_uuid_literals)}{raw_payload}".lstrip()

    # Otherwise draw from the integer prefix strategy.
    return f"{draw(leading_integer_literals)}{raw_payload}".lstrip()


@strategies.composite
def rescue_identifier(draw):
    numbers = rescue_number()
    names = valid_irc_name()
    identifier = strategies.one_of(numbers, names)

    return draw(identifier)
