<img align="left" width="190" src="/images/Silver-Logo-2.jpg"/>


<h1>Silver Project</h1>

### Data language used to create better file formatting and dynamic usage.<br><br>![Language](https://img.shields.io/badge/language-Python-6A7FC8.svg?style=for-the-badge)

--- 

* [The Language](#the-language)<br>
* [Installation](#installation)
* [Testing](#testing)
* [Documentation](#docs)
    * [Structs](#structs)
    * [Data Arrays](#data-arrays)
    * [Exports](#exports)
* [MileStones](#milestones)
* [Similar Projects](#bsimilar-projectsb)

---


## <b>The Language</b> 

Its main purpose is to generalize dynamic data written and being able to export it to different file types.

There is a current updated syntax highlighter for the language for vs code.
You can find it at - https://github.com/Frostn1/SilverProject-SyntaxHighlight -.

## <b>Installation</b>
Git clone the files to your computer.
```
git clone "https://github.com/Frostn1/Silver-Project"
```
Cd inside of the repo folder itself
```
cd Silver-Project
```
Make sure you have python 3.8 or higher installed, in order to run the code.<br>

Under the `src` folder you will see `app` folder, this folder holds all of the core code for Silver.<br>
Inside of it there will be a `main.py` file, which can be used to run Silver on any <b>file</b> of you choosing.  
As follows ( while sitting in main dir ):
```
py -m src.app.main <FILE>
```
For block testing of folders check [Silver's Test-Agent](#testing).

## <b>Testing</b>
As of v2.0.0 Silver has an automated tester.
In order to run it, you will need to run `test.py`, as follows ( while sitting in main dir ):
```
py -m src.test.test --test [FOLDER | FILE ...]
```

Silver's testers will run on the folder/files given and return an output based of each case return, e.g.
```
D:\Programming\Projects\Silver-Project(develop)> py -m src.test.test --test assets/
Running tests for Silver v1.0.0
Total of 1 test cases given

assets/const.si ... Passed; in 0.001s
assets/data_arrays.si ... Passed; in 0.000s
assets/person.si ... Passed; in 0.002s
assets/struct.si ... Passed; in 0.000s

Test ended - 4 tests

4 Passed
Average time of 0.001
```

## <b>Docs</b>
The Silver Language is focused on the data itself and how we can manipulate and rewrite it in different ways.

### <b>Structs</b>
You can create various structs that can represents chunks of different data, and have it classified as one unit.
For example we can create a Person struct
```js
< Person:
    first name,
    last name,
    age => (CurrentYear - Person.year of birth),
    year of birth
>
```
As you can see, we created a new struct named `Person` that holds 4 fields.<br>
The fields names can be what ever you want, and don't have any limitations, this make is so you can have spaces in the name too !<br><br>
The keen eye of you have noticed that the `age` field is a bit special, as it holds a delta, i.e. ( `=> (CurrentYear - Person.year of birth)` ).<br><br>
As this language is dynamic and wants to take the load off the user itself, when one or more of the fields is not given when creating a new struct, the lang will try and replace it with a new value, either using a delta or a blank value.<br>
This feature makes it that the structure of the final file export is kept and can be safely read by a 3rd party.

As we can see age field's delta is subtracting the structs in question `year of birth` from an identifier `CurrentYear`.<br>
`CurrentYear` is not a special identifier, but it is just a future reference to a constant that will be presentetd in the chunk part of the code file.<br>
When creating a new Person struct, all of the fields will be initiated with the value given, but if the `age` field will be left empty, the delta will execute with the new data it gathered and create an updated value for it.<br><br>

We can see the delta power in action in the following example: 
```js
// Person.si

< Person:
    first name,
    last name,
    age => (CurrentYear - Person.year of birth),
    year of birth
>

{
    'CurrentYear' : 2022,
    'John' : Person[first name='John' | last name= 'Doe' | year of birth=1998]
}


export json
export yaml
export raw
```

Which will export to .json, .yaml .txt files:
```json
// Person.json
{
    "CurrentYear": 2022,
    "Data": {
        "first name": "John",
        "last name": "Doe",
        "age": "24",
        "year of birth": "1998"
    }
}
```
```yaml
// Person.yaml
- CurrentYear: 2022
- John: 
    - first name: John
    - last name: Doe
    - year of birth: 1998
    - age: 24
```
```js
// Person.txt
{
	CurrentYear :  2022,
	John : [ John, Doe, 1998, 24 ]
}
```

As we can see, the Silver code is exported to different file types, while having a special format that related to the file type itself, while that data is up to date with the delta calculation that Silver could deduct.<br>

Futher more, this might have gone unnoticed but Silver will also keep the formatting of struct's keys order when exporting to another file type, as you can see all the key-value pairs in the json file are all have the same order for key-value pair, for better code visibility.

### <b>Data Arrays</b>

As pretty much any developed programming language has arrays, Silver has its own arrays too.<br>
Here we call them `data arrays` ( how unique I know ), as they entire language is centerly on the data itself.<br>
They can be initiated with a simple brackets and values inside same as any other language you might know, the only difference being is that instead of separating the values in the array with `,` ( i.e. commas ), in Silver we just separate with spaces between value to value.<br>
Not following this structure won't always lead to a visible error, as Silver will try and solve your mistake for you by continuing to parse through the data and coming up with a viable export.<br>
Heads up, it won't always be a pretty one...<br>

For example this Silver code, which clearly has an error
```js
{
    'People' : [ "John"56"Name"]
}

export json
export yaml
export raw
```
Will lead to a crash when Silver will try to export the code to json, with the following error:<br>
```SyntaxError: invalid syntax - {"People":["John",56"Name"]}```<br>
As we can see Silver fails to find the values in the data arrays, because the had no spaces between values, after all there is a limit to Silver's power.<br>

Further more, exporting to yaml and raw for example, won't make Silver crash, but as Silver can't find the values by himself, the solution it will make for the export code won't be a clean\good one.<br>
Just to show the yaml, raw exports for reference:
```js
// Raw export code
{
	People : [ "John", 56"Name"]
}
```
```yaml
// Yaml export code
- People: 
    - John
    - 56Name
```
----
<br>
As the Silver language is all about being dynamic and taking the load of the user, all of the data arrays can hold any value that is present in the current code ( i.e. created structs ), and/or primitive types that are present in the language itself ( string, numbers ).

Example for the capabilities of the data arrays in Silver:
```js
< Person:
    first name,
    last name,
    age => (CurrentYear - Person.year of birth),
    year of birth
>

{
    'CurrentYear' : 2022,
    'Data' : ["Current Date" "Hello world"  Person[first name='John' | last name= 'Doe' | year of birth=1998] 2017]
}
```

As Silver supports data arrays, ( which are close to how they work in other languages ), it also supports data arrays as values in another array, aka multi dimensional arrays.<br>
It works the same as any other type of value in Silver so far ( Text, Number, Boolean etc... ), and can still be exported to all supported file types.<br>
A simple example of multi dimensional arrays in Silver:
```js
{
    'Dates' : [ '11.7.2004' ["Silver" [ 17 False] True 12.2 ] 2021],
}

export json
export base
```

Which will export to the following json code:
```json
// Json Export Code
{
    "Dates": [
        "11.7.2004",
        [
            "Silver",
            [
                17,
                false
            ],
            true,
            12.2
        ],
        2021
    ]
}
```

And to the new type export ( also known as `base` exporting):
```haskell
// Base Export Code
[ Dates [ Text,  [ Text,  [ Number, Bool ] : List, Bool, Number ] : List, Number ] : List ]
```

### Exports
As the languages progresses it will have more and more official implemented export file extensions, which may include : json, yaml, raw, base etc...<br>
Inorder to use each export ( including future ones that are not implemented at this point of writing ), you would just need to use the `export` keyword and the file type you want to export to.<br>
This will create an output file, which will hold the same name as the original file name, but with a different file extension.<br>


`Note : Currently the only supported file extension for exporting are few, but in  the future we plan on implementing a way for other to create their exports, for their own file extensions, either through a specific language api, or through the language itself.<br>
Maybe through another file which will dictate how it is suppose to written in each way you can have.`

#### __Officially supported file exports by Sillver__
Side note, all of the exports will show the same example, to have some uniformity.
```js
// Example.si
< Person:
    first name,
    last name,
    age => (CurrentYear - Person.year of birth),
    year of birth
>

{
    ano : 2021,
    'CurrentYear' : 2022,
    'Data' : [True "Hello world"  Person[first name='John' | last name= 'Doe' | year of birth=1998] 2017]
}
```
- _json_
```json
// Example.json
{
    "ano": [
        2021
    ],
    "CurrentYear": 2022,
    "Data": [
        true,
        "Hello world",
        {
            "first name": "John",
            "last name": "Doe",
            "age": "24",
            "year of birth": "1998"
        }
    ]
}
```
- _yaml_
```yaml
// Example.yaml
- ano: 
    - 2021
- CurrentYear: 2022
- Data: 
    - True
    - Hello world
    - first name: John
    - last name: Doe
    - age: 24
    - year of birth: 1998
```
- _raw_
```js
// Example.txt
{
	ano : [  2021 ],
	CurrentYear :  2022,
	Data : [  True,  Hello world, [ John, Doe, 24, 1998 ] ]
}
```
- _base_<br>
Catalogs all of the key's with their values type.<br>
Can be mainly used for debugging.
```haskell
// Example.base
Person [ first name : Any, last name : Any, age : Any, year of birth : Any ] : Struct
[ ano [ Number ] : List, CurrentYear : Number, Data [ Bool, Text, Person ] : List ]
```

## <b>Milestones</b>
### Current
- [x] Multi Dimensional Data arrays
- [ ] Reference Past Keys
- [x] Boolean data type
- [x] Export to definitions < Code Info >
- [ ] Links to other .si files
- [ ] Rebase entire compiler
  - [ ] Lexer
  - [ ] Parser
  - [ ] Ast
  - [ ] Generator
  - [ ] Structs
  - [ ] Exports
  - [ ] Links
- [ ] Struct type hints
- [x] Struct Data Arrays as Structs Values

### Done

- [x] Data structs<br>
- [x] Export to json, yaml, raw<br>
- [x] Constant data<br>
- [x] Delta Calculation<br>
- [x] Data arrays<br>
- [x] Silver Auto Tester<br>

## <b>Similar Projects</b>
- <i><b>The Dhall Configuration Language</b></i><br>
    At - https://github.com/dhall-lang/dhall-lang/blob/master/README.md -


* [Back to Top](#bthe-languageb)
