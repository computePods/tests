
import asyncio
import os

from cpcli.cpTests import cpTest
from cputils.rsyncFileTransporter import RsyncFileTransporter

projectPath = "~/GitTools/computePods/tests/data/majorDomo/cLogic/doc/"
chefPath    = os.path.abspath(os.path.expanduser(
    '~/GitTools/computePods/tests/data/chefs/context/tmpDir/'
)) + os.path.sep

@cpTest
async def buildADocument(config, nc) :
  print("This is how to build a ConTeXt document...")

  workDone = asyncio.Event()

  async def doneCallback(aSubject, theSubject, theMsg) :
    print("DONE callback!")
    workDone.set()
  await nc.listenToSubject('done.build.from.cLogic', doneCallback)

  rsync = RsyncFileTransporter(config)
  if not await rsync.isSshAgentRunning() :
    if not await rsync.startedAgent() :
      print("Could not start the ssh-agent for this ComputePod")
      return

  if not await rsync.loadedKey() :
    print("FAILED to load the ssh key into the ssh-agent for this ComputePod")
    return

  print(projectPath)
  print(chefPath)

  success, stdout, stderr = await rsync.rsyncedFiles(projectPath, chefPath)
  if success :
    print("----------------------------------------------------")
    print(stdout)
    print("----------------------------------------------------")
  else :
    print(stderr)
    print(f"Could not rsync files from {projectPath} to {chefPath}")
    return

  # send NATS message directly to context-chef to build a document
  print("Sending build message...")
  await nc.sendMessage("build.from.cLogic", {
    'userName' : 'stg',
    'podName'  : 'nn01',
    'name'     : "cLogic",
    'path'     : projectPath,
    'doc'      : 'cLogic.tex'
  })

  # listen for "done" reply
  print("Listenting for done reply...")
  await workDone.wait()
  print("Heard done reply!")

  success, stdout, stderr = await rsync.rsyncedFiles(chefPath, projectPath)
  if success :
    print("----------------------------------------------------")
    print(stdout)
    print("----------------------------------------------------")
  else :
    print(stderr)
    print(f"Could not rsync files from {chefPath} to {projectPath}")
    return

  # check that the required *.pdf file has been rsynced back to user's
  # directory.
  print("Checking for *.pdf file...")