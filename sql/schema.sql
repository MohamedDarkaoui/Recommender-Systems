CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  username VARCHAR(20)  UNIQUE NOT NULL , 
  email VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(250) NOT NULL
);

CREATE TABLE dataset (
  id INT UNIQUE,
  name VARCHAR(50) NOT NULL,
  usr_id INT NOT NULL,
  private BOOL NOT NULL,
  FOREIGN KEY (usr_id) REFERENCES users (id),
  PRIMARY KEY (usr_id,name)
);

CREATE TABLE item (
  id INT,
  dataset_id INT,
  FOREIGN KEY (dataset_id) REFERENCES dataset (id),
  PRIMARY KEY (id, dataset_id)
);

CREATE TABLE client (
  id INT,
  dataset_id INT,
  FOREIGN KEY (dataset_id) REFERENCES dataset (id),
  PRIMARY KEY (id, dataset_id)
);

CREATE TABLE interaction (
  dataset_id INT NOT NULL,
  client_id INT NOT NULL,
  item_id INT NOT NULL,
  timestamp DATE NOT NULL,
  FOREIGN KEY (client_id, dataset_id) REFERENCES client(id,dataset_id),	
  FOREIGN KEY (item_id, dataset_id) REFERENCES item(id,dataset_id),	
  PRIMARY KEY (dataset_id,client_id,item_id, timestamp)
);

CREATE TABLE metadata (
  id INT PRIMARY KEY,
  dataset_id INT NOT NULL REFERENCES dataset(id)
);


CREATE TABLE metadata_element (
  item_id INT NOT NULL,
  dataset_id INT NOT NULL,
  metadata_id INT NOT NULL REFERENCES metadata (id),
  description TEXT NOT NULL,
  data TEXT NOT NULL,
  FOREIGN KEY (item_id, dataset_id) REFERENCES item(id, dataset_id),
  PRIMARY KEY (item_id, metadata_id, description)
);