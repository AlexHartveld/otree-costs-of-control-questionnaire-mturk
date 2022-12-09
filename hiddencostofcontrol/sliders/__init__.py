import time
import json

from otree import settings
from otree.api import *

from .image_utils import encode_image
from . import task_sliders

doc = """
A two-stage principal-agent game is played with only one round. There is no context given, the game is framed in a neutral manner. X represents some productive activity and is costly to the agent 
(c(x) = x) but benefits the principal (πp = 2x). The profit function of the agent is πa = 120 – x.
The principal can either leave the choice of x to the agent or set a minimum level (x > 0), thereby re-stricting the choice set representing the level of control in this experiment design.
"""

class C(BaseConstants):
    NAME_IN_URL = "sliders"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = "sliders/instructions.html"
    ENDOWMENT_AGENT = cu(120) #Agents endowment
    ENDOWMENT_PRINCIPAL = cu(0) #Principals endowment

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    session = subsession.session
    defaults = dict(
        trial_delay=1.0,
        retry_delay=0.1,
        num_sliders=60,
        num_columns=3,
        attempts_per_slider=1
    )
    session.params = {}
    for param in defaults:
        session.params[param] = session.config.get(param, defaults[param])

    control = [5, 10, 20]
    for player in subsession.get_players():
        player.control = control[player.group.id % 3]


class Group(BaseGroup):
    minimum_amount = models.StringField(
        choices=['Yes', 'No'],
        widget=widgets.RadioSelectHorizontal
    )
    chosen_effort = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(0), max=cu(120))
    chosen_effort_min5 = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(5), max=cu(120))
    chosen_effort_min10 = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(10), max=cu(120))
    chosen_effort_min20 = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(20), max=cu(120))


class Player(BasePlayer):
    # only suported 1 iteration for now
    iteration = models.IntegerField(initial=0)

    num_correct = models.IntegerField(initial=0)
    elapsed_time = models.FloatField(initial=0)

    control = models.IntegerField() 


# FUNCTIONS
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    # check which chosen_effort has a value
    chosen_effort_control = None
    if group.field_maybe_none('chosen_effort_min5') is not None: 
        chosen_effort_control = group.chosen_effort_min5
    elif group.field_maybe_none('chosen_effort_min10') is not None: 
        chosen_effort_control = group.chosen_effort_min10
    elif group.field_maybe_none('chosen_effort_min20') is not None: 
        chosen_effort_control = group.chosen_effort_min20
    
    # check if p1 chose set minimum amount or not
    if group.minimum_amount == "No":
        p1.payoff = 2 * group.chosen_effort
        p2.payoff = C.ENDOWMENT_AGENT - group.chosen_effort
    else:
        p1.payoff = 2 * chosen_effort_control
        p2.payoff = C.ENDOWMENT_AGENT - chosen_effort_control

# puzzle-specific stuff
class Puzzle(ExtraModel):
    """A model to keep record of sliders setup"""

    player = models.Link(Player)
    iteration = models.IntegerField()
    timestamp = models.FloatField()

    num_sliders = models.IntegerField()
    layout = models.LongStringField()

    response_timestamp = models.FloatField()
    num_correct = models.IntegerField(initial=0)
    is_solved = models.BooleanField(initial=False)


class Slider(ExtraModel):
    """A model to keep record of each slider"""

    puzzle = models.Link(Puzzle)
    idx = models.IntegerField()
    target = models.IntegerField()
    value = models.IntegerField()
    is_correct = models.BooleanField(initial=False)
    attempts = models.IntegerField(initial=0)


def generate_puzzle(player: Player) -> Puzzle:
    """Create new puzzle for a player"""
    params = player.session.params
    num = params['num_sliders']
    layout = task_sliders.generate_layout(params)
    puzzle = Puzzle.create(
        player=player, iteration=player.iteration, timestamp=time.time(),
        num_sliders=num,
        layout=json.dumps(layout)
    )
    for i in range(num):
        target, initial = task_sliders.generate_slider()
        Slider.create(
            puzzle=puzzle,
            idx=i,
            target=target,
            value=initial
        )
    return puzzle


def get_current_puzzle(player):
    puzzles = Puzzle.filter(player=player, iteration=player.iteration)
    if puzzles:
        [puzzle] = puzzles
        return puzzle


def get_slider(puzzle, idx):
    sliders = Slider.filter(puzzle=puzzle, idx=idx)
    if sliders:
        [puzzle] = sliders
        return puzzle


def encode_puzzle(puzzle: Puzzle):
    """Create data describing puzzle to send to client"""
    layout = json.loads(puzzle.layout)
    sliders = Slider.filter(puzzle=puzzle)
    # generate image for the puzzle
    image = task_sliders.render_image(layout, targets=[s.target for s in sliders])
    return dict(
        image=encode_image(image),
        size=layout['size'],
        grid=layout['grid'],
        sliders={s.idx: {'value': s.value, 'is_correct': s.is_correct} for s in sliders}
    )


def get_progress(player: Player):
    """Return current player progress"""
    return dict(
        iteration=player.iteration,
        solved=player.num_correct
    )


def handle_response(puzzle, slider, value):
    slider.value = task_sliders.snap_value(value, slider.target)
    slider.is_correct = slider.value == slider.target
    puzzle.num_correct = len(Slider.filter(puzzle=puzzle, is_correct=True))
    puzzle.is_solved = puzzle.num_correct == puzzle.num_sliders


def play_game(player: Player, message: dict):
    """Main game workflow
    Implemented as reactive scheme: receive message from browser, react, respond.

    Generic game workflow, from server point of view:
    - receive: {'type': 'load'} -- empty message means page loaded
    - check if it's game start or page refresh midgame
    - respond: {'type': 'status', 'progress': ...}
    - respond: {'type': 'status', 'progress': ..., 'puzzle': data}
      in case of midgame page reload

    - receive: {'type': 'new'} -- request for a new puzzle
    - generate new sliders
    - respond: {'type': 'puzzle', 'puzzle': data}

    - receive: {'type': 'value', 'slider': ..., 'value': ...} -- submitted value of a slider
      - slider: the index of the slider
      - value: the value of slider in pixels
    - check if the answer is correct
    - respond: {'type': 'feedback', 'slider': ..., 'value': ..., 'is_correct': ..., 'is_completed': ...}
      - slider: the index of slider submitted
      - value: the value aligned to slider steps
      - is_corect: if submitted value is correct
      - is_completed: if all sliders are correct
    """
    session = player.session
    my_id = player.id_in_group
    params = session.params

    now = time.time()
    # the current puzzle or none
    puzzle = get_current_puzzle(player)

    message_type = message['type']

    if message_type == 'load':
        p = get_progress(player)
        if puzzle:
            return {my_id: dict(type='status', progress=p, puzzle=encode_puzzle(puzzle))}
        else:
            return {my_id: dict(type='status', progress=p)}

    if message_type == "new":
        if puzzle is not None:
            raise RuntimeError("trying to create 2nd puzzle")

        player.iteration += 1
        z = generate_puzzle(player)
        p = get_progress(player)

        return {my_id: dict(type='puzzle', puzzle=encode_puzzle(z), progress=p)}

    if message_type == "value":
        if puzzle is None:
            raise RuntimeError("missing puzzle")
        if puzzle.response_timestamp and now < puzzle.response_timestamp + params["retry_delay"]:
            raise RuntimeError("retrying too fast")

        slider = get_slider(puzzle, int(message["slider"]))

        if slider is None:
            raise RuntimeError("missing slider")
        if slider.attempts >= params['attempts_per_slider']:
            raise RuntimeError("too many slider motions")

        value = int(message["value"])
        handle_response(puzzle, slider, value)
        puzzle.response_timestamp = now
        slider.attempts += 1
        player.num_correct = puzzle.num_correct

        p = get_progress(player)
        return {
            my_id: dict(
                type='feedback',
                slider=slider.idx,
                value=slider.value,
                is_correct=slider.is_correct,
                is_completed=puzzle.is_solved,
                progress=p,
            )
        }

    if message_type == "cheat" and settings.DEBUG:
        return {my_id: dict(type='solution', solution={s.idx: s.target for s in Slider.filter(puzzle=puzzle)})}

    raise RuntimeError("unrecognized message from client")


# PAGES
class Introduction(Page):
    pass

class Send(Page):
    """This page is only for Principal. Can either trust the agent or not."""
    form_model = 'group'
    form_fields = ['minimum_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1

class SendBackWaitPage(WaitPage):
    pass

class SendBackC5(Page):
    """This page is only for Agent. Agent can decide on effort level x."""
    form_model = 'group'
    form_fields = ['chosen_effort', 'chosen_effort_min5']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2 and player.control == 5

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

class SendBackC10(Page):
    """This page is only for Agent. Agent can decide on effort level x."""
    form_model = 'group'
    form_fields = ['chosen_effort', 'chosen_effort_min10']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2 and player.control == 10

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

class SendBackC20(Page):
    """This page is only for Agent. Agent can decide on effort level x."""
    form_model = 'group'
    form_fields = ['chosen_effort', 'chosen_effort_min20']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2 and player.control == 20

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Game(Page):
    timeout_seconds = 120

    live_method = play_game

    @staticmethod
    def js_vars(player: Player):
        return dict(
            params=player.session.params,
            slider_size=task_sliders.SLIDER_BBOX,
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            params=player.session.params,
            DEBUG=settings.DEBUG
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        puzzle = get_current_puzzle(player)

        if puzzle and puzzle.response_timestamp:
            player.elapsed_time = puzzle.response_timestamp - puzzle.timestamp
            player.num_correct = puzzle.num_correct
            player.payoff = player.num_correct


class Results(Page):
    pass

page_sequence = [    
    Introduction,
    Send,
    SendBackWaitPage,
    SendBackC5,
    SendBackC10,
    SendBackC20,
    ResultsWaitPage,
    Results,]
