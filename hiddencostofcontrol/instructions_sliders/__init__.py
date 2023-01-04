from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'instructions_sliders'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'instructions_sliders/instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
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
        choices=[10,13,15,25],
        widget=widgets.RadioSelectHorizontal,
        label='If Player B decided to set a minimum amount of 10 and Player A moved 3 sliders correctly, how many points does Player B have in the end?'
    )

# PAGES
class Introduction(Page):
    form_model = 'player'
    form_fields = ['instruction_q1','instruction_q2','instruction_q3']


page_sequence = [Introduction]
