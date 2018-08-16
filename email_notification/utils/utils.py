import os
import logging
import yaml

def logger(logger_name = __name__, 
           filename = 'log.log', 
           level = logging.DEBUG):
    """
    logger for logging
    
    Args:
        logger_name:``str``
            name of logger
        filename:``str`` 
            path and file name
        level:``str``
            logging level
        
    Return:
        logger funcation for logging:``logger``
        
    """
    #set logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.FileHandler('log.log')
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler) 

    return logger
    
def walk_directory(dir_path, files_only = True):
    """
    Get list of all file in directory recursive
    
    Args:
        dir_path:``str``
            parent directory to start
        files_only:``bool``
            get list of files only other
    
    Return:
        If file only than list of all files 
        otherwise files and list of directories
        
    """

    list_files = []
    list_dir = []
    for root, directories, filenames in os.walk(dir_path):
        for filename in filenames: 
            list_files.append(os.path.join(root,filename))
        for directory in directories:
            list_dir.append(os.path.join(root, directory))
                
    if files_only:
        return list_files
    else:
        return list_files, list_dir
            
    
def read_config(filename):
    """
    Parse config yaml file
    
    Args:
        filename:``str``
            path of config file
            
    """
    
    with open(filename, 'r') as stream:
        try:
            config = yaml.load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)