Cyber Security Base course project. 
In this project, task is to create a web application that has at least five different flaws from the OWASP top ten list.

LINK: link to the repository
installation instructions if needed

FLAW 1 - Injection:
safebanking/views.py
depositView method starting from the line xxx:
Raw sql query has been used in a incorrect way. This allows users to write sql queries to the amount input field. For example user can write "1000--" which removes the WHERE clause and adds 1000 to everyones balance instead of just user.
This can be fixed by replacing the line with cursor.execute("UPDATE safebanking_user_account SET balance = balance + %s WHERE id = %s", [amount, User_account_id]) which prevents possibility for sql instead. Even better way would be using the Django ORM tools and find user with user = User_account.objects.get(id = User_account_id) and then change the balance with user.balance += amount and finally save with user.save(). 

You can prevent any missuses by using simply if amount >= 0 etc... and handle the incorrect inputs with else: redirect... (in a similar way than it is handled at the transferView method above)

FLAW 2 - Cross-site Request Forgery:
safebanking/views.py and safebanking/templates/safebanking/transfer.html
transferView method starting from the line xxx:
This uses request.GET method without csrf protection. To test this vulnerability, there are file in a location Csrf_test/crsftest.html which transfers 10 balance out from the first user (id=1) and gives it to the second user (id=2).

This can be fixed by changing the form method into POST and making a csrf token verification {% csrf_token %} at the safebanking/templates/safebanking/transfer.html. 

FLAW 3 - Cross-site Scripting:
safebanking/views.py and safebanking/templates/safebanking/main.html
mainView method starting from the line xxx:
From the main page user can add a personal motto which is stored into database. Default motto is empty but user is allowed to add or edit the motto by using the form. The motto will be rendered and shown at the same main page. There are however two problems with the current approach: 
- Firstly there are no restrictions which prevents other users for reaching certain main page. Mainpage path is /main/{user_id}/ but the method does not check if the user is actually correct one. Any user who has logged in can reach anyones mainpage and edit their mottos.
- Secondly main.html page has flagged motto's to be safe on a line xxx. This makes it vulnerable for XXS. For example user (for example with id=1) can go the second user (id=2) mainpage using the path /main/2/ and type a for example new motto "<script>alert("You are hacked");</script>". When the second user (id=2) logs in, she/he will get a pop up window with the text "You are hacked" instead of mainpage.

To prevent this happening, safe flagging needs to be removed from the main.html at line xxx. Also it would be a good idea to add a check for the mainView method that the User_account_id (which is recieved from the path) matches with session.user_id (which is stored for user session during login). As matter of fact, in this kind of application, there probably wouldn't be a need for other users to vsit other pages, so the whole User_account_id could be removed from the path and user could be determined from the session.user_id instead.

FLAW 4 - Broken Access Control:
safebanking/views.py and safebanking/templates/safebanking/admin.html
adminView allows admin users to access admin panel where they can see database information from all users and make admin promotions / demotions. There are some flaws on this approuch:
- Firstly there are no actual checking if the user who tries to access admin panel has admin rights. Link to the admin panel is hidden for non-admin users at safebanking/templates/safebanking/base.html line xxx. However, anyone can reach the admin pages by using the addres /admin/user_id/ (any valid user id works there).
- Secondly anyone who can get into the admin panel and modify the admin rights for any user. This means that the user who does not have admin rights can promote herself/himself and even demote everyone else.

Easiest way to fix this flaw is to entirely remove this feature. Django has its own "Django Admin site" where admin users can explore and make modifications. Admin users can be created from the command line by typing $ python manage.py createsuperuser and following the instructions. Models can be make modifiable from safebanking/admin.py by adding for example in this case line admin.site.register(User_account). 

FLAW 5 - Broken Authentication:
There are no complexity requirements for the password.

How to fix - Create complexity

FLAW 6 - Sensity Data Exposure
Password and account number can be considered as a sensitive data and these are not encrypted at all. Ultimately both data can be seen from admin panel which is possible for anyone to access (See FLAW 4)

How to fix - Django has a built in User model which contains several fields including encrypted passwords and permissions. Instead of making a User_account model (like in this case), we could have used Djangos User model and additional Account model with a reference to the User model like this way:

class Account(models.Model):
    owner = models.ForeignKey(User)
    balance = models.IntegerField()
    motto = models.TextField()
    account_number = models.TextField()

