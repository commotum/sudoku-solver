Status of Strategy Implementation
The solver currently supports only singles, subsets, and basic intersection techniques, as listed in the “Implemented Strategies” section of the README. Files for fish, wing, and chain techniques exist but contain only placeholder comments, meaning these methods are not yet implemented:

fish.py – intended for X-Wing and Swordfish

wings.py – intended for XY-Wing and XYZ-Wing

chains.py – intended for Coloring, Forcing Chain, and Nishio

Plan to Complete Remaining Strategies
Enable elimination handling

Extend utils.apply_deductions (and/or a candidate-management helper) so elimination-type deductions can update candidates immediately, allowing advanced strategies to propagate their effects.

Implement missing strategy families

Fish strategies (fish.py): X-Wing and Swordfish with a generic pattern-scanning helper.

Wing strategies (wings.py): XY-Wing and XYZ-Wing using bivalue/trivalue pivots to remove candidates.

Chain strategies (chains.py): Coloring, Forcing Chain, and Nishio to capture implication-based eliminations or forced fills.

Integrate and register

Add each new strategy function to STRATEGY_FUNCTIONS in strategies/strategies.py and expand the default strategy list in solver.py as they become stable.

Testing & validation

Create small puzzle sets or unit tests that exercise each strategy.

Confirm eliminations/fills are correct and improve overall solver progress without conflicts.

Following this roadmap will complete the solver’s planned strategy suite and enable more human-style deduction sequences across harder puzzles.