import itertools

actions = {
    'Mouse control': [
        'Move mouse left',
        'Move mouse right',
        'Move mouse up',
        'Move mouse down',
        'Mouse left click',
        'Mouse right click',
        'Mouse double click',
        'Mouse movement wildcard'
    ],
    'Keyboard actions': [
        'Space',
        'Enter',
        'Backspace',
        'Escape'
    ],
    'App commands': [
        'Quit',
        'Mode'
    ],
    'Navigation control': [
        'Up arrow',
        'Down arrow',
        'Left arrow',
        'Right arrow'
    ],
    'Typing': [
        'Type 0',
        'Type 1',
        'Type a b c 2',
        'Type d e f 3',
        'Type g h i 4',
        'Type j k l 5',
        'Type m n o 6',
        'Type p q r s 7',
        'Type t u v 8',
        'Type w x y z 9'
    ],
}

def combine_actions(actions):
    """
    Provide list of lists and this method returns the flattened
    list.
    """
    return list(itertools.chain.from_iterable(actions))