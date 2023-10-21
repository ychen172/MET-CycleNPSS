@call setupnpss.bat
py parse_yaml.py
@pushd ExampleRuns
runnpss SimpleTurbojet.run
@popd