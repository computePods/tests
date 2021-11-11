# This is ConTeXt ComputePods Chef plugin

# It provides the Chef with recipes on how to typeset ConTeXt documents....

import cpchef.plugins
import yaml

def registerPlugin(config, natsClient) :
  print("Registering ConTeXt TEST plugin via registerPlugin")

  @natsClient.subscribe("silly.>")
  async def dealWithSillyTestMessages(subject, data) :
    print(type(subject))
    print(subject)
    print(type(data))
    print(data)
    # do something!!!
    # If we are *inside* an instance method.... we have access to self.
    # which we *will* need to send messages using the natsClient


  print("Finished registering Context Plugin")
