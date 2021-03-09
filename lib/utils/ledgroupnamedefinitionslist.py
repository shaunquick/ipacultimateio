# Copyright 2021-2021 Shaun Quick
# Copyright 2021-2021 contributors
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# This is a common module that parse the LedGroupNameDefinitions.json file
# that resides in the data folder and holds the list in memory for use
# by other modules



import json
from importlib import resources

from ..common.globalvar import MAX_LEDS

LED_GROUP_DEFINITIONS = []
LedGroupDefinitionsFileFound = True


def InitLedGroupNameDefinitionsList():
# Load the definitions file, validate it and keep the list in memory for later use
    global LED_GROUP_DEFINITIONS
    global LedGroupDefinitionsFileFound
    
    try :
#    with open("LedGroupNameDefinitions.json", "r") as read_file:
        with resources.open_text("data", "LedGroupNameDefinitions.json") as read_file:
            filecontent = read_file.read()
    except FileNotFoundError as err:
# the LedGroupNameDefinitions.json is not found - the flag is set to False which will be used IF the input script tries to use a 'LedGroupName' coommand
        LedGroupDefinitionsFileFound = False
    except Exception as err:
        raise Exception("InitLedGroupNameDefinitionsList {0}".format(err))

    if  LedGroupDefinitionsFileFound:
        LED_GROUP_DEFINITIONS = json.loads(filecontent)
        try:
            _isValidLedGroupNameDefinitions(LED_GROUP_DEFINITIONS)
            
        except Exception as err:
            raise Exception("InitLedGroupNameDefinitionsList(): LedGroupNameDefinitions.json not in expected format: {0}".format(err))

    return(LED_GROUP_DEFINITIONS)

def IsLedGroupNameDefinitionsFileFound():
    global LedGroupDefinitionsFileFound
    return(LedGroupDefinitionsFileFound)

def GetLedGroupNameDefinitions():
    global LED_GROUP_DEFINITIONS
    return(LED_GROUP_DEFINITIONS)

def _isValidLedGroupNameDefinition(LedGroupNameDefinition):
# validate the  definition    
    if not LedGroupDefinitionsFileFound : raise Exception("LedGroupNameDefinitions.json did not load - cannot use LedGroupNames")
    
    if "LedGroupName" in LedGroupNameDefinition:
        if not "LedNrRGB" in LedGroupNameDefinition:
            raise Exception("LedNrRGB name not found")
        else:
            if type(LedGroupNameDefinition["LedNrRGB"]) is not list :
                raise Exception("LedNrRGB not a list: {0}".format(LedGroupNameDefinition))
            if len(LedGroupNameDefinition["LedNrRGB"]) < 3:
                raise Exception("LedNrRGB expecting at least 3 values: {0}".format(LedGroupNameDefinition))
            for LedNr in LedGroupNameDefinition["LedNrRGB"]:
                if not (LedNr  >= 0 and LedNr  < MAX_LEDS) :
                    raise Exception("LedNr not between 0 and 95: {0}".format(LedGroupNameDefinition))
            
    return (True)

def _isValidLedGroupNameDefinitions(LedGroupNameDefinitions):
# validate the  definitions file content 
    if not LedGroupDefinitionsFileFound : raise Exception("LedGroupDefinitions.json did not load - cannot use LedGroupNames")
    
    if type(LedGroupNameDefinitions) is not list: raise Exception("LedGroupNameDefinitions is not a list")
    for LedGroupNameDefinition in LedGroupNameDefinitions:
        try:
            _isValidLedGroupNameDefinition(LedGroupNameDefinition)
        except Exception as err:
            raise Exception("Led Group Name Definition Invalid:{0}: {1}".format(LedGroupNameDefinition, err))        
    return(True)

if __name__ == '__main__':
    pass