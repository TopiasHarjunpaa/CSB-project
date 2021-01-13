Cyber Security Base course project. 
<<<<<<< HEAD
In this project, task is to create a web application that has at least five different flaws from the OWASP top ten list.
=======
In this project, task is to create a web application that has at least five different flaws from the OWASP top ten list.

LINK: link to the repository
installation instructions if needed

FLAW 1 - Injection:
safebanking/views.py
depositView method starting from the line xxx:
Raw sql query has been used in a incorrect way. This allows users to write sql queries to the amount input field. For example user can write "1000--" which removes the WHERE clause and adds 1000 to everyones balance instead of just user.
This can be fixed by replacing the line with cursor.execute("UPDATE safebanking_user_account SET balance = balance + %s WHERE id = %s", [amount, User_account_id]) which prevents possibility for sql instead. Even better way would be using the Django ORM tools and find user with user = User_account.objects.get(id = User_account_id) and then change the balance with user.balance += amount and finally save with user.save(). You can prevent any missuses by using simply if amount >= 0 etc... and handle the incorrect inputs with else: redirect... (in a similar way than it is handled at the transferView method above)

FLAW 2 - Cross-site Request Forgery:
safebanking/views.py
transferView method starting from the line xxx:
This uses request.GET method without csrf protection. To test this vulnerability, there are file in a location Csrf_test/crsftest.html which transfers 10 balance out from the first user (id=1) and gives it to the second user (id=2).
This can be fixed by changing the form method into POST and making a csrf token verification {% csrf_token %} at the safebanking/templates/safebanking/transfer.html. 

FLAW 3 - Cross-site Scripting:
exact source link pinpointing flaw 2...
description of flaw 2...
how to fix it...

FLAW 4 - Broken Access Control:
exact source link pinpointing flaw 2...
description of flaw 2...
how to fix it...

FLAW 5 - Broken Authentication:
exact source link pinpointing flaw 2...
description of flaw 2...
how to fix it...
>>>>>>> 030c04f83cec5f393c1ac46e03719470674047c9
