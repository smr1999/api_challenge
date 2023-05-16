# api_challenge
An api challenge project

In this project, we have three main sections.
1. User
2. Ad
3. Commenting

---

In this project each user can register an account wih their username(email) and password. Then login in the website and get an access token and also refresh token.

This user can also logout and revoke his/her token and save revoked token in the redis database.

After the user authenticated, this user can create an ad, modify it and also delete it.

Each user in this system can comment on each ad once.

---

## Installation steps
**Make sure that postgresql installed in user system and also can change connection string in the .env file. Also install redis and use port 6379 for it.(Needs to logout the user)**

1. git clone [https://github.com/smr1999/api_challenge.git](https://github.com/smr1999/api_challenge)
2. initalize an virtual enviroment 
3. pip install -r requirements.txt
4. Run command `flask db init`
5. Also run Command `flask db migrate`
6. And also run Command `flask db upgrade`
4. flask run (project default run on `localhost:5000` address)
---

You can visit *swagger-ui* in `localhost:5000/swagger-ui`

Also *rapid_doc* exists in `localhost:5000/rapid_doc`

---

<sup>Regards rouzegar</sup>