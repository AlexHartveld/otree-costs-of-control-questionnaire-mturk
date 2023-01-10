from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'feedback'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    feedback_text = models.StringField(
        blank=True, 
        label='Is there any feedback you could give to us?')


# PAGES
class Feedback(Page):
    form_model = 'player'
    form_fields = ['feedback_text']


page_sequence = [Feedback]
