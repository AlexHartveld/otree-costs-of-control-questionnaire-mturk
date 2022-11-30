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
        player.control = control[player.group.id % 3 - 1]

class Group(BaseGroup):
    trust = models.StringField(
        choices=['Yes', 'No'],
        widget=widgets.RadioSelectHorizontal
    )
    chosen_effort = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(0), max=cu(120))
    chosen_effort5 = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(5), max=cu(120))
    chosen_effort10 = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(10), max=cu(120))
    chosen_effort20 = models.CurrencyField(doc="""Amount sent back by P2""", min=cu(20), max=cu(120))

class Player(BasePlayer):
#    pass
    control = models.IntegerField() #this is necessary since control variable is used as treatment. idk what to set it to so I just chose the models.StringField. definitely WIP only.


# FUNCTIONS
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = 2 * group.chosen_effort
    p2.payoff = C.ENDOWMENT_AGENT - group.chosen_effort


# PAGES
class Introduction(Page):
    pass


class Send(Page):
    """This page is only for Principal. Can either trust the agent or not."""
    form_model = 'group'
    form_fields = ['trust']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    pass


#class SendBack(Page):
#    """This page is only for Agent. Agent can decide on effort level x."""
#    form_model = 'group'
#    form_fields = ['chosen_effort']

#    @staticmethod
#    def is_displayed(player: Player):
#        return player.id_in_group == 2

#    @staticmethod
#    def vars_for_template(player: Player):
#        group = player.group


class SendBackC5(Page):
    """This page is only for Agent. Agent can decide on effort level x."""
    form_model = 'group'
    form_fields = ['chosen_effort', 'chosen_effort5']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2 and player.control == 5

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

class SendBackC10(Page):
    """This page is only for Agent. Agent can decide on effort level x."""
    form_model = 'group'
    form_fields = ['chosen_effort', 'chosen_effort10']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2 and player.control == 10

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

class SendBackC20(Page):
    """This page is only for Agent. Agent can decide on effort level x."""
    form_model = 'group'
    form_fields = ['chosen_effort', 'chosen_effort20']

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

        #return dict(tripled_amount=group.sent_amount * C.MULTIPLIER)


page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
#    SendBack,
    SendBackC5,
    SendBackC10,
    SendBackC20,
    ResultsWaitPage,
    Results,
]
