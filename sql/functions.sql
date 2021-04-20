--selects a subset of interactions between the given timestamps that belongs to the given dataset
CREATE OR REPLACE FUNCTION subset_for_scenario (TIMESTAMP, TIMESTAMP, INT)
RETURNS TABLE (client_id INT,item_id INT,tmstamp TIMESTAMP)
AS
$body$
	
	SELECT I1.client_id, I1.item_id, I1.tmstamp FROM interaction I1
	WHERE I1.dataset_id = $3
	AND I1.tmstamp BETWEEN $1 AND $2

$body$
LANGUAGE sql;

CREATE OR REPLACE FUNCTION subset_for_scenario ( INT)
RETURNS TABLE (client_id INT,item_id INT,tmstamp TIMESTAMP)
AS
$body$
	
	SELECT I1.client_id, I1.item_id, I1.tmstamp FROM interaction I1
	WHERE I1.dataset_id = $1

$body$
LANGUAGE sql;

--selects clients 
CREATE OR REPLACE FUNCTION subset_for_scenario_client (TIMESTAMP, TIMESTAMP, INT, INT, FLOAT DEFAULT 'infinity')
RETURNS TABLE (client_id INT)
AS
$body$

	SELECT I1.client_id FROM subset_for_scenario($1,$2,$3) I1
    GROUP BY I1.client_id
    HAVING  COUNT(I1.client_id) BETWEEN $4 AND $5

$body$
LANGUAGE sql;

CREATE OR REPLACE FUNCTION subset_for_scenario_client (INT, INT, FLOAT DEFAULT 'infinity')
RETURNS TABLE (client_id INT)
AS
$body$

	SELECT I1.client_id FROM subset_for_scenario($1) I1
    GROUP BY I1.client_id
    HAVING  COUNT(I1.client_id) BETWEEN $2 AND $3

$body$
LANGUAGE sql;

--selects clients 
CREATE OR REPLACE FUNCTION subset_for_scenario_item (TIMESTAMP, TIMESTAMP, INT, INT, FLOAT DEFAULT 'infinity')
RETURNS TABLE (item_id INT)
AS
$body$

	SELECT I1.item_id FROM subset_for_scenario($1,$2,$3) I1
    GROUP BY I1.item_id
    HAVING  COUNT(I1.item_id) BETWEEN $4 AND $5

$body$
LANGUAGE sql;

CREATE OR REPLACE FUNCTION subset_for_scenario_item (INT, INT, FLOAT DEFAULT 'infinity')
RETURNS TABLE (item_id INT)
AS
$body$

	SELECT I1.item_id FROM subset_for_scenario($1) I1
    GROUP BY I1.item_id
    HAVING  COUNT(I1.item_id) BETWEEN $2 AND $3

$body$
LANGUAGE sql;

--delete scenario_elements when scenario is deleted
CREATE OR REPLACE FUNCTION delete_scenario_elements ()
RETURNS TRIGGER
AS 
$body$
BEGIN
	DELETE FROM scenario_element 
	WHERE scenario_id = old.id; 
	RETURN OLD;
END;
$body$
LANGUAGE plpgsql;


CREATE TRIGGER delete_scenario_trigger 
BEFORE DELETE
ON scenario
FOR EACH ROW
EXECUTE FUNCTION  delete_scenario_elements ();

--delete interactions when dataset is deleted
CREATE OR REPLACE FUNCTION delete_interactions()
RETURNS TRIGGER
AS 
$body$
BEGIN
	DELETE FROM interaction 
	WHERE dataset_id = old.id; 
	RETURN OLD;
END;
$body$
LANGUAGE plpgsql;


CREATE TRIGGER delete_dataset_trigger 
BEFORE DELETE
ON dataset
FOR EACH ROW
EXECUTE FUNCTION  delete_interactions();