from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'demographics'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.StringField(
        label='What is your age?', 
        widget=widgets.RadioSelect,
        choices=['18-24', '25-34', '35-44', '45-54', '55-', 'Prefer not to say'],
    )
    gender = models.StringField(
        choices=['Male', 'Female', 'Other', 'Prefer not to say'],
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
    workexperience = models.IntegerField(
        label="Please indicate your work experience. All jobs count, including part-time and volunteer work.",
        choices=[
            [1, 'I do not have work experience.'],
            [2, 'Less than 1 year work experience.'],
            [3, 'Between 1 and less than 2 years of work experience'],
            [4, 'Between 2 and less than 3 years work experience.'],
            [5, 'Between 3 and less than 4 years work experience.'],
            [6, 'Between 4 and less than 5 years work experience.'],
            [7, '5 years or more work experience.'],
            [8, 'I prefer not to say.'],
        ]
    )


# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'highest_education', 'workexperience', 'country']


page_sequence = [Demographics]
