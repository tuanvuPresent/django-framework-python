# django-framework-python
- [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
- [https://docs.djangoproject.com/en/3.0/](https://docs.djangoproject.com/en/3.0/)
# use 
step 1: install docker and docker-compose

- [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
- [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)

step 2: Build code with docker compose
```
docker-compose up --build
```

step 3: Create folder logs tại root project

step 4: Run
```
- run server 0.0.0.0:8888

- run phpmyadmin 0.0.0.0:8088
```

# social-oauth2
```To get info user``` 
# GITHUB
- access_token_github = 'abc'
- headers = {'Authorization': 'token {}'.format(access_token_github)}
- url1 = 'https://api.github.com/user'
- url2 = 'https://api.github.com/user/email'
- res1 = requests.get(url1, headers=headers)
- res2 = requests.get(url2, headers=headers)
- print('github', res1.json())
- print('github', res2.json())

# FACEBOOK
- url = 'https://graph.facebook.com/v3.2/me'
- access_token_facebook = 'abc'
- params = {'access_token': access_token_facebook}
- res = requests.get(url, headers=headers, params=params)
- print('facebook', res.json())

# GOOGLE
- url = 'https://www.googleapis.com/oauth2/v3/userinfo'
- access_token_google = 'abc'
- headers = {'Authorization': 'Bearer {}'.format(access_token_google)}
- res = requests.get(url, headers=headers)
- print('google', res.json())

# Third-party application permissions for mail 
- https://myaccount.google.com/lesssecureapps