This module helper functions to find public holidays did allow to use an
hr.employee to filter country and states based on the employee address.

Since only the address of the employee was used, modifying the functions
to use a res.partner instead of an hr.employee allows more possibilities
such as checking public holidays for customers and suppliers.
