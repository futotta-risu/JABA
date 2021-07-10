from PyQt5.QtWidgets import QAction

def create_action(application, text, function):
    '''
        Create and action and connect on trigger 
        
        Parameters
            application (QMainWindow) Usually self
            text (str) String of the action
            function (function) Function to be triggered
            
    '''
    action = QAction('&' + text, application)
    action.triggered.connect(function)

    return action