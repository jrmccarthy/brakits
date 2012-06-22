Needs



- Brackets Display Page

- Bracket Creation Page
    - Define number of teams
    - Define/upload a list of teams
    - Place teams in bracket, either manually or automagically
    - Some function to create properly sized bracket based on number of teams (powers of 2, etc)
    - Proper KnockoutJS to handle that and update brackets
    - Maybe some cool Socket stuff to display next-team-to-play

- Bracket Creator:
    - Define table size based on X teams
        -> 3 + X/4 High
        -> 4Y-1 Wide, where 2^Y = X
        -> Create grid with championship as match1, top 4 as match2-3, etc.
        -> Create table + classes for appropriate match size
        -> Generate CSS for that size and set proper bracket lines
        -> Generate data bindings for knockout-js (should probably pass a match dict instead of list)
