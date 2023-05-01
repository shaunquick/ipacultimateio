# __Init__ for package lib/utils

#from .buttonname import InitButtonNameModule
from .ledgroupnameslist import InitLedGroupNamesList
from .ledgroupnamedefinitionslist import InitLedGroupNameDefinitionsList
#from .ledcurrentstateslist import InitLedStatus
#from .lednrlist import InitLedNrList

try:
    LedGroupDefsList = InitLedGroupNameDefinitionsList()
    InitLedGroupNamesList(LedGroupDefsList)
#    InitLedStatus()
#    InitLedNrList()

#    print("Just L:oaded the button names: {0}".format(BUTTON_NAMES))
except Exception as err:
    print("package lib.utils __init__ Error {0}".format(err))
