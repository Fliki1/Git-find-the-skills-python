import configparser

CONFIG = configparser.RawConfigParser()
CONFIG.read('ConfigFile.properties')


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(CONFIG.get('DatabaseSection', 'database.dbname'))

def validatePropertiesSkills():
    """ Valida i campi di ConfigFile.properties (non vuoti) """
    # for e in CONFIG. check if campi non vuoti

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    CONFIG.read('ConfigFile.properties')
    if validatePropertiesSkills():
        pass
