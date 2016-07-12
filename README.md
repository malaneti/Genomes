# Chroma


## Introduction 
Chroma allows users to click on their colorful chromosomes and view information about their genetic data, specifically focused on health risks.
It then directs users to a bubble map, showing them visually which health risks they may be more susceptible to, and tips on lifestyle changes.
<hr>
## Table of Contents

  - [Example](#example)
  - [Installation](#installation)
  - [Technologies](#technologies)
  - [Architecture](#architecture)
  - [API Endpoints](#api)
 
 

==========
## Usage

<img width="1280" alt="screenshot1" src="https://cloud.githubusercontent.com/assets/17863675/16776714/84de5b82-481b-11e6-894b-3ab9012db72d.png">
<img width="1279" alt="screen shot 2016-07-11 at 5 10 42 pm" src="https://cloud.githubusercontent.com/assets/17863675/16776765/bc86a292-481b-11e6-8d95-931352b2b72b.png">
<img width="1280" alt="screen shot 2016-07-11 at 5 11 08 pm" src="https://cloud.githubusercontent.com/assets/17863675/16776771/bffef7d0-481b-11e6-8aba-8b832f775ee2.png">
<img width="1280" alt="screen shot 2016-07-11 at 5 31 12 pm" src="https://cloud.githubusercontent.com/assets/17863675/16776729/998b1c5a-481b-11e6-8ad5-fab097f9d14c.png">
<img width="1280" alt="screen shot 2016-07-11 at 5 31 21 pm" src="https://cloud.githubusercontent.com/assets/17863675/16777096/14a57074-481d-11e6-989f-c9cc084e3a79.png">
<img width="1278" alt="screen shot 2016-07-12 at 10 49 41 am" src="https://cloud.githubusercontent.com/assets/17863675/16777487/9c8d198c-481e-11e6-87b6-1db447033711.png">
<img width="1280" alt="screen shot 2016-07-12 at 10 50 38 am" src="https://cloud.githubusercontent.com/assets/17863675/16777497/a7231efa-481e-11e6-8bb5-e60e7f91f365.png">
<img width="1280" alt="screen shot 2016-07-12 at 9 51 34 am" src="https://cloud.githubusercontent.com/assets/17863675/16776796/d5328586-481b-11e6-9316-a289b550fd54.png">


===============
## Installation
Install Python/Flask dependencies within the root directory
```
$ virtualenv .
$ source bin/activate
$ pip install -r requirements.txt
```

Next, install the client-side dependencies
```
$ sudo npm install -g bower
$ bower install
```
**For testing**
```
$ npm install
```

Start server:
```
$ npm start
```

===============
## Technologies
Front-end
- AngularJS 
- D3.js

Back-end
- Python/Flask
- PostgreSQL
- SQLAlchemy

Automation
- Grunt

===============
