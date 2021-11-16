
from cpcli.cpTests import cpTest

@cpTest
async def buildADocument(config, nc) :
  print("This is how to build a ConTeXt document...")

  # send NATS message directly to context-chef to build a document
  print("Sending build message...")
  await nc.sendMessage("build.from.cLogic", {
    'name' : "cLogic",
    'path' : "~/GitTools/computePods/tests/data/majorDomo/cLogic/doc",
    'doc'  : 'cLogic.tex'
  })

  # listen for "done" reply
  print("Listenting for done reply...")

  # check that the required *.pdf file has been rsynced back to user's
  # directory.
  print("Checking for *.pdf file...")