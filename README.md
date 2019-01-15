# CV generator
This is an attempt to make a "git-like" curriculum generator.
It has the generator [cvCommit.py](cvCommit.py) and the viewer [index.html](front-end/index.html) witch is a front-end-only web.

## Usage
The usage is as much git-like as possible.

To init a new cv:
````bash
python cvCommit.py init 
```` 
It will create an empty repository with the default master branch

To generate a new node:
````bash
python cvCommit.py commmit -m "message" 
```` 
To checkout on an existing node to make a fork:
````bash
python cvCommit.py checkout commit_index 
```` 
and the new nodes will be created from the one given

To create a new branch:
````bash
python cvCommit.py checkout -b "branch name" 
```` 

To checkout on an existing branch:
````bash
python cvCommit.py checkout "branch name" 
```` 

To view the result you must type:
````bash
python cvCommit.py export
```` 
And open the viewer [index.html](front-end/index.html) on your browser