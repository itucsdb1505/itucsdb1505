Parts Implemented by Caghan Caglar
==================================
Database Design
---------------
Pool Table consists of 5 attributes.

.. figure:: pooltable.png

   Pool Table

- **ID**        : New ID values for each Pool tuple

- **NAME**       : Name of the Pool (Stadium)

- **COUNTRY_ID** : Foreign key that references the COUNTRY_ID attribute of the Country Table with "ON DELETE CASCADE ON UPDATE CASCADE" option for Data Integrity

- **CAPACITY**   : Number of seats that Pool (Stadium) has

- **BUILT**      : Built year of the Pool (Stadium)

----------------------------------------------------------------------------

Stats Table consists of 6 attributes.

.. figure:: statstable.png

   Stats Table

- **ID**        : New ID values for each Statistic tuple

- **PLAYER_ID** : Foreign key that references the PLAYER_ID attribute of the Player Table with "ON DELETE CASCADE ON UPDATE CASCADE" option for Data Integrity

- **LEAGUE_ID** : Foreign key that references the LEAGUE_ID attribute of the League Table with "ON DELETE CASCADE ON UPDATE CASCADE" option for Data Integrity

- **GOAL**      : Number of goals that Player scored

- **ASSIST**    : Number of assists that Player made

- **SAVE**      : Number of saves that Player made

.. toctree::
   Pool_d
   Statistic_d