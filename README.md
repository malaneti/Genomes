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

Landingpage:
![screen shot 2016-06-06 at 20 10 44](![screen shot 2016-06-06 at 20 10 44](screenshot1.png))
Login:
![screen shot 2016-06-06 at 20 11 19](https://cloud.githubusercontent.com/assets/10008938/15844918/2796150a-2c23-11e6-98ab-8042cbf48ea1.png)
Authentication:
![screen shot 2016-06-06 at 20 08 50](https://cloud.githubusercontent.com/assets/10008938/15844927/334263b8-2c23-11e6-94f4-d9a040efdfd1.png)
Chromosomes:
![screen shot 2016-06-06 at 20 10 18](https://cloud.githubusercontent.com/assets/10008938/15844922/2cdbb236-2c23-11e6-9f2d-4adf4d9b0f79.png)
Bubble Map :
![screen shot 2016-06-06 at 20 09 39](https://cloud.githubusercontent.com/assets/10008938/15844923/2f5013c2-2c23-11e6-8608-607eff0c4da8.png)

===============
## Installation
Please install Python/Flask dependencies within the root directory
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

You're good to go. Start the server with:
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
## Architecture
### High Level Architecture
![](http://i64.tinypic.com/2zpp661.png)

### Database Schema
Database in Postgres, using SQLAlchemy
![](http://i68.tinypic.com/23i6plz.jpg)

======
## API
##### Public End Points
|Description|Endpoint|
|---|---|
|[Log-in OAuth](#get-receive_code)|GET /receive_code/|
|[Log-in Demo](#post-demo)|POST /demo/|
|[Log-out current user](#post-logout)|POST /logout|
|[Get User Info](#get-userbasicinfo)|GET /user/basicinfo/|
|[Get User's SNP Data](#post-usersnpinfo)|POST /user/snpinfo/|

##### Admin Only
|Description|Endpoint|
|---|---|
|[Access to 23&Me Individual data](#get-1useruserid)|GET /1/user/:userID|
|[Access to 23&Me Genotype data](#get-1genotypeuserid)|GET /1/genotype/:userID|
|[Access to 23&Me Relative data](#get-1relativesuserid)|GET /1/relatives/:userID|



## `GET /receive_code/`

Redirects back to server after acquiring access token after User approves OAuth permissions

### Example Request
```bash
curl -H 'Accept: auth-url' -H 'Authorization: OAuth <access_token>' \
-X GET https://BASE_API_URL + 
{
  'client_id': CLIENT_ID,
  'client_secret': CLIENT_SECRET,
  'grant_type': 'authorization_code',
  'code': request.args.get('code'),
  'redirect_uri': REDIRECT_URI,
  'scope': DEFAULT_SCOPE
}
```


## `POST /demo/`

Allows visitors to access site as a demo user

### Example Request
```bash
{
	'demo_profile_id': 'demo_id',
	'demo_first_name': 'Foo',
	'demo_last_name': 'Bar'
	'demo_data': [
		'sex': 'm/f',
		'rs_id': 'demo_basepairs',
		...
	]
}
```


## `POST /logout/`

Logs out user from session and clears cookies/cache

### Example Request
```bash
{
	'user_profile_id': 'profile_id',
	'headers': {
		'cookie': {
			'token': 'asj238xlzhs_uw28hzbhslsm8es9'
		}
	}
}
```

## `GET /user/basicinfo/`

Fetches the basic information of the current authorized user

### Example Response
```json
{
  "user": {
  	"profile_id": 1738,
    "first_name": "Foo",
    "last_name": "Bar",
    "location": "United States",
    "picture_url": ""
    }
}
```

## `POST /user/relativesinfo/`

Gathers information about the current user's relatives

### Example Request
```bash
{
	'user_profile_id': 'profile_id',
	'headers': {
		'cookie': {
			'token': 'asj238xlzhs_uw28hzbhslsm8es9'
		}
	}
}
```

### Example Response
```json
{
	"user_profile_id": "profile_id",
	"relatives": [
		{"relative1": {
			"first_name": "Foo",
			"last_name": "Bar",
			"sex": "m/f",
			"residence": "California",
			"similarity": 0.25,
			"maternal_side": "False",
			"paternal_side": "True",
			"birth_year": 1992,
			"relationship": "Brother",
			"birthplace": "United States",
			"ancestry": "Northwestern Europe",
			"picture_url": ""
		}},
		{"relative2": {
			"first_name": "Foo2",
			"last_name": "Bar2",
			"sex": "m/f",
			"residence": "California",
			"similarity": 0.25,
			"maternal_side": "False",
			"paternal_side": "True",
			"birth_year": 1990,
			"relationship": "Sister",
			"birthplace": "United States",
			"ancestry": "Northwestern Europe",
			"picture_url": ""
		}},
		...
	]
}
```

## `POST /user/snpinfo/`

Gathers DNA information about the current user

### Example Request
```bash
{
	'user_profile_id': 'profile_id',
	'headers': {
		'cookie': {
			'token': 'asj238xlzhs_uw28hzbhslsm8es9'
		}
	}
}
```

### Example Response
```json
{
	"user_profile_id": "profile_id",
	"body": [
		{"rs270831": {
			"title": "Lactose Intolerance",
			"dna_pair": "AA",
			"outcome": "You have a high likelihood of being lactose intolerant",
			"video": "4UvzSuP_Tzd"
		}},
		{"rs812202": {
			"title": "Cilantro",
			"dna_pair": "GG",
			"outcome": "You are likely to experience a dislike for cilantro, may taste like soap",
			"video": "TZs309snmr"
		}},
		...
	]
}
```

## Admin Routing

## `GET /1/user/:userID`

Requests user's information upon login from 23andMe's designated endpoint

### Example Request
```bash
curl -H 'Accept: %s%sBASE_API_URL + '/1/user/' + 'user_id'' -H 'Authorization: 'Bearer %s' % access_token' \ -X GET https://auth-url/1/user?email=true
```

## `GET /1/genotype/:userID`

Requests user's unique genotype information upon login from 23andMe's designated endpoint

### Example Request
```bash
curl -H 'Accept: %s%sBASE_API_URL + '/1/genotype/' + 'user_id'' -H 'Authorization: 'Bearer %s' % access_token' \ -X GET https://auth-url/1/genotype/
```

## `GET /1/relatives/:userID`

Requests user's relatives' information upon login from 23andMe's designated endpoint

### Example Request
```bash
curl -H 'Accept: %s%sBASE_API_URL + '/1/user/' + 'user_id'' -H 'Authorization: 'Bearer %s' % access_token' \ -X GET https://auth-url/1/relatives
```




