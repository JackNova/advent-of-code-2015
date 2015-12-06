# Install Mono

> brew update && brew install mono

# SublimeText Build System for C#

tools/build system/new

{
    "shell": true, 
    "cmd": ["mcs $file ; mono $file_base_name.exe"], 
    "selector": "source.cs"
}