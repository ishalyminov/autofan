heroku create --stack cedar-14 --buildpack https://github.com/heroku/heroku-buildpack-chromedriver.git
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome 

