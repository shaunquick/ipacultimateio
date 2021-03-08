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


# This is a common module that parse the LedGroupDefinitions.json file
# that resides in the data folder and extracts all the user defined
# button names. These button names are the ones that are then
# validated against when executing the command scripts.

LED_GROUP_NAMES = []

def InitLedGroupNamesList(LedGroupNameDefinitionsList):
    global LED_GROUP_NAMES
    LED_GROUP_NAMES = []
    for LedGroupNameDefinition in LedGroupNameDefinitionsList:
        if ("LedGroupName" in LedGroupNameDefinition):
            LED_GROUP_NAMES.append(LedGroupNameDefinition["LedGroupName"])

def GetLedGroupNamesList():
    global LED_GROUP_NAMES
    return(LED_GROUP_NAMES)


def _IsValidLedGroupName(LedGroupName):

    if (type(LedGroupName) is not str): raise Exception("LedGroupName not in string format")
    if LedGroupName not in LED_GROUP_NAMES: raise Exception("LedGroupName not in list of Led Group Names in definitiona file: {0}, {1}".format(LedGroupName, LED_GROUP_NAMES))
    return(True)

if __name__ == '__main__':
    pass