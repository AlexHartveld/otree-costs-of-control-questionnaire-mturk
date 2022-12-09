from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'informed_consent'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.StringField(
        label = 'I agree to take part in this study',
        choices = ['Yes'],
        widget=widgets.RadioSelectHorizontal
    )


# PAGES
class informed_consent(Page):
    form_model = 'player'
    form_fields =  ['consent']


page_sequence = [informed_consent]
