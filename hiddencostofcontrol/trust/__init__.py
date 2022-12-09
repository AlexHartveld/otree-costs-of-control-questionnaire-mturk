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
    age = models.StringField(
        label='What is your age?', 
        widget=widgets.RadioSelect,
        choices=['18-24', '25-34', '35-44', '45-54', '55-', 'Prefer not to say'],
    )
    gender = models.StringField(
        choices=['Male', 'Female'],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    highest_education = models.StringField(
        choices=['High School or lower', 'Bachelors Degree', 'Masters Degree', 'Ph.D. or higher', 'Trade School', 'Prefer not to say'],
        label='What is the highest degree or level of education you have completed?',
        widget=widgets.RadioSelect,
    )
    country = models.StringField(
        label='Which country do you live in?',
        choices=["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]
    )
    consent = models.StringField(
        label = 'I agree to take part in this study',
        choices = ['Yes'],
        widget=widgets.RadioSelectHorizontal
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
class informed_consent(Page):
    form_model = 'player'
    form_fields =  ['consent']

class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'highest_education', 'country']

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


class Results(Page):
    """This page displays the profit of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

page_sequence = [
    informed_consent,
    Introduction,
    Demographics,
    Send,
    SendBackWaitPage,
    SendBackC5,
    SendBackC10,
    SendBackC20,
    ResultsWaitPage,
    Results,
]
