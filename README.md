# Silver Project
Data language used to create better file formatting and dynamic usage.

## Usage
Git clone the files to your computer.  
Under the `src` folder you will see `main.py` file.  
Run said file using python 3.8 or higher while giving it with args a file to compile.

## Example Code
```go
( link : 'code.nova' )
< person:
    first name,
    last name,
    year of birth,
    age => calAge(currentYear | person.year of birth),
    email
>
{
    'currentYear' ? 2021,
    ano ? person[first name='Jane' |  last name='Doe' | age=21 | email='hello@bla.com'],
    ano ? person[first name='John' |  last name='Doe'| age=34 | email='somethinginc@atcooli.com'],
    ano ? person[first name='Larry' | last name='Bird' | email='something@blail.org' | year of birth=1986],
    'lebron' ? person[first name='lebron' |  last name='james'| age=36 | email='leking@gmail.com']
}

#export json
```
Compiles to

```json
{
    "ano": [
        {
            "first name": "Jane",
            "last name": "Doe",
            "age": "21",
            "email": "hello@bla.com",
            "year of birth": ""
        },
        {
            "first name": "John",
            "last name": "Doe",
            "age": "34",
            "email": "somethinginc@atcooli.com",
            "year of birth": ""
        },
        {
            "first name": "Larry",
            "last name": "Bird",
            "email": "something@blail.org",
            "year of birth": "1986"
        }
    ],
    "currentYear": 2021,
    "lebron": {
        "first name": "lebron",
        "last name": "james",
        "age": "36",
        "email": "leking@gmail.com",
        "year of birth": ""
    }
}
```
