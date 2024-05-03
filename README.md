# Summary

This is a sample Django application that has some failing tests.  It's built off the example project in
[Writing your first Django app](https://docs.djangoproject.com/en/dev/intro/tutorial01/).

As a programming exercise do the following:
* Create a fork of this repo.
* Make a pull request that fixes the broken tests.

## Instructions for Running

* to run tests:

    docker-compose run --service-ports app-test

* to run (user is `admin` and password is `asdfASDF1234`):

    docker-compose run --service-ports app

## Improvements I added

* Added Dockerfile and docker-compose to have it in container.
* Updated requirements.txt.
* Added some linters and checkers, included: black, isort, flake8, pre-commit.
* Fixed tests.
* Added QuestionListSerializer, to handle update of many objects (only patch for now).
* Added CustomRouter to handle additional_routes (for example patch).
* Added migration in poll adding date_created.
* Added github CI to run tests.
