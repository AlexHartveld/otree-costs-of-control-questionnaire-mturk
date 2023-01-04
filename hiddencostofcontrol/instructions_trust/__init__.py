from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'instructions_trust'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'instructions_trust/instructions.html'



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
        choices=[10,11,22,44],
        widget=widgets.RadioSelectHorizontal,
        label='Player B decided to set a minimum amount of 10 and Player A stated to send 23 points in case of no minimum amount and 11 in case of a minimum amount, how many points does Player B have in the end?'
    )
    instruction_q4 = models.IntegerField(
        choices=[40,80,120,160],
        widget=widgets.RadioSelectHorizontal,
        label='Player A sent 40 points to Player B. How many points does player A have in the end?'
    )


# PAGES
class Introduction(Page):
    form_model = 'player'
    form_fields = ['instruction_q1','instruction_q2','instruction_q3','instruction_q4']


page_sequence = [Introduction]
