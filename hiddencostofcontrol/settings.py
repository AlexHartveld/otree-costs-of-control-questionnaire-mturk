from os import environ


SESSION_CONFIGS = [
    dict(
        name='trust',
        display_name="Experiment 1: Falk & Kosfeld",
        app_sequence=['informed_consent','demographics','trust','payment_info'],
        num_demo_participants=2,
    ),
    dict(
        name="sliders",
        display_name="Experiment 2: Real Effort",
        num_demo_participants=2,
        app_sequence=['informed_consent','demographics','sliders','payment_info']
    ),
        dict(
        name='survey',
        display_name="Experiment 3: Questionnaire",
        app_sequence=['survey', 'payment_info'], 
        num_demo_participants=1
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
        title='Study: Hidden costs of control',
        description='Our experiment lets participants play a short game with other participants, and/or answer a few question. We are interested in how people provide effort under different conditions.',
        frame_height=500,
        template='global/mturk_template.html',
        minutes_allotted_per_assignment=8,
        expiration_hours=1, # 7 * 24,
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
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '1875695137541'

INSTALLED_APPS = ['otree']

PARTICIPANT_FIELDS = ['random_treatment_ids']