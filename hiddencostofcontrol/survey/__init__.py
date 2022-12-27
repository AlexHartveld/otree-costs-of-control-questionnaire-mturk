from otree.api import *
import random


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    vignettes = ['1', '2', '3', '4', '5']
    NUM_ROUNDS = len(vignettes)
    StandardChoices=[
        [1, 'Very low'],
        [2, 'Low'],
        [3, 'Medium'],
        [4, 'High'],
        [5, 'Very high']
    ]

class Subsession(BaseSubsession):
    pass
def creating_session(self):
    if self.round_number == 1:
        for p in self.get_players():
            round_numbers = list(range(1, C.NUM_ROUNDS + 1))
            random.shuffle(round_numbers)
            p.participant.vars['surveys_rounds'] = dict(zip(C.vignettes, round_numbers))
            #p.participant.vars['num_rounds'] = C.NUM_ROUNDS

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Have 20 questions, only show results for 5 of them?
    # 5 pages with 1 / 4 random questions
    # Vignette 1
    item1control = models.IntegerField(
        label='You realize on the way home that you forgot your umbrella. When you enter the supermarket, you see that the manager is again examining the amounts in the cash registers.',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item1trust = models.IntegerField(
        label='The manager believes that you reports are honest and does not double check the balances in the cash registers.',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item1autocontrol = models.IntegerField(
        label='Condition C',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item1monitoring = models.IntegerField(
        label='Condition D',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    # Vignette 2
    item2control = models.IntegerField(
        label='Before starting your work, you have to sign a binding agreement. This defines your working times exactly.',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item2trust = models.IntegerField(
        label='Your boss asks you to follow the work times exactly.',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item2autocontrol = models.IntegerField(
        label='Condition C',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item2monitoring = models.IntegerField(
        label='Condition D',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    # Vignette 3
    item3control = models.IntegerField(
        label='The new employer does not hire you until he has gathered information about you from your previous employer and confirmed the accuracy of your information.',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item3trust = models.IntegerField(
        label='The new employer believes your information and hires you.',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item3autocontrol = models.IntegerField(
        label='Condition C',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item3monitoring = models.IntegerField(
        label='Condition D',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    # Vignette 4
    item4trust = models.IntegerField(
        label='The room where the photocopier and the printer are located stands open.',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item4control = models.IntegerField(
        label='The room where the photocopier and the printer are located is locked, meaning that in general you first have to get the key from your boss.',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item4autocontrol = models.IntegerField(
        label='Condition C',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item4monitoring = models.IntegerField(
        label='Condition D',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
        # Vignette 5
    item5trust = models.IntegerField(
        label='During a meeting, the management asks all employees to respect this rule.',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item5control = models.IntegerField(
        label='In order to limit potential abuses, the management installed special software, which lists all Internet sites the employees have visited.',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    # control and monitoring may be the same...
    item5autocontrol = models.IntegerField(
        label='Condition C',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )
    item5monitoring = models.IntegerField(
        label='Condition D',
        choices=C.StandardChoices,
        widget=widgets.RadioSelectHorizontal
    )

# FUNCTIONS
# PAGES
# def progress(p):
#     curpageindex = page_sequence.index(type(p))+1
#     progress = ((p.round_number-1)*pages_per_round+curpageindex)/tot_pages*100
#     return progress


class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['crt_bat', 'crt_widget', 'crt_lake']

class Vignette1(Page):
    form_model = 'player'
    def is_displayed(self):
        return self.round_number == self.participant.vars['surveys_rounds']['1']

    @staticmethod
    def get_form_fields(self):
        conditions = [
        'item1control',
        'item1trust',
        'item1autocontrol',
        'item1monitoring',
        ]
        return [random.choice(conditions)]

    # def vars_for_template(self):
    #     #curpageindex = page_sequence.index(type(self)) - 1
    #     #progress = curpageindex / len(page_sequence) * 100
    #     return {
    #         'progress': progress(self)
    #     }

class Vignette2(Page):
    form_model = 'player'
    def is_displayed(self):
        return self.round_number == self.participant.vars['surveys_rounds']['2']

    @staticmethod
    def get_form_fields(self):
        conditions = [
        'item2control',
        'item2trust',
        'item2autocontrol',
        'item2monitoring',
        ]
        return [random.choice(conditions)]

    # def vars_for_template(self):
    #     #curpageindex = page_sequence.index(type(self)) - 1
    #     #progress = curpageindex / len(page_sequence) * 100
    #     return {
    #         'progress': progress(self)
    #     }

class Vignette3(Page):
    form_model = 'player'
    def is_displayed(self):
        return self.round_number == self.participant.vars['surveys_rounds']['3']

    @staticmethod
    def get_form_fields(self):
        conditions = [
        'item3control',
        'item3trust',
        'item3autocontrol',
        'item3monitoring',
        ]
        return [random.choice(conditions)]

    # def vars_for_template(self):
    #     #curpageindex = page_sequence.index(type(self)) - 1
    #     #progress = curpageindex / len(page_sequence) * 100
    #     return {
    #         'progress': progress(self)
    #     }

class Vignette4(Page):
    form_model = 'player'
    def is_displayed(self):
        return self.round_number == self.participant.vars['surveys_rounds']['4']

    @staticmethod
    def get_form_fields(self):
        conditions = [
        'item4control',
        'item4trust',
        'item4autocontrol',
        'item4monitoring',
        ]
        return [random.choice(conditions)]

    # def vars_for_template(self):
    #     #curpageindex = page_sequence.index(type(self)) - 1
    #     #progress = curpageindex / len(page_sequence) * 100
    #     return {
    #         'progress': progress(self)
    #     }

class Vignette5(Page):
    form_model = 'player'
    def is_displayed(self):
        return self.round_number == self.participant.vars['surveys_rounds']['5']

    def get_form_fields(self):
        conditions = [
        'item5control',
        'item5trust',
        'item5autocontrol',
        'item5monitoring',
        ]
        return [random.choice(conditions)]

    # def vars_for_template(self):
    #     #curpageindex = page_sequence.index(type(self)) - 1
    #     #progress = curpageindex / len(page_sequence) * 100
    #     return {
    #         'progress': progress(self)
    #     }

page_sequence = [
    Vignette1,
    Vignette2,
    Vignette3,
    Vignette4,
    Vignette5,
]

pages_per_round = len(page_sequence)
tot_pages = pages_per_round * C.NUM_ROUNDS
