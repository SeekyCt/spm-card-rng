# SPM Card Shop RNG Simulator

An old Python re-implementation of the logic that determines the card given by a card bag and the caught cards for sale in Super Paper Mario.

## Setup
A ram dump of the game named `ram.raw` should be placed in the folder. This can be taken any time after the last sequence change & card transaction.

## cardbag.py

Says what the next card bag from a ram dump would sell.

## caughtcards.py

Says what the caught cards shop would sell when refreshed (happens when talking to the shopkeeper and GSWF(19) is set).

## allchances.py

Dumps all possible card chances assuming every card is owned on all sequence values to the `out` folder. 0% chance cards are skipped.
