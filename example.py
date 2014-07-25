#!/usr/bin/python

import NIOS

# Enter "https://x.y.z/"
nios_server = NIOS.prompt_input(
    "Enter NIOS server",
    "https://gridmaster.example.com/"
)

s = NIOS.NIOS(nios_server)
s.prompt_credentials()
