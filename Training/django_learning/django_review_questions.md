# Django review questions

This is the final set of 15 questions for preparation and the review meeting, arranged from basic concepts to more challenging scenarios. The same wording and scope will be used during the meeting. Explain your reasoning and use short code examples or pseudocode where requested.

## Q1. Project setup and structure

What is the difference between a Django project and an app? Starting with Django installed, which commands would you use to create a project named `config` and an app named `library`, and what are the roles of `manage.py`, `settings.py`, and the project's `urls.py`?

## Q2. Models and field choices

What is a Django model, and how does it relate to a database table? Sketch a `Book` model with a title, optional summary, optional publication date, and price. Explain your field choices and the difference between `null=True` and `blank=True`.

## Q3. Database configuration and migrations

Where is a Django project's database connection configured? Explain the difference between `makemigrations` and `migrate`, and describe the steps needed after adding a new field to a model.

## Q4. Views, URLs, and templates

Describe how Django handles a request to `/books/42/`. Sketch the URL pattern and view that retrieve the book and render its title in a template. What response should be returned if the book does not exist?

## Q5. Form handling and validation

You need a form to create a book. When would you choose a `Form` rather than a `ModelForm`? Explain how the view should handle GET, invalid POST, and valid POST requests, how you would reject a negative price, and how you would change the title input's placeholder.

## Q6. Static files and uploaded media

A book page needs an application stylesheet and a cover image uploaded by a user. Explain how these two files are handled differently in Django. Describe how you would reference the stylesheet in a template and implement the cover-image upload from the HTML form through to storage and display.

## Q7. Reusable views and URL design

You are building a book list used alongside another app that also has a URL named `list`. Explain how you would implement the book list as a class-based view and connect it to a namespaced URL. When would you use `re_path()` instead of `path()`?

## Q8. Relationships and query parameters

Each book belongs to one category and can have several authors; an author can write several books. Describe the model relationships you would use. For `/books/?category=3&q=django`, show how you would retrieve the query parameters and build an ORM query, including your behavior for a missing or invalid category value.

## Q9. Django admin customization

How would you make `Book` manageable in Django admin and provide the appropriate staff access? Describe how you would display title and price, search by title, filter by a Boolean `is_available` field, and add an action that marks only selected books as unavailable.

## Q10. Model inheritance

Several models need the same `created_at` and `updated_at` fields. Explain the difference between abstract base model inheritance and multi-table inheritance, including the tables each creates. Which would you choose for sharing these timestamp fields, and why?

## Q11. Signals

A separate `Profile` record should be created when a new user is registered. Explain how you would implement this using a Django signal, ensure the handler is registered, and avoid creating another profile whenever the same user is saved again. What is one tradeoff of using a signal instead of calling the profile-creation logic explicitly?

## Q12. Schema-change debugging scenario

After a model change, one environment reports that a database column does not exist, while another works correctly. Explain how you would investigate and fix the difference. If the change also adds a required field to a table that already contains rows, how would you handle those existing records without losing data?

## Q13. Middleware scenario

A Django application needs a custom middleware that measures request duration and restricts a private area to authenticated users. Explain where the middleware runs, how request and response order work, and how you would implement and register it. Describe how you would avoid blocking public pages or creating a redirect loop.

## Q14. Signup and JWT scenario

A signup form accepts first name, last name, a unique email address, and a password. Describe the backend flow for validating the input, creating the user securely, and issuing JWTs after successful signup. Explain how you would enforce unique email addresses, distinguish access and refresh tokens, and validate a token on a later protected request.

## Q15. Protected profile scenario

A profile page must display only the authenticated user's first name, last name, and email. A developer retrieves the user using an ID supplied in the request, and users can change that ID to see someone else's profile. Explain how you would correct the view and pass data to the template. Also explain how an HTML profile request should behave when the user is unauthenticated, and why receiving JWTs at signup does not automatically authenticate a later ordinary Django template request.
