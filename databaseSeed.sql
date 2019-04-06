--Truncate grc.unit, grc.ingredient, grc.meal, grc.recipe;

INSERT INTO grc.unit(id, name)
	VALUES (1, 'Each'), (2, 'Tablespoon');

INSERT INTO grc.ingredient (id, name, unit_id)
	VALUES (1, 'Olive Oil', 2);
	
INSERT INTO grc.meal(id, name, rating)
	VALUES (1, 'West African Peanut Soup', 5);
	
INSERT INTO grc.recipe(meal_id, ingredient_id, quantity)
	VALUES (1, 1, 1);