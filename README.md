![GitHub Logo](/images/Silver-Logo-2.jpg)


# Silver Project
Data language used to create better file formatting and dynamic usage.<br>
Its main purpose is to generalize dynamic data written and being able to export it to different file types.

There is a current updated syntax highlighter for the language for vs code.
You can find it at - https://github.com/Frostn1/SilverProject-SyntaxHighlight -.

## <b>Usage</b>
Git clone the files to your computer.
```
git clone "https://github.com/Frostn1/Silver-Project"
```
Cd inside of the repo folder itself
```
cd Silver-Project
```
Under the `src` folder you will see `app` folder, this folder holds all of the core code for Silver.<br>
Inside of it there will be a `main.py` file, which can be used to run Silver on any <b>file</b> of you choosing.  
Run said file using python 3.8 or higher while giving it ( with args ) a file to compile.<br>

For block testing of folders check [Silver's Test-Agent](README.md#Data%20Arrays).

## <b>Testing</b>
As of v1.0.1 Silver has an automated tester.
In order to run it, you will need to run

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
The keen eye of you have noticed that the `age` field is a bit special, as it holds a delta, i.e. ( `=> (CurrentYear - Person.year of birth) ).`<br><br>
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
`Note:`
So far Silver doesn't support multi dimensional data arrays, but it is WIP, so you may hope to see it in future updates coming to Silver. 


## <b>Milestones</b>
### Current
- [ ] Multi Dimensional Data arrays
- [ ] Reference Past Keys
- [ ] Boolean data type
- [ ] Export to definitions < Code Info >
- [x] Silver Auto Tester

### Done

- [x] Data structs<br>
- [x] Export to json, yaml, raw<br>
- [x] Constant data<br>
- [x] Delta Calculation<br>
- [x] Data arrays<br>

## <b>Similar Projects</b>
- <i><b>The Dhall Configuration Language</b></i><br>
    At - https://github.com/dhall-lang/dhall-lang/blob/master/README.md -