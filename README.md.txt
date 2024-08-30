I do have a new requirement: Fill NaN 'Email' and 'Name' values with non-NaN values only if the 'can_id' group has:
 - Only one unique non-NaN 'Email' value and
 - Only one unique non-NaN 'Name' value.

To be clear, the unique non-NaN 'Email' value may already be the value in more than one row in the 'can_id' group, and the unique non-NaN 'Name' value may already be the value in more than one row. The requirement is that they are unique.

