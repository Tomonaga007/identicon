# py_identicon

GitHub-style identicons as PNGs JPG.

![Alt text](examples/example1.png?raw=true "Title")
![Alt text](examples/example2.png?raw=true "Title")
![Alt text](examples/example4.png?raw=true "Title")
![Alt text](examples/example5.png?raw=true "Title")

Simple module to create GitHub-style square identicons. Supports PNG and JPG. Uses md5 hash algorithm to produce images.   

## Usage
### Comand-line usage 


    usage: identicon.py [-h] [--string STRING] [--size SIZE] [--blocks BLOCKS]
                    [--color COLOR [COLOR ...]]
                    [--background BACKGROUND [BACKGROUND ...]]
                    [--border BORDER] [--not_symetrical] [--save SAVE]
### Arguments

| Short   | Long         | Default|Description                                |
| --------|:----------------| -------------  |-------------------------------------------|
|     -h  | --help          |             | Show help                                 |
|         | --string        |random srting      |Hashed string is used to generate identicon|
|         | --size          |   400 | Output image size in pixels (size x size)|
|         |--blocks         |5      | Number of blocks(squares) in row |
|         | --color         |color based on hash| 3(RGB) or 4(RGBA) integers. Color of blocks
|         | --background    | white| 3(RGB) or 4(RGBA) integers. Background color
|         | --border        | 0| Border around image in pixels
|         | --not_symertical| False| Bool flag, if set to True image won't be symetric
|         | --save          | none| name with extension(.png, .jpg, .jpeg for saved image, if not specified image will be displayed notsaved
