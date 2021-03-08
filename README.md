# Cyber Security Base course project. 
In this project, task is to create a web application that has at least five different flaws from the OWASP top ten list.

[Link to the repository](https://github.com/TopiasHarjunpaa/CSB-project)

## Installation instructions

Requires Python 3 (3.5 or higher)

Instructions for [installing Python and additional packages](https://cybersecuritybase.mooc.fi/installation-guide)

Clone repository:

```
$ git clone git@github.com:TopiasHarjunpaa/CSB-project.git
$ cd CSB-project
```

Run application:

```
$ python3 manage.py runserver
```

## FLAW 1 - Injection:
Location of the flaw [(views.py)](https://github.com/TopiasHarjunpaa/CSB-project/blob/d7e07727fffcd323dab6d205e9d0b54e1e4e78d7/safebanking/views.py#L137)

#### Description
Raw sql query has been used in this method. Right now the query is following:

```
cursor.execute(f"UPDATE safebanking_user_account SET balance = balance + {amount} WHERE id = {User_account_id}")
```

This gives the non-friendly user possibility to make sql injection. Instead of typing amount to the input field in a application, user can type for example "1000--" which removes the whole WHERE clause and adds 1000 to everyones balance instead of just for current user.

#### How to fix
To prevent sql injection in a raw sql query, we could replace the query with following:

```
cursor.execute("UPDATE safebanking_user_account SET balance = balance + %s WHERE id = %s", [amount, User_account_id])
```

Perhaps even better way would be using the Django ORM tools:

```
user = User_account.objects.get(id = User_account_id)
amount = request.POST.get("amount")
user.balance += amount
user.save()
```
And of course it could be a good idea to prevent users for adding a negative amounts etc.


## FLAW 2 - Cross-site Request Forgery:
Location of the flaws [(views.py)](https://github.com/TopiasHarjunpaa/CSB-project/blob/8d752cc92868132556eb27af96775cd3543cfd91/safebanking/views.py#L115) and [(transfer.html)](https://github.com/TopiasHarjunpaa/CSB-project/blob/8d752cc92868132556eb27af96775cd3543cfd91/safebanking/templates/safebanking/transfer.html#L17)

#### Description
This uses request.GET method without csrf protection. To test this vulnerability, there are file [crsftest.html](https://github.com/TopiasHarjunpaa/CSB-project/blob/8d752cc92868132556eb27af96775cd3543cfd91/Csrf_test/crsftest.html#L4) which transfers 10 balance out from the first user (id=1) and gives it to the second user (id=2). Just make sure that there are at least 2 users created at the application

#### How to fix
This can be fixed by changing the form method into POST (both views.py and transfer.html) and making a csrf token verification (transfer.html)

Current solution:

```
<form action="/transfer/{{owner.id}}/" method="GET">
    <h6>Transfer money to:</h6>
    ...
```
Fixed solution:

```
<form action="/transfer/{{owner.id}}/" method="POST">
    {% csrf_token %}
    <h6>Transfer money to:</h6>
    ...
```

## FLAW 3 - Cross-site Scripting:
Location of the flaws [(views.py)](https://github.com/TopiasHarjunpaa/CSB-project/blob/a6206e61d4ec13411bc75c9bf6456906754bc9f1/safebanking/views.py#L104) and [(main.html)](https://github.com/TopiasHarjunpaa/CSB-project/blob/a6206e61d4ec13411bc75c9bf6456906754bc9f1/safebanking/templates/safebanking/main.html#L22)

safebanking/views.py and safebanking/templates/safebanking/main.html
mainView method starting from the line xxx:

#### description
From the main page user can add a personal motto which is stored into database. Default motto is empty, but user is allowed to add or edit the motto by using the form. The motto will be rendered and shown at the same main page. There are however two problems with the current approach: 
- Firstly there are no restrictions which prevents other users for reaching certain main page. Mainpage path is `/main/{user_id}/` but the method does not check if the user is actually the owner of that id. Any user who has logged in can reach anyones mainpage and edit their mottos.
- Secondly [(main.html)](https://github.com/TopiasHarjunpaa/CSB-project/blob/a6206e61d4ec13411bc75c9bf6456906754bc9f1/safebanking/templates/safebanking/main.html#L22) page has flagged motto's to be safe. This makes it vulnerable for XXS. For example user `with id = 1` can go to the second users `with id = 2` mainpage using the path `/main/2/` and create a new motto, such as:

 `<script>alert("You are hacked");</script>`
  
When the second user `with id = 2` logs in, she/he will get a pop up window with the text `You are hacked` instead of mainpage.

#### how to fix
To prevent this happening, simple replace `{{owner.motto|safe}}` with `{{owner.motto}}` from [(main.html)](https://github.com/TopiasHarjunpaa/CSB-project/blob/a6206e61d4ec13411bc75c9bf6456906754bc9f1/safebanking/templates/safebanking/main.html#L22)

Also it would be a good idea to add a check for the [(mainView method)](https://github.com/TopiasHarjunpaa/CSB-project/blob/a6206e61d4ec13411bc75c9bf6456906754bc9f1/safebanking/templates/safebanking/main.html#L22) that the `User_account_id` (which is recieved from the path) matches with `session.user_id` (which is stored for user session during login). As matter of fact, in this kind of application, there probably wouldn't be a need for other users to visit other pages, so the whole `User_account_id` could be removed from the path and user could be determined from the `session.user_id` instead.

## FLAW 4 - Broken Access Control:
safebanking/views.py and safebanking/templates/safebanking/admin.html

#### description
adminView allows admin users to access admin panel where they can see database information from all users and make admin promotions / demotions. There are some flaws on this approuch:
- Firstly there are no actual checking if the user who tries to access admin panel has admin rights. Link to the admin panel is hidden for non-admin users at safebanking/templates/safebanking/base.html line xxx. However, anyone can reach the admin pages by using the addres /admin/user_id/ (any valid user id works there).
- Secondly anyone who can get into the admin panel and modify the admin rights for any user. This means that the user who does not have admin rights can promote herself/himself and even demote everyone else.

#### how to fix
Easiest way to fix this flaw is to entirely remove this feature. Django has its own "Django Admin site" where admin users can explore and make modifications. Admin users can be created from the command line by typing $ python manage.py createsuperuser and following the instructions. Models can be make modifiable from safebanking/admin.py by adding for example in this case line admin.site.register(User_account). 

## FLAW 5 - Broken Authentication:

#### description
There are no complexity requirements for the password. Basically user can choose whatever password they prefers, such as "password" or "1234" Secondly, the passwords are stored into database as a plain textfield without any encryption at all.

#### how to fix
Restrict users to choose whatever password they prefer. One solution could be create a function which checks the password input and makes sure it does has certain complexity (such as minimun length, lower- and uppercase letters and some special characters). Also there could be a another function which tests the password input by going through list of top 10000 words passwords and prevents users from choosing those. Solution for encryption problem is explained at the FLAW 6.

## FLAW 6 - Sensity Data Exposure

#### description
Password and (and perhaps sometimes account number) can be considered as a sensitive data and these are not encrypted at all. Ultimately both data can be seen from admin panel which is possible for anyone to access (See FLAW 4)

#### how to fix
Django has a built in User model which contains several fields including encrypted passwords and permissions. Instead of making a User_account model (like in this case) we could have used Djangos User model and additional Account model with a reference to the User model like this way:

class Account(models.Model):
    owner = models.ForeignKey(User)
    balance = models.IntegerField()
    motto = models.TextField()
    account_number = models.TextField()

