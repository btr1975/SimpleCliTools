# Python Script: SimpleCliTools

## Written By: Benjamin P. Trachtenberg 
### If you have any questions e-mail me

### Contact Information:  e_ben_75-python@yahoo.com

### LinkedIn: [Ben Trachtenberg](https://www.linkedin.com/in/ben-trachtenberg-3a78496)
### Docker Hub: [Docker Hub](https://hub.docker.com/r/btr1975)

### About

This script is various tools, to compare, some Cisco Network Configurations

### Features
1. Prefix-List Diff
    * The Differ does not look at sequence numbers, the name, or popper ordering.  It compares the permit, and deny 
    data.  Allowing you to compare for content of the list.
    
2. Standard ACL Diff
    * The differ dose not look at ACL ordering.  It compares permit, and deny data.  Allowing you to compare content 
    of the ACL.
    
3. Convert a Standard ACL to a Prefix-List for route filtering
    * Takes a standard ACL, and converts it to a Prefix-List for filtering routes on a routing protocol.

4. A line by line file differ
    * Takes 2 text files, and outputs a Excel spreadsheet with a highlighted diff.

5. A config splitter
    * Takes a show run, and splits the config for seeing specific sections.
    * This is still under development.

6. Make a NX-OS style mcast config from a IOS show run ACL
    * Takes a show ip access-list from a IOS device, and converts it to a NX-OS style config.
    * Has the option to only convert matches lines.

7. IP Address tools
    * Takes a IP Address in the following format X.X.X.X/X, and gives you all possible subnets it could be in.
    * Takes a IP Address in the following format X.X.X.X/X, and gives you all possible hosts in the range.