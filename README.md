Building And Deploying A Complete Web Backend With FastAPI
==========================================================

Based on part two, Building And Deploying A Complete Web Backend With FastAPI, of the book [Building Data Science Applications with FastAPI - Second Edition](https://www.amazon.com/Building-Data-Science-Applications-FastAPI-ebook/dp/B0C9D1QYVX?qid=1692021319&refinements=p_27:Fran%C3%A7ois+Voron&s=digital-text&sr=1-1&text=Fran%C3%A7ois+Voron&linkCode=sl1&tag=mobilea00b2a6-20&linkId=751999f2c2a85565dbd749e640befa60&language=en_US&ref_=as_li_ss_tl) by François Voron

Run app with `uvicorn my_sqlalchemy.app:app --reload`

View documentation at `http://localhost:8000/docs`

# Chapter 6: Databases and Asynchronous ORMs

Use Pydantic models (schemas for short) to validate and serialize the data, but the database communication will be done with the ORM model (model for short).

## Creating ORM Models

Each ORM model is a Python class whose attributes represent the columns of your table. The actual entities of the database are instances of this class, providing access to its data. SQLAlchemy ORM links this Python object and the row in the database. The blog post model is defined via `models.py`.

## Defining Pydantic Schemas

## Connecting to SQLite Database

## Creating Objects
