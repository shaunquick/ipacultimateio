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

# This module provide some core functions, such as initiale the board
# for use by other modules
# Basic Board information can also be returned by the following
# functions

import usb.core
import usb.util
import usb.control

from ..common.common_lib import my_func_name
from ..common.common_lib import isDebugOn


UM_VENDOR_ID_LIST = [ 0xD209 ] # There should only be one Vendor - but there may be an issue when setup as XInput
UM_PRODUCT_ID_LIST = [ 0x0410, 0x0411, 0x0412, 0x0413 ]

UM_XINPUT_VENDOR_ID_LIST = [ 0X045e ]
UM_XINPUT_PRODUCT_ID_LIST =[ 0X028e ]



def _IsValidIpacUltimateDevice(DeviceID, xinput_flag=False):
    FUNC_NAME=my_func_name()
    if isDebugOn(): print(FUNC_NAME)



# Verify the board is an iPAC Ultimate IO
    if (DeviceID != None and DeviceID.idProduct in UM_PRODUCT_ID_LIST and DeviceID.idVendor in UM_VENDOR_ID_LIST ):
        return (True)
    elif xinput_flag and DeviceID.idProduct in UM_XINPUT_PRODUCT_ID_LIST and DeviceID.idVendor in UM_XINPUT_VENDOR_ID_LIST:
        return (True)
    else:
        return(False)