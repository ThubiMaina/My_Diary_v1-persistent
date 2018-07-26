# My-Online-Diary
___
![diary](https://user-images.githubusercontent.com/31989539/42674910-477c815c-867a-11e8-9241-3c76d5978f7a.jpg)

___

## My Online Diary

A diary is a record of personal experiences, thoughts and feelings. A diary can be considered as a friend you talk to and thats why most start with dear diary, . One can talk about people they meet, exciting things we do , memories of places basically every thing we encounter.
#### Note:
* Should be in first person
This app allows you to plan for your day and record all memories
___
### Prerequisites

* Python 3.4 and above
____

### Installation
create a directory MyDiary
```
$  mkdir MyDiary
```

clone the repo:git
```
$  git clone https://github.com/ThubiMaina/My-Online-Diary.git
```
and cd into the folder:
```
$ cd MyDiary
```
create a virtual environment for the project.
```
$ virtualenv <virtualenv-name>
```
and activate virtual environment
```
$ cd MyDiary\virtualenv-name\Scripts\activate
```

Run the command `$ pip install -r requirements.txt` to install necessary libraries.

### Run 

Run ` db\db_001.py ` to create tables 

To test our project on your terminal run 

* ```set FLASK_APP=run.py``` on windows
or
* ```export FLASK_APP=run.py``` on a unix environment

then

``` flask run ```
### Running the tests 

To run tests on your terminal run 

* ```pytest .\<file-name>``` 
* ```py.test --cov=app``` to get the coverage


### Api Endpoints

| Endpoint | Functionality | Method | Authorization |
| -------- | ------------- | --------- | -------------- |
| /api/auth/v1/register | Creates a user account | POST | FALSE |
| /api/auth/v1/login | Logs in a user | POST | TRUE |
| /api/user/v1/entries  | Adds a new diary entry | POST | TRUE |
| /api/user/v1/entries  | Gets all  diary entries for a user| GET | TRUE |
| /api/user/v1/entries/<entry_id>  | Gets a single entry for a user| GET | TRUE |
| /api/user/v1/entries/<entry_id> | Updates an entry | PUT | TRUE |
|  /api/user/v1/entries/<entry_id> | Remove a diary entry | DELETE | TRUE |
