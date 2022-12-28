from otree.api import *

doc = """
A two-stage principal-agent game is played with only one round. There is no context given, the game is framed in a neutral manner. X represents some productive activity and is costly to the agent 
(c(x) = x) but benefits the principal (πp = 2x). The profit function of the agent is πa = 120 – x.
The principal can either leave the choice of x to the agent or set a minimum level (x > 0), thereby re-stricting the choice set representing the level of control in this experiment design.
"""

class C(BaseConstants):
    NAME_IN_URL = 'trust'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'trust/instructions.html'
    ENDOWMENT_AGENT = cu(120) #Agents endowment
    ENDOWMENT_PRINCIPAL = cu(0) #Principals endowment

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
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
    control = models.IntegerField()
    instruction_q1 = models.StringField(
        choices=['Yes', 'No'],
        widget=widgets.RadioSelectHorizontal,
        label='Player A can set a minimum amount for Player B.'
    )
    instruction_q2 = models.StringField(
        choices=['Yes', 'No'],
        widget=widgets.RadioSelectHorizontal,
        label='Player A knows about the decision of Player B before Player A he has to decide.'
    )
    instruction_q3 = models.IntegerField(
        choices=[10,11,22,44],
        widget=widgets.RadioSelectHorizontal,
        label='Player B decided to set a minimum amount of 10 and Player A stated to send 23 points in case of no minimum amount and 11 in case of a minimum amount, how many points does Player B have in the end?'
    )
    instruction_q4 = models.IntegerField(
        choices=[40,80,120,160],
        widget=widgets.RadioSelectHorizontal,
        label='Player A sent 40 points to Player B. How many points does player A have in the end?'
    )


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

# PAGES
class Introduction(Page):
    form_model = 'player'
    form_fields = ['instruction_q1','instruction_q2','instruction_q3','instruction_q4']

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


class Results(Page):
    """This page displays the profit of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBackC5,
    SendBackC10,
    SendBackC20,
    ResultsWaitPage,
    Results,
]
