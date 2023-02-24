from flask import Flask,render_template,request, url_for, redirect, render_template, send_from_directory
import os 
import pandas as pd 
from logging.handlers import RotatingFileHandler
import logging
from flask import Flask
from flask.logging import default_handler
from werkzeug.utils import secure_filename
import random
import string

app = Flask(__name__)

# create the extension
app.secret_key = "az900"

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}


app = Flask(__name__)



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))


def configure_logging(app):
    # Logging Configuration
    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler = RotatingFileHandler('instance/flask-user-management.log',
                                           maxBytes=16384,
                                           backupCount=20)
        file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    app.logger.info('Starting the Flask User Management App...')


def generate_random_string(length):
    """Génère une chaîne de caractères aléatoire de longueur donnée."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
    


def salesman_distance(df_param):
    """Simple Travelling Salesperson Problem (TSP) between cities."""
    

    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp
    
    def fill_model():
    
      df = df_param
      n = max(df.iloc[:, :2].values.flatten()) 
      result = [[0 if i == j else 9999 for j in range(n)] for i in range(n)]
    
      for _, row in df.iterrows():
        u, v, _, cost = row
        result[u-1][v-1] = cost
        result[v-1][u-1] = cost if cost != 0 else 0
    
      return result 
    
    def create_data_model(i):
        """Stores the data for the problem."""
        data = {}
        data['distance_matrix'] = fill_model()
    
        
        data['num_vehicles'] = 1
        data['depot'] = i
        return data
    
    
    def print_solution(manager, routing, solution,i):
        result=[]
        result.append('Objective: {} miles'.format(solution.ObjectiveValue()))
        index = routing.Start(0)
        plan_output = 'Ville de départ '+str(i+1)+' :\n'
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(manager.IndexToNode(index)+1)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += ' {}\n'.format(manager.IndexToNode(index)+1)
        result.append(plan_output)
        
        return result
        
    return_list=[]
    for i in range(5):
      """Entry point of the program."""
      # Instantiate the data problem.
      data = create_data_model(i)

      # Create the routing index manager.
      manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                            data['num_vehicles'], data['depot'])

      # Create Routing Model.
      routing = pywrapcp.RoutingModel(manager)


      def distance_callback(from_index, to_index):
          """Returns the distance between the two nodes."""
          # Convert from routing variable Index to distance matrix NodeIndex.
          from_node = manager.IndexToNode(from_index)
          to_node = manager.IndexToNode(to_index)
          return data['distance_matrix'][from_node][to_node]



      transit_callback_index = routing.RegisterTransitCallback(distance_callback)

      # Define cost of each arc.
      routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

      # Setting first solution heuristic.
      search_parameters = pywrapcp.DefaultRoutingSearchParameters()
      search_parameters.first_solution_strategy = (
          routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

      # Solve the problem.
      solution = routing.SolveWithParameters(search_parameters)
      
      # Print solution on console.
      if solution:
          return_list.append(print_solution(manager, routing, solution,i))
    
    
  
    return return_list
    


def salesman_cost(df_param):
    """Simple Travelling Salesperson Problem (TSP) between cities."""
    

    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp
    
    def fill_model():
      
      df = df_param
      n = max(df.iloc[:, :2].values.flatten()) 
      result = [[0 if i == j else 9999 for j in range(n)] for i in range(n)]
    
      for _, row in df.iterrows():
        u, v, _, cost = row
        result[u-1][v-1] = _
        result[v-1][u-1] = _ if _ != 0 else 0
    
      return result 
    
    def create_data_model(i):
        """Stores the data for the problem."""
        data = {}
        data['distance_matrix'] = fill_model()
    
        
        data['num_vehicles'] = 1
        data['depot'] = i
        return data
    
    
    def print_solution(manager, routing, solution,i):
        result=[]
        result.append('Objective: {} miles'.format(solution.ObjectiveValue()))
        index = routing.Start(0)
        plan_output = 'Ville de départ '+str(i+1)+' :\n'
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(manager.IndexToNode(index)+1)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += ' {}\n'.format(manager.IndexToNode(index)+1)
        result.append(plan_output)
        
        return result
        
    return_list=[]
    for i in range(5):
      """Entry point of the program."""
      # Instantiate the data problem.
      data = create_data_model(i)

      # Create the routing index manager.
      manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                            data['num_vehicles'], data['depot'])

      # Create Routing Model.
      routing = pywrapcp.RoutingModel(manager)


      def distance_callback(from_index, to_index):
          """Returns the distance between the two nodes."""
          # Convert from routing variable Index to distance matrix NodeIndex.
          from_node = manager.IndexToNode(from_index)
          to_node = manager.IndexToNode(to_index)
          return data['distance_matrix'][from_node][to_node]



      transit_callback_index = routing.RegisterTransitCallback(distance_callback)

      # Define cost of each arc.
      routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

      # Setting first solution heuristic.
      search_parameters = pywrapcp.DefaultRoutingSearchParameters()
      search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

      # Solve the problem.
      solution = routing.SolveWithParameters(search_parameters)
      
      # Print solution on console.
      if solution:
          return_list.append(print_solution(manager, routing, solution,i))
    
    
  
    return return_list
    

def salesman_f(df_param):
    """Simple Travelling Salesperson Problem (TSP) between cities."""
    

    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp
    
    def fill_model():
  
      df = df_param
    
      result=[]
    
      cout=df.iloc[:,2].values
      distance=df.iloc[:,3].values
      for i in range(len(cout)):
        result.append(cout[i]/distance[i])
    
      df_temp= pd.DataFrame({"4":result})
      df=pd.concat([df, df_temp],axis=1)
    
      n = max(df.iloc[:, :2].values.flatten()) 
      result = [[0 if i == j else 9999 for j in range(n)] for i in range(n)]
    
      for _, row in df.iterrows():
        u, v, _, cost,po = row
        result[int(u)-1][int(v)-1] = po
        result[int(v)-1][int(u)-1] = po if po != 0 else 0
    
      return(result)
    
    def create_data_model(i):
        """Stores the data for the problem."""
        data = {}
        data['distance_matrix'] = fill_model()
    
        
        data['num_vehicles'] = 1
        data['depot'] = i
        return data
    
    
    def print_solution(manager, routing, solution,i):
        result=[]
        result.append('Objective: {} miles'.format(solution.ObjectiveValue()))
        index = routing.Start(0)
        plan_output = 'Ville de départ '+str(i+1)+' :\n'
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(manager.IndexToNode(index)+1)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += ' {}\n'.format(manager.IndexToNode(index)+1)
        result.append(plan_output)
        
        return result
        
    return_list=[]
    for i in range(5):
      """Entry point of the program."""
      # Instantiate the data problem.
      data = create_data_model(i)

      # Create the routing index manager.
      manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                            data['num_vehicles'], data['depot'])

      # Create Routing Model.
      routing = pywrapcp.RoutingModel(manager)


      def distance_callback(from_index, to_index):
          """Returns the distance between the two nodes."""
          # Convert from routing variable Index to distance matrix NodeIndex.
          from_node = manager.IndexToNode(from_index)
          to_node = manager.IndexToNode(to_index)
          return data['distance_matrix'][from_node][to_node]



      transit_callback_index = routing.RegisterTransitCallback(distance_callback)

      # Define cost of each arc.
      routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

      # Setting first solution heuristic.
      search_parameters = pywrapcp.DefaultRoutingSearchParameters()
      search_parameters.first_solution_strategy = (
          routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

      # Solve the problem.
      solution = routing.SolveWithParameters(search_parameters)
      
      # Print solution on console.
      if solution:
          return_list.append(print_solution(manager, routing, solution,i))
    
    
  
    return return_list
    

#---------------------------------------------------------------------------------------
#Page de l'interface : 

@app.route('/')
def accueil():
    return render_template('index.html')


@app.route('/drop')
def logo():
    info=request.args.get('info')
    return render_template('drop.html',info=info)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
          
            return redirect(url_for('logo',info='Renseignez un fichier !') )
        
        if file and allowed_file(file.filename):
            import requests
            import base64
            
            random_string = generate_random_string(15)+".csv"
            
            githubAPIURL = "https://api.github.com/repos/azury74/depo_csv/contents/"+random_string
            githubToken = "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"
            
            
        
            encodedData = base64.b64encode(file.read())
            
            headers = {
                    "Authorization": f'''Bearer {githubToken}''',
                    "Content-type": "application/vnd.github+json"
                }
            data = {
                    "message": "My commit message", # Put your commit message here.
                    "content": encodedData.decode("utf-8")
                }
            
            r = requests.put(githubAPIURL, headers=headers, json=data)
            
            url = 'https://raw.githubusercontent.com/azury74/depo_csv/main/'+random_string
        
            df = pd.read_csv(url, sep=";",header=None)
            
            
            return render_template('result.html',distance=salesman_distance(df),cost=salesman_cost(df),f=salesman_f(df))
        
        else: 
            return redirect(url_for('logo',info='Pas la bonne extention !') )
    return


if __name__ == '__main__':
    app.run()

    
