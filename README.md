VANELLOPE
=========

vanellope is a publishing engine (just a blog software) named after the adorable Disney character [Vanellope von Schweetz](http://disney.wikia.com/wiki/Vanellope_von_Schweetz). It it is designed to be deployed with a minimal effort.

## DEMO

```
pip install vanellope
vanellope --port=8080
```

There it is ! A brand new app is running on port 8080. You can run on port 80 or put it behind a reverse proxy like Nginx. In either way you work here is done.

** REMEMBER **, after vanellope started, it will look for a `content` directory in the current location. If the directory not exist it will create one and put every thing it generated in it.

And one more thing, a newly created vanellope instance is completely vulnerable like every new born baby. You should visit `/welcome` page signup as administrator immediately after the instance start running. The `/welcome` page can be used only once.
