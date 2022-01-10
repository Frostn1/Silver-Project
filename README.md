# Silver Project
Data language used to create better file formatting and dynamic usage.<br>
Its main purpose is to generalize dynamic data written and being able to export it to different file types.

## <b>Usage</b>
Git clone the files to your computer.  
Under the `src` folder you will see `main.py` file.  
Run said file using python 3.8 or higher while giving it with args a file to compile.

## <b>Docs</b>
The Silver Language is focused on the data itself and how we can manipulate and rewrite it in different ways.

### Structs
You can create various structs that can represents chunks of different data, and have it classified as one unit.
For example we can create a Person struct
```go
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

## <b>Milestones</b>
[x] Data structs<br>
[x] Ano data<br>
[x] Export to json<br>
[x] Constant data<br>
[ ] Delta Calculation<br>
[ ] Data arrays<br>

