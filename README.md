# Blog on Flask

This is a simple blog application powered by Flask 🐍
The app was created by following [a great tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) from Miguel Grinberg.

Flask Blog provides a docker setup with two environments:

```bash
./start_development_env.sh  # includes auto applying of changes
./start_production_env.sh
```

Kubernetes is used to define a resilent architecture for the Flask Blog.

Tech Stack:

- Python 3.8+
- Flask
- SQLite via SQLAlchemy

## Credits

Created with a help of open source community by [Roman Glushko](https://www.romaglushko.com/) 🦁

## References

- https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/
- https://www.cockroachlabs.com/docs/cockroachcloud/deploy-a-python-to-do-app-with-flask-kubernetes-and-cockroachcloud.html