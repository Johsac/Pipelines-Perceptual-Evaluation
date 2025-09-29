from flask import Flask, render_template, request, jsonify, redirect, url_for, Blueprint, session
import json
import numpy as np
import random
import datetime
import os
import pandas as pd  
from config.experiment import *

# Initialize directories
os.makedirs('results', exist_ok=True)
os.makedirs('sessionlogs', exist_ok=True)

# Initialize the Flask application
app = Flask(__name__)  
app.secret_key = 'this_is_a_random_key'

# Create blueprints for static folders
styles_bp = Blueprint('styles', __name__, static_folder='styles', static_url_path='/styles')
data_bp = Blueprint('data', __name__, static_folder='data', static_url_path='/data')

# Register blueprints with the Flask application
app.register_blueprint(styles_bp)
app.register_blueprint(data_bp)

START = None

# Initialize the session
def sessionPlanner():
    """
    Create a session based on the experiment parameters defined in /config/experiment.py

    Check the /config/experiment.py for a detailed explanation of the experiment structure
    """
    if len(session['SESSION']) == 0:
        # Create a list of the Experiment Parts
        len_exp = len(EXPERIMENT) - 1
        order = list(range(len_exp))
        # Randomize the order of the Parts
        if EXPERIMENT['Config']['Random_part']:
            random.shuffle(order)
        for j, n_order in enumerate(order):
            # Get Part
            part = list(EXPERIMENT.keys())[n_order+1]
            # Get (test) Pages
            tests = EXPERIMENT[part]
            # Randomize the order of the Pages
            if EXPERIMENT['Config']['Random_page']:
                random.shuffle(tests)
            # For each Page
            for test in tests:
                stimulus = len(test) - 1
                stimulus_order = list(range(stimulus))
                # Randomize the order of the Stimulus
                if test['Config']['Random']:
                    random.shuffle(stimulus_order)
                stimulus = [ [list(test.keys())[n_stimulys+1], list(test.values())[n_stimulys+1] ] for n_stimulys in stimulus_order]
                # Add to session
                # 'SESSION' is the list of pages to be presented
                session['SESSION'].append([
                    'Page'+str(len(session['SESSION'])+1),
                    part,
                    test['Config']['Name'],
                    test['Config']['Mode'],
                    stimulus
                ])

def printSession():
    """
    Print pages to be presented in the session in order
    """
    for page in session['SESSION']:
        print(page[0])
        print(page[1], page[2], page[3])
        for stimulus in page[4]:
            print(stimulus[0])
            print(stimulus[1])
        print('---------')

def getNextPage():
    """
    Delete the current page from the session and return the next page
    """
    if len(session['SESSION']) > 0:
        session['RECORDED'].append(session['SESSION'].pop(0))
        session.modified = True
        return session['RECORDED'][-1]
    else:
        return None

def checkNextPage():
    """
    This does not register the page, just checks the next page
    """
    if len(session['SESSION']) > 0:
        return session['SESSION'][0]

def getCurrentPage():
    """
    Get the current page of the session
    """
    if len(session['RECORDED']) > 0:
        return session['RECORDED'][-1]
    return None 
    
def page2dict(page):
    if page:
        page_number = len([p for p in session['RECORDED'] if p[1] == page[1]])
        video_left_folder = os.path.basename(os.path.dirname(page[4][0][1])) # Obtiene la carpeta del video izquierdo
        video_right_folder = os.path.basename(os.path.dirname(page[4][1][1])) # Obtiene la carpeta del video derecho
        return dict(
            {
                'Page ID'     : page[0],
                'Part'        : page[1],
                'Test'        : page[2],
                'Mode'        : page[3],
                'VSource'     : EXPERIMENT['Config']['VideoSource'],
                'VConfig'     : VIDEO_PARAMS,
                'PageNumber'  : page_number,
                'PageTotal'   : len(EXPERIMENT[page[1]]),
                'video_left_folder': video_left_folder, # Añade la carpeta del video izquierdo
                'video_right_folder': video_right_folder, # Añade la carpeta del video derecho
            },
            **{'S'+str(i+1)  : stimulus[0]  for i, stimulus in enumerate(page[4])},
            **{'URL'+str(i+1): stimulus[1]  for i, stimulus in enumerate(page[4])},
        )
    else:
        return None

def registerAnswer(answer):
    """
    Register the answer of a given Page.

    The answer can be processed differently depending on the type (mode) of the Page.
    After the answer is processed, it is added to the session['ANSWERS'] list.
    Once the session is finished, the answers are saved *AS IS* to a file.
    Therefore, the processing of the answers should be done in this function.
    """
    # Get what is registered in the current page
    print('REGISTERING ANSWER')
    page = page2dict(getCurrentPage())
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if page['Mode'] == 'MUSHRA':                                            # Registration for MUSHRA type of page
        part = EXPERIMENT[page['Part']]                                     # Get the part of the experiment
        for test in part:                                                   # Run through the tests of the part
            if test['Config']['Name'] == page['Test']:                      # Checks which test is the current page
                # Para MUSHRA, ahora se itera sobre los videos y se agrega la información de cada uno.
                # Asegúrate de que 'answer' contenga un diccionario con las puntuaciones de cada video
                for video_key, score in answer.items():
                    # Extraer el número del video (ej. '1' de 'video1')
                    video_num = video_key.replace('video', '')
                    # Obtener el nombre del estímulo usando el número del video
                    stimulus_name = page['S' + video_num]
                    session['ANSWERS'].append([session['id'], page['Mode'], page['Part'], page['Test'], stimulus_name, score, timestamp])
                break                                                       
    
    elif page['Mode'] == 'AB':                                              # Registration for AB type of page
        selected_value = answer
        mapped_value = None # Inicializa mapped_value
        if selected_value == 'left_clearly_better':
            mapped_value = -2
        elif selected_value == 'left_slightly_better':
            mapped_value = -1
        elif selected_value == 'both_equal':
            mapped_value = 0
        elif selected_value == 'right_slightly_better':
            mapped_value = 1
        elif selected_value == 'right_clearly_better':
            mapped_value = 2
        else:
            mapped_value = 'Unknown'

        # Extraer el nombre de la carpeta (v5, v7, ref_low, ref_high) de las URLs
        # Esto asume que la estructura de la URL es "data/carpeta_video/nombre_video.mp4"
        video_left_folder = os.path.basename(os.path.dirname(page['URL1']))
        video_right_folder = os.path.basename(os.path.dirname(page['URL2']))

        # AGREGAR ESTA LÍNEA CON LAS VARIABLES video_left_folder y video_right_folder
        session['ANSWERS'].append([session['id'], page['Mode'], page['Part'], page['Test'], video_left_folder, video_right_folder, mapped_value, timestamp])
    session.modified = True
    session.modified = True
    logSession()
    printAnswers()

def logSession():
    """
    Save a log with the current answers of the session.
    This is useful to recover the session in case of a crash.
    """
    with open('sessionlogs/' + session['id'] + '.json', 'w') as outfile:
        json.dump(session, outfile, indent=4)

@app.route('/loadSession', methods=['GET', 'POST'])
def loadSession():
    """
    Recover a session from a log file.
    This function can only be called through index.html
    """
    try:
        data = request.get_json()
        assert data is not None, 'No data provided'
        # Load log data
        with open('sessionlogs/' + data['id'] + '.json') as file:
            session_data = json.load(file)
        # Update session
        session.update(session_data)
        # redirect to the next page
        return process_answer()
    except Exception as e:
        print('error on loadSession: ', e)
        return jsonify({'error on process_answer': str(e)})

def printAnswers():
    """
    Print every answer in the session
    """
    for entry in session['ANSWERS']:
        print(entry)

def saveResults():
    """
    Save results to local CSV files.
    """
    printAnswers()
    save_results_local_csv()

def save_results_local_csv():
    """
    Save results to a local CSV file for the current participant.
    """
    participant_id = session['id']
    csv_file_path = f'results/participant_{participant_id}.csv'
    
    # Define headers for the CSV
    headers = ['Participant_ID', 'Mode', 'Part', 'Test', 'Stimulus_or_VideoLeft', 'Score_or_VideoRight', 'Value_or_Timestamp', 'Timestamp_if_AB']

    # Prepare data for CSV
    csv_data = []
    for entry in session['ANSWERS']:
        if entry[1] == 'MUSHRA': # MUSHRA answers
            csv_data.append([
                entry[0], # Participant_ID
                entry[1], # Mode
                entry[2], # Part
                entry[3], # Test
                entry[4], # Stimulus
                entry[5], # Score
                entry[6], # Timestamp
                '' # Empty for AB-specific timestamp
            ])
        elif entry[1] == 'AB': # AB answers
            csv_data.append([
                entry[0], # Participant_ID
                entry[1], # Mode
                entry[2], # Part
                entry[3], # Test
                entry[4], # Video_Left
                entry[5], # Video_Right
                entry[6], # Score_AB (el valor numérico)
                entry[7]  # Timestamp
            ])
    
    # Create a DataFrame and save to CSV
    df = pd.DataFrame(csv_data, columns=headers)
    df.to_csv(csv_file_path, index=False)
    print(f"Participant {participant_id} results saved locally at: {csv_file_path}")

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Start a new session. This is the first page of the experiment.
    It is called when the user access the website or every time the user enters the URL and updates the page.
    """
    print('-----------------------------------------------------------')
    print('----------------------- NEW SESSION -----------------------')
    print('-----------------------------------------------------------')
    # Creates a new and unique session using Flask's session
    # This prevents that different users interfere with each other
    session['id'] = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    session['SESSION'] = []
    session['RECORDED'] = []
    session['ANSWERS'] = []
    return render_template("index.html", data={'id': session['id']})

@app.route('/process_answer', methods=['POST'])
def process_answer():
    """
    One of the most important functions of the experiment.
    It processes the answer of the user and redirects to the next page.
    """
    try:
        # Get the data sent by the client
        data = request.get_json()
        assert data is not None, 'No data provided'

        # Should only enter here after the index.html Page
        if 'Next' in data:
            if data['Next'] == "introp1":
                return jsonify({'redirect': '\introp1'})
            else:
                print("Something went wrong")
                
        # The Page before the experiment starts should enter here
        # i.e., if your experiment have lots of pages before the actual experiment starts
        # only the last one should send "{'Start': true}" back to Flask
        elif 'Start' in data:
            if len(session['SESSION']) == 0:
                sessionPlanner()
                global START
                START = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            return loadNextPage()
        
        # The actual experiment should enter here. Every Page in the experiment should pass through this code
        elif 'NextPage' in data:
            # Register the answer given the data sent by the client
            currentPage = page2dict(getCurrentPage())
            if 'videoScores' in data: # If it is a MUSHRA page
                registerAnswer(data['videoScores'])
            elif 'selectedValue' in data: # If it is a AB page
                registerAnswer(data['selectedValue'])

            # Checks the current and the next Page, if they have different modes (types), 
            # redirect to the intro page of the next mode. 
            currentPage = page2dict(getCurrentPage())
            nextPage = page2dict(checkNextPage())
            if nextPage:
                if nextPage['Mode'] != currentPage['Mode']:
                    if nextPage['Mode'] == 'AB':
                        return jsonify({'redirect': '\introp2'})
                    else:
                        print('Error on process_answer: no intro for the next page mode.')

            # If there is no next Page, save the results and redirect to the end page
            elif not nextPage:
                print('You have reached the end of the experiment. Saving results.')
                saveResults()
                return jsonify({'redirect': url_for('end')})

            # Change to the next page. This should be the last thing to do
            return loadNextPage()
        
        # The intro pages are not part of the experiment. They are just to introduce the next mode (type) of the experiment
        # After these pages, get back to the experiment
        elif 'outIntro' in data:
            return loadNextPage()
                
    # Catch any error and return it to the client
    except Exception as e:
        print('Caught an error on process_answer: ', e)
        return jsonify({'error on process_answer': str(e)})
    
def getURL(page):
    """
    Get the correct URL for any page
    """
    if page == 'MUSHRA':
        return jsonify({'redirect': url_for('MUSHRA')})
    elif page == 'AB':
        return jsonify({'redirect': url_for('AB')})
    return jsonify({'error': 'Invalid page mode'})

def loadNextPage():
    """
    Delete the current page from the session and get the next page from getNextPage()
    Returns the URL of the next page
    """
    page = page2dict(getNextPage())
    if page:
        return getURL(page['Mode'])
    else: 
        print('No next page found')
        return jsonify({'redirect': url_for('end')})

@app.route('/mushra')
def MUSHRA():
    pagedict = page2dict(getCurrentPage())
    # Generar dinámicamente los nombres y URLs de los videos
    videos = []
    # Itera sobre los estímulos en el orden correcto
    for i in range(1, 5): # Asumiendo 4 videos para MUSHRA
        stimulus_key = f'S{i}'
        url_key = f'URL{i}'
        if stimulus_key in pagedict and url_key in pagedict:
            videos.append({
                'name': pagedict[stimulus_key],
                'url': pagedict[url_key],
                'id': i
            })
    return render_template('MUSHRA.html', data=pagedict, videos=videos)

@app.route('/ab')
def AB():
    pagedict = page2dict(getCurrentPage())
    return render_template('AB.html', data=pagedict)

@app.route('/finished')
def end():
    return render_template('end.html')

@app.route('/introp1')
def introp1():
    return render_template('introp1.html')

@app.route('/introp2')
def introp2():
    return render_template('introp2.html')

def printClientSession(full=True):
    """
    Print the current session of the client
    """
    print('-----------------------------')
    print('-------CLIENT SESSION--------')
    print('-----------------------------')
    print('ID: ', session['id'])
    print('SESSION: ', len(session['SESSION']))
    print('RECORDED: ', len(session['RECORDED']))
    print('ANSWERS: ', len(session['ANSWERS']))
    if full:
        printAnswers()
    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)