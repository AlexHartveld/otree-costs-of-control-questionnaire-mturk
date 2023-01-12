from os import environ


SESSION_CONFIGS = [
    dict(
        name='trust',
        display_name="Experiment 1: Falk & Kosfeld",
        app_sequence=['informed_consent','demographics','instructions_trust','trust','feedback','payment_info'],
        num_demo_participants=2,
    ),
    dict(
        name="sliders",
        display_name="Experiment 2: Real Effort",
        num_demo_participants=2,
        app_sequence=['informed_consent','demographics','instructions_sliders','sliders','feedback','payment_info']
    ),
        dict(
        name='survey',
        display_name="Experiment 3: Questionnaire",
        app_sequence=['survey', 'demographics', 'feedback', 'payment_info'], 
        num_demo_participants=1
    ),
    dict(
        name='trust+slider',
        display_name="Experiment 1+2: Demo",
        app_sequence=['informed_consent','demographics','instructions_demo', 'trust', 'sliders','feedback','payment_info'], 
        num_demo_participants=2
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01, participation_fee=0.25, doc="",
    mturk_hit_settings=dict(
        keywords='bonus, study',
        title='University Study: Hidden costs of control (short questionnaire or game with bonus)',
        description='Our experiment lets participants play a short game with other participants, and/or answer a few question. We are interested in how people provide effort under different conditions.',
        frame_height=500,
        template='global/mturk_template.html',
        minutes_allotted_per_assignment=8,
        expiration_hours=12, # 7 * 24,
        qualification_requirements=[
            {
            'QualificationTypeId': "36AGRGPO8VC7SA83E1O82NC4TWFCAY",
            'Comparator': "DoesNotExist",
            }],
        grant_qualification_id='36AGRGPO8VC7SA83E1O82NC4TWFCAY', # to prevent retakes
        ),
)

PARTICIPANT_FIELDS = ['is_dropout']
SESSION_FIELDS = ['params']



# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='mturk_room_hcoc',
        display_name='WU Vienna Experiment HCOC',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
    dict(
        name='poster_experiment1_2',
        display_name='Poster Presentation Experiment 1 + 2'
    ),
    dict(
        name='poster_experiment3',
        display_name='Poster Presentation Experiment 3'
    )
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are three experiments that aim to capture the hidden costs of control. Agents get an initial endowment (like a salary), and the Principal's payoff depends on what the Agent sends back.
The third experiment consists of five vignette stories, offered in a random order and with one out of four conditions per vignette (trust, human control, automated control, and monitoring).
The installation instructions are on GitHub: https://github.com/AlexHartveld/otree-costs-of-control-questionnaire-mturk
We also made this project to work with mTurk workers because we want to compare this population of automated control workers with the students from the original Falk & Kosfeld (2006) study. 
"""


SECRET_KEY = '1875695137541'

INSTALLED_APPS = ['otree']

PARTICIPANT_FIELDS = ['random_treatment_ids']