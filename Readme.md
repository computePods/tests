# ComputePods tests

A collection of end-to-end tests for the ComputePods project.

These tests use the `cpcli` tool in "tester" mode (`--tester`) to make
requests on a local MajorDomo. These requests are essentially the same as
a user might make using the `cpcli` command line tool or web interfaces.

The JSON results are then compared with the expected result stored in each
test.

As with any `cpcli` command, tests can be either a Python function
decorated as a `@click.command`, or, alternatively, a test can be a YAML
file which has the following entries:

```yaml

testName: <aTestName>
request:
  method: <GET>
  url: <anInterfaceFastAPIPath>
validate: <aCPInterfacesPythonPackage>
expected:
  ...<<the expected JSON structure as YAML>>...

```

