# Description: Configuration file for the experiment. It contains the experiment structure and the video sources.
# Terms used:
# Experiment    - The entire experiment, which is composed of parts. 
#                 One participant will go through everuthing contained in the experiment.
#                 A "session" is a single run of the experiment by a participant.
# Part          - A division of the experiment. Can be an abstract or concrete concept. 
#                 For example, a part can be a set of videos to be evaluated, or a set of questions to be answered.
#                 It is useful to divide the experiment into parts to make it easier to manage each session.
#                 The first part may contain the MUSHRA test page, the second part may contain the AB test page, and so on.
#                 But it is NOT required that every test page in a part be the same.
#                 Parts contain one or more (test) Pages. Parts can be randomized for each participant.
# Page          - A test page. It can be a MUSHRA test page, an AB test page, or any other *mode* of test page defined in /templates.
#                 A Page contains one unique ID (Name), its *mode* (MUSHRA, AB, etc.), and one or more stimuli to be evaluated.
#                 Pages can be randomized for each participant.
# Stimulus      - A content to be evaluated (currently, only videos). 
#                 A stimulus contains a unique ID (Name) and the path to the video file.
#                 Stimuli inside a Page can be randomized for each participant.
#
#
# The EXPERIMENT variable contains the experiment structure. It is a dictionary with the following keys:
# - Config: Contains the configuration for the experiment, also a dictionary:
#   - Random_part: If True, the order of the Parts will be randomized.
#   - Random_page: If True, the order of the Pages inside a Part will be randomized.
#   - VideoSource: The source of the videos. Can be 'local' or 'youtube'.
#                  (Only 'local' is fully implemented at the moment)
# - Parts: Every Part is defined by its name (key as string) and a list of Pages (values).
#          Create a new Part by adding a new key-value pair to the dictionary.
#
# A Page is defined as dictionary with the following keys:
# - Config: Contains the configuration for the Page, a dictionary:
#   - Mode: The mode of the test page. Can be 'MUSHRA', 'AB', 'Single', 'Single_v2', etc.
#           (See /templates for the available modes)
#   - Random: If True, the order of the stimuli will be randomized.
#   - Name: The name (ID) of the Page. This name will be used to save the results.
# - Stimulus: Every stimulus is defined by its name (key as string) and the path to the file (value).
#             Create a new stimulus by adding a new key-value pair to the dictionary.
#             Note: Some modes require a specific number of stimuli. Check the template for each mode.

HL_1 = {
    'Config': {
        'Mode': 'MUSHRA',
        'Random' : True,
        'Name': 'id_004',
    },
    'llm'   : 'data/llm/id_004.mp4',
    'llm_DiT' : 'data/llm_DiT/id_004.mp4',
    'ref_low' : 'data/ref_low/id_004.mp4', 
    'ref_high': 'data/ref_high/id_004.mp4',
}   

HL_2 = {
    'Config': {
        'Mode': 'MUSHRA',
        'Random' : True,
        'Name': 'id_005',
    },
    'llm'   : 'data/llm/id_005.mp4',
    'llm_DiT' : 'data/llm_DiT/id_005.mp4',
    'ref_low' : 'data/ref_low/id_005.mp4', 
    'ref_high': 'data/ref_high/id_005.mp4',
}

HL_3 = {
    'Config': {
        'Mode': 'MUSHRA',
        'Random' : True,
        'Name': 'id_006',
    },
    'llm'   : 'data/llm/id_006.mp4',
    'llm_DiT' : 'data/llm_DiT/id_006.mp4',
    'ref_low' : 'data/ref_low/id_006.mp4',
    'ref_high': 'data/ref_high/id_006.mp4',
}

HL_4 = {
    'Config': {
        'Mode': 'MUSHRA',
        'Random' : True,
        'Name': 'id_010',
    },
    'llm'   : 'data/llm/id_010.mp4',
    'llm_DiT' : 'data/llm_DiT/id_010.mp4',
    'ref_low' : 'data/ref_low/id_010.mp4', 
    'ref_high': 'data/ref_high/id_010.mp4',
}

HL_5 = {
    'Config': {
        'Mode': 'MUSHRA',
        'Random' : True,
        'Name': 'id_017',
    },
    'llm'   : 'data/llm/id_017.mp4',
    'llm_DiT' : 'data/llm_DiT/id_017.mp4',
    'ref_low' : 'data/ref_low/id_017.mp4', 
    'ref_high': 'data/ref_high/id_017.mp4',
}

HL_6 = {
    'Config': {
        'Mode': 'MUSHRA',
        'Random' : True,
        'Name': 'id_040',
    },
    'llm'   : 'data/llm/id_040.mp4',
    'llm_DiT' : 'data/llm_DiT/id_040.mp4',
    'ref_low' : 'data/ref_low/id_040.mp4', 
    'ref_high': 'data/ref_high/id_040.mp4',
}

HL_7 = {
    'Config': {
        'Mode': 'MUSHRA',
        'Random' : True,
        'Name': 'id_049',
    },
    'llm'   : 'data/llm/id_049.mp4',
    'llm_DiT' : 'data/llm_DiT/id_049.mp4',
    'ref_low' : 'data/ref_low/id_049.mp4', 
    'ref_high': 'data/ref_high/id_049.mp4',
}

HL_8 = {
    'Config': {
        'Mode': 'MUSHRA',
        'Random' : True,
        'Name': 'id_057',
    },
    'llm'   : 'data/llm/id_057.mp4',
    'llm_DiT' : 'data/llm_DiT/id_057.mp4',
    'ref_low' : 'data/ref_low/id_057.mp4', 
    'ref_high': 'data/ref_high/id_057.mp4',
}


import itertools


# --- Definiciones de AB (Appropriateness) - GENERADAS AUTOMÁTICAMENTE ---
VIDEO_CATEGORIES = ['llm', 'llm_DiT', 'ref_low', 'ref_high']
#VIDEO_IDS = ['id_004', 'id_005', 'id_006', 'id_010', 'id_017', 'id_040', 'id_049', 'id_057']
VIDEO_IDS = ['id_010', 'id_017', 'id_040', 'id_049']

# Generar todas las combinaciones únicas de dos categorías
CATEGORY_COMBINATIONS = list(itertools.combinations(VIDEO_CATEGORIES, 2))

# Lista para almacenar los nombres de las variables APP_X
APP_LIST = []
APP_COUNTER = 1

for video_id in VIDEO_IDS:
    for cat1, cat2 in CATEGORY_COMBINATIONS:
        # Crea una variable global con el nombre APP_X
        # Esto permite que EXPERIMENT['Part2'] contenga referencias a estas variables
        globals()[f'APP_{APP_COUNTER}'] = {
            'Config': {
                'Mode': 'AB',
                'Random': True,
                'Name': f'{cat1}_vs_{cat2}_{video_id}', # Nombre descriptivo de la comparación
            },
            'VideoA': f'data/{cat1}/{video_id}.mp4', # Video A
            'VideoB': f'data/{cat2}/{video_id}.mp4', # Video B
        }
        APP_LIST.append(f'APP_{APP_COUNTER}')
        APP_COUNTER += 1


EXPERIMENT = {
    'Config'      : {
        'Random_part' : False,
        'Random_page' : True,
        'VideoSource' : 'local', # youtube or local
    },
    'Part1'           : [HL_1, HL_2, HL_3, HL_4, HL_5, HL_6, HL_7, HL_8],
    'Part2'           : [globals()[app_name] for app_name in APP_LIST], # Usa la lista generada
    # Para depuración, puedes usar subconjuntos:
    # 'Part1'          : [HL_1],
    # 'Part2'          : [globals()['APP_1']], # Solo un ejemplo, si solo quieres la primera APP generada
}


# Use this if using youtube API
VIDEO_PARAMS = { 'autoplay': 0,
                   'color': 'red',
                   'controls': 0,
                   'disablekb': 1,
                   'enablejsapi': 1,
                   'mute': 0,
                   'loop': 0,
                   'modestbranding': 1,
                   'playsinline': 1,
                   'start': 0,
                   'rel': 0,
                   'showinfo': 0,
                 }

