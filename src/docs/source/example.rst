.. _example:

Examples
========

This page shows real fixture-based examples from ``test/data`` and the corresponding
flattened pandas DataFrame output produced by ``DeepNestedHandler``.

Conversion Pattern
------------------

All examples follow the same two-step workflow:

.. code-block:: python

	 from json2df.json2df import LoadInfo, DeepNestedHandler

	 payload = LoadInfo(file="test/data/<fixture>.json").get_data()
	 df = DeepNestedHandler(json_data=payload).convert_to_df()

Example 1: Household Data
-------------------------

Input JSON (``test/data/user_household_data.json``):

.. code-block:: json

	 {
		 "name": "John",
		 "age": 30,
		 "married": true,
		 "divorced": false,
		 "children": ["Ann", "Billy"],
		 "pets": null,
		 "cars": [
			 {"model": "BMW 230", "mpg": 27.5},
			 {"model": "Ford Edge", "mpg": 24.1}
		 ]
	 }

Output DataFrame preview (shape: ``(4, 8)``):

.. parsed-literal::

	 **name**  **age**  **married**  **divorced** **children** **pets** **cars_model**  **cars_mpg**
	 John   30     True     False      Ann None    BMW 230      27.5
	 John   30     True     False      Ann None  Ford Edge      24.1
	 John   30     True     False    Billy None    BMW 230      27.5
	 John   30     True     False    Billy None  Ford Edge      24.1

Flattened columns:

- ``name``
- ``age``
- ``married``
- ``divorced``
- ``children``
- ``pets``
- ``cars_model``
- ``cars_mpg``

Example 2: Superhero Roster
---------------------------

Input JSON excerpt (``test/data/superhero_team_roster.json``):

.. code-block:: json

	 {
		 "squadName": "Super hero squad",
		 "homeTown": "Metro City",
		 "formed": 2016,
		 "secretBase": "Super tower",
		 "active": true,
		 "members": [
			 {
				 "name": "Molecule Man",
				 "age": 29,
				 "secretIdentity": "Dan Jukes",
				 "powers": ["Radiation resistance", "Turning tiny", "Radiation blast"]
			 }
		 ]
	 }

Output DataFrame preview (shape: ``(11, 9)``):

.. parsed-literal::

	        **squadName**   **homeTown**  **formed**  **secretBase**  **active**    **members_name**  **members_age** **members_secretIdentity**       **members_powers**
	 Super hero squad Metro City    2016 Super tower    True    Molecule Man           29              Dan Jukes Radiation resistance
	 Super hero squad Metro City    2016 Super tower    True    Molecule Man           29              Dan Jukes         Turning tiny
	 Super hero squad Metro City    2016 Super tower    True    Molecule Man           29              Dan Jukes      Radiation blast
	 Super hero squad Metro City    2016 Super tower    True Madame Uppercut           39            Jane Wilson  Million tonne punch
	 Super hero squad Metro City    2016 Super tower    True Madame Uppercut           39            Jane Wilson    Damage resistance

Key behavior shown:

- Nested dictionaries are flattened with underscore-separated names.
- List-valued fields (for example ``members`` and ``members_powers``) expand rows.

Example 3: Deep Nested Quiz Data
--------------------------------

Input JSON excerpt (``test/data/quiz.json``):

.. code-block:: json

	 {
		 "quiz": {
			 "sport": {
				 "q1": {
					 "question": "Which one is correct team name in NBA?",
					 "options": [
						 "New York Bulls",
						 "Los Angeles Kings",
						 "Golden State Warriors",
						 "Houston Rockets"
					 ],
					 "answer": "Huston Rocket"
				 }
			 },
			 "maths": {
				 "q1": {
					 "question": "5 + 7 = ?",
					 "options": ["10", "11", "12", "13"],
					 "answer": "12"
				 }
			 }
		 }
	 }

Output DataFrame preview (shape: ``(64, 9)``):

.. parsed-literal::

	                 **quiz_sport_q1_question** **quiz_sport_q1_options** **quiz_sport_q1_answer** **quiz_maths_q1_question** **quiz_maths_q1_options** **quiz_maths_q1_answer** **quiz_maths_q2_question** **quiz_maths_q2_options** **quiz_maths_q2_answer**
	 Which one is correct team name in NBA?        New York Bulls        Huston Rocket             5 + 7 = ?                    10                   12              12 - 8 = ?                     1                    4
	 Which one is correct team name in NBA?        New York Bulls        Huston Rocket             5 + 7 = ?                    10                   12              12 - 8 = ?                     2                    4
	 Which one is correct team name in NBA?        New York Bulls        Huston Rocket             5 + 7 = ?                    10                   12              12 - 8 = ?                     3                    4
	 Which one is correct team name in NBA?        New York Bulls        Huston Rocket             5 + 7 = ?                    10                   12              12 - 8 = ?                     4                    4

Key behavior shown:

- Deeply nested keys become long, explicit column names.
- Multiple list fields can create combinational row expansion.

Example 4: Donut Metadata
-------------------------

Input JSON excerpt (``test/data/sample_donut_data.json``):

.. code-block:: json

	 {
		 "id": "0001",
		 "type": "donut",
		 "name": "Cake",
		 "ppu": 0.55,
		 "hello": [1, 2, 3],
		 "batters": {
			 "batter_1": [
				 {"id": "1001", "type": "Regular"},
				 {"id": "1002", "type": "Chocolate"}
			 ]
		 },
		 "topping": [
			 {"id": "5001", "type": "None"},
			 {"id": "5002", "type": "Glazed"}
		 ]
	 }

Output DataFrame preview (shape: ``(336, 11)``):

.. parsed-literal::

	   **id**  **type** **name**  **ppu**  **hello** **batters_batter_1_id** **batters_batter_1_type** **batters_batter_2_id** **batters_batter_2_type** **topping_id**             **topping_type**
	 0001 donut Cake 0.55      1                1001               Regular                1001               Regular       5001                     None
	 0001 donut Cake 0.55      1                1001               Regular                1001               Regular       5002                   Glazed
	 0001 donut Cake 0.55      1                1001               Regular                1001               Regular       5005                    Sugar
	 0001 donut Cake 0.55      1                1001               Regular                1001               Regular       5007           Powdered Sugar

Key behavior shown:

- Sibling nested lists (``hello``, ``batter_*``, ``topping``) can produce a large
	number of rows.
- Scalar metadata columns (``id``, ``type``, ``name``, ``ppu``) are repeated across
	expanded rows.

Tips for Reading Output
-----------------------

- Use ``df.shape`` first to understand expansion impact.
- Use ``df.columns.tolist()`` to inspect flattened names quickly.
- Use ``df.head()`` and ``df.sample()`` to validate row-level behavior on large outputs.

