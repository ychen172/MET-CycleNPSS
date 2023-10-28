@call setupnpss.bat
py parse_yaml.py %1
@pushd ExampleRuns
runnpss SimpleTurbojet.run
@popd