CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  username VARCHAR(20)  UNIQUE NOT NULL , 
  email VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(250) NOT NULL
);


CREATE TABLE item (
  id INT PRIMARY KEY
);


CREATE TABLE client (
  id INT PRIMARY KEY
);


CREATE TABLE dataset (
  id INT UNIQUE,
  name VARCHAR(50) NOT NULL,
  usr_id INT NOT NULL,
  private BOOL NOT NULL,
  FOREIGN KEY (usr_id) REFERENCES users (id),
  PRIMARY KEY (id,name)
);


CREATE TABLE dataset_element (
  id INT PRIMARY KEY,
  dataset_id INT NOT NULL REFERENCES dataset(id),
  client_id INT NOT NULL REFERENCES client(id),
  item_id INT NOT NULL  REFERENCES item(id),
  timestamp DATE NOT NULL
);


CREATE TABLE metadata (
  id INT PRIMARY KEY,
  dataset_id INT NOT NULL REFERENCES dataset(id)
);


CREATE TABLE metadata_element (
  id INT PRIMARY KEY,
  item_id INT NOT NULL REFERENCES item (id),
  metadata_id INT NOT NULL REFERENCES metadata (id),
  data TEXT NOT NULL,
  description TEXT NOT NULL
);
