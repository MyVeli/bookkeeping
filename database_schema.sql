CREATE TABLE Title(
    id SERIAL PRIMARY KEY,
    name TEXT,
    author TEXT,
    genre TEXT
);

CREATE TABLE BookStatus(
    id SERIAL PRIMARY KEY,
    status TEXT UNIQUE
);

CREATE TABLE Users(
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT 
);

CREATE TABLE Friends(
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(id),
    name TEXT
);

CREATE TABLE Book(
    id SERIAL PRIMARY KEY,
    title_id INT REFERENCES Title(id),
    status_id INT REFERENCES BookStatus(id),
    owner_id INT REFERENCES Users(id),
	holder_id INT REFERENCES Friends(id)
);