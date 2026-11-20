# Django review answer key — reviewer only

Keep this document private. Share only `django_review_questions.md` with the junior. This key corresponds exactly to Q1–Q15 in that file; use those fixed prompts during the meeting. There are no additional scored follow-up questions or surprise practical tasks.

## Source material and scope

Reviewed the 15 screenshots currently present in `topics_ss/`, covering Days 15–29, and the earlier `DJANGO_REVIEW.md`. The screenshots are the primary evidence of training coverage; the earlier review is a derived assessment. The files in `../python_learning/` contain Python exercises rather than additional Django lessons.

Days 15–25 and 27 are marked **Complete**. Days 26 (login/logout), 28 (profile update/account deletion), and 29 (testing/final touches) are marked **Overdue**, so their specific learning objectives are excluded from the scored set. Optional verification-email delivery is also excluded. Completion labels establish the review scope; they do not establish the junior's competence.

| Completed source | Covered objectives | Questions |
|---|---|---|
| [Day 15](topics_ss/topic_15.png) | Project/app creation, structure, settings, URL configuration | Q1, Q3, Q4 |
| [Day 16](topics_ss/topic_16.png) | Models, fields, ORM, database settings, migrations | Q2, Q3, Q8, Q12 |
| [Day 17](topics_ss/topic_17.png) | Request handling, basic views/URLs, templates, dynamic content | Q4, Q15 |
| [Day 18](topics_ss/topic_18.png) | Query parameters, dynamic data, class-based views, regex URLs, namespaces | Q7, Q8 |
| [Day 19](topics_ss/topic_19.png) | Forms, submission, validation, behavior and appearance | Q5, Q14 |
| [Day 20](topics_ss/topic_20.png) | Admin access, model registration, customization, actions and filters | Q9 |
| [Day 21](topics_ss/topic_21.png) | Schema-change scenarios, foreign keys, many-to-many relationships | Q8, Q12 |
| [Day 22](topics_ss/topic_22.png) | Static files, template references, file/image uploads | Q6 |
| [Day 23](topics_ss/topic_23.png) | Abstract and multi-table inheritance, signals and handlers | Q10, Q11 |
| [Day 24](topics_ss/topic_24.png) | Custom middleware, request processing, authentication checks | Q13 |
| [Day 25](topics_ss/topic_25.png) | Signup, validation, user creation, Simple JWT setup and token issuance | Q14 |
| [Day 27](topics_ss/topic_27.png) | Profile template, authenticated retrieval, passing user data to frontend | Q15 |

## Marking scheme

**15 questions × 5 marks = 75 marks.** Suggested meeting duration: 75–90 minutes. Each question has five one-mark criteria below. Award 1 for a correct explanation/application, 0.5 for partial understanding, or 0 for an absent or materially incorrect answer. Record substantial assistance and reduce the affected criterion to partial credit. Accept equivalent supported APIs and sound pseudocode; do not require exact memorized syntax for full conceptual credit. Do not require topics or details beyond the fixed prompt.

The expected answers describe sufficient content, not scripts to memorize. Judge whether the junior can connect each explanation to the requested implementation. Documentation references use Django 5.2 as an explicit baseline; adapt accepted syntax to the actual training version. Simple JWT setup depends on the installed package versions.

## Q1. Project setup and structure — 5 marks

**Expected answer:** A project assembles configuration and apps; an app implements a coherent feature area and can be reused. From an appropriate working directory, run `django-admin startproject config .` and `python manage.py startapp library`. `manage.py` executes project management commands, `settings.py` holds configuration, and root `urls.py` routes requests or includes app URLconfs. Register the app in `INSTALLED_APPS` when integrating its models and other app features. An app's `urls.py` is normally created manually.

**Evaluation criteria — 1 mark each:**

- Distinguishes project configuration from app functionality.
- Gives correct project creation command, with or without the optional directory argument.
- Gives correct app creation command.
- Explains `manage.py` and `settings.py` accurately.
- Explains the root URLconf and app integration accurately.

## Q2. Models and field choices — 5 marks

**Expected answer:** A concrete model normally represents a database table, its fields represent columns, and instances represent rows. For example:

```python
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    published_on = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

Use decimal values for prices rather than binary floating-point. `null` controls database NULL storage; `blank` controls validation of empty values. Optional text usually uses an empty string, while an absent date commonly uses NULL. A nonnegative-price validator may be added here, but its implementation is assessed in Q5.

**Evaluation criteria — 1 mark each:**

- Explains model/table/instance relationships.
- Uses suitable title and summary field types.
- Represents the optional publication date correctly.
- Chooses a decimal price field and explains precision.
- Correctly distinguishes `null` and `blank`.

## Q3. Database configuration and migrations — 5 marks

**Expected answer:** Database engine and connection details live in `DATABASES` in the active settings. `makemigrations` creates migration files from model-state changes relative to migration history; it does not apply schema changes. `migrate` applies migrations to the selected database. After changing a model, generate and inspect the migration, apply it, and verify the resulting schema/application behavior. Commit the migration with the model change and use consistent migration files across environments.

**Evaluation criteria — 1 mark each:**

- Identifies `DATABASES` and the active settings.
- Explains migration generation correctly.
- Explains migration application correctly.
- Gives a sensible change/review/apply/verify sequence.
- Recognizes migration files as versioned project artifacts.

## Q4. Views, URLs, and templates — 5 marks

**Expected answer:** Django resolves the URL to a view. The view retrieves the requested object, builds context, renders a template, and returns a response. For an app included at `/books/`:

```python
# library/urls.py
path("<int:pk>/", views.book_detail, name="detail")

# library/views.py
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "library/detail.html", {"book": book})
```

Assume the normal imports for `path`, `views`, `Book`, `render`, and `get_object_or_404`. The template can render `{{ book.title }}`. An unknown object should produce HTTP 404. The integer converter does not prove the object exists.

**Evaluation criteria — 1 mark each:**

- Explains the request-to-response sequence.
- Shows a matching route and view argument.
- Retrieves the specific book through the ORM.
- Passes context and renders the title correctly.
- Returns 404 for an unknown book.

## Q5. Form handling and validation — 5 marks

**Expected answer:** A `Form` suits input not directly mapped to one model or a custom workflow; a `ModelForm` derives model fields and provides persistence helpers, so it is suitable here. Explicitly select editable fields. GET displays an unbound form; POST binds submitted data and calls `is_valid()`. Invalid POST rerenders the bound form with errors and input; valid POST saves and redirects. A `clean_price()` method or field/model `MinValueValidator` can reject negative prices. Use a widget's `attrs`, such as `{"placeholder": "Book title"}`, for appearance. The POST template includes a CSRF token with CSRF protection configured. Browser-only validation is insufficient.

**Evaluation criteria — 1 mark each:**

- Justifies `Form` versus `ModelForm`.
- Distinguishes GET from bound POST processing.
- Preserves invalid form errors/input and saves only valid data, with a successful redirect.
- Implements server-side nonnegative-price validation.
- Explains widget placeholder customization.

## Q6. Static files and uploaded media — 5 marks

**Expected answer:** CSS is application static content; uploaded covers are media managed through configured storage. A static template reference can use `{% load static %}` and `{% static 'library/styles.css' %}`. Static discovery uses app static directories or configured additional directories; `STATIC_URL` is the URL prefix and `STATIC_ROOT` can collect deployment assets. A cover uses an `ImageField(upload_to="covers/")` with an appropriate form field. `ImageField` requires Pillow. The form uses POST and `enctype="multipart/form-data"`; bind both `request.POST` and `request.FILES`. Validate the file and size policy, then save through the form/storage. Under local filesystem storage, configure `MEDIA_ROOT`/`MEDIA_URL` and display a present cover using `book.cover.url`. Remote storage may provide its own URLs. Development serving helpers are not production file serving.

**Evaluation criteria — 1 mark each:**

- Distinguishes static assets from uploaded media and their configuration.
- Uses Django's static template tag correctly.
- Chooses a suitable image field and upload form encoding.
- Binds files, validates them, and persists through storage.
- Explains media URL display and storage/serving configuration.

## Q7. Reusable views and URL design — 5 marks

**Expected answer:** Define a `BookListView(ListView)` with `model = Book`, a template name, and a context name if desired. Connect it using `BookListView.as_view()`. In the app URLconf, set `app_name = "library"` and name the route `list`; include this URLconf from the project and reverse `library:list`. Namespacing distinguishes another app's `list`. `path()` converters cover common dynamic segments; `re_path()` permits regex restrictions, such as a four-digit archive year. Generic views reuse common behavior rather than requiring every list operation to be written from scratch.

**Evaluation criteria — 1 mark each:**

- Describes a suitable class-based list implementation.
- Explains its reusable behavior and connects it with `as_view()`.
- Shows an app namespace and named route.
- Explains inclusion and namespaced reversal.
- Gives a valid reason/example for regex routing.

## Q8. Relationships and query parameters — 5 marks

**Expected answer:** Use a foreign key from `Book` to `Category`, with a deliberate `on_delete` policy, and a many-to-many field between books and authors. Read query data from `request.GET`; it is separate from path parameters. Start with `Book.objects.all()`, apply `filter(category_id=category_id)` after validating/converting the supplied ID, and `filter(title__icontains=term)` for a nonempty search. An absent category can mean no category restriction. A nonnumeric value should produce a controlled validation response or a clearly explained normalization policy. A numeric ID with no matching category can return an empty result or a documented error. Do not concatenate the search into SQL.

**Evaluation criteria — 1 mark each:**

- Correct foreign-key relationship and deletion-policy reasoning.
- Correct many-to-many relationship.
- Retrieves category/search from query parameters.
- Builds correct combined ORM filters.
- Handles missing, malformed, and nonmatching category values deliberately.

## Q9. Django admin customization — 5 marks

**Expected answer:** Register `Book` with a `ModelAdmin`. Default admin entry requires an active staff user, plus appropriate model permissions for operations; a superuser is useful for local setup but is not required for every operator. Configure `list_display = ("title", "price")`, `search_fields = ("title",)`, and `list_filter = ("is_available",)`. Register an action accepting `(modeladmin, request, queryset)` or an equivalent ModelAdmin method. Update only that queryset, e.g. `queryset.update(is_available=False)`, require change permission, and report the affected count. Bulk update is sufficient for this simple change; it bypasses per-object `save()` and save signals. Do not require that caveat for full marks unless it affects the proposed implementation.

**Evaluation criteria — 1 mark each:**

- Correct registration and staff/model-permission explanation.
- Correct list display.
- Correct search configuration.
- Correct filter configuration.
- Correct selected-queryset action, registration, permission, and feedback.

## Q10. Model inheritance — 5 marks

**Expected answer:** An abstract model declares `class Meta: abstract = True`; it has no separate table and contributes fields to concrete child models. Multi-table inheritance gives the concrete parent and child separate tables linked by an implicit one-to-one parent relationship. It suits a real parent/child entity design, but may require joins. Choose an abstract timestamp base when the goal is only to reuse `created_at` and `updated_at`, commonly using `auto_now_add` and `auto_now` respectively.

**Evaluation criteria — 1 mark each:**

- Explains abstract inheritance and its declaration.
- Explains absence of an abstract parent table and inherited child fields.
- Explains concrete parent/child tables in multi-table inheritance.
- Identifies the parent link and its implications.
- Justifies an abstract timestamp base for this requirement.

## Q11. Signals — 5 marks

**Expected answer:** Connect a receiver to `post_save` for the configured user model. Read `instance` and `created`, creating the one-to-one profile only when `created` is true. Import the signals module from the installed app's `AppConfig.ready()` so receivers are connected; avoid querying the database in `ready()`. A unique one-to-one relation and `get_or_create(user=instance)` can make creation robust against duplicate attempts. Signals allow decoupled reactions, but make side effects and execution flow less visible than an explicit call. Profile records are not automatically created just because a one-to-one relation exists.

**Evaluation criteria — 1 mark each:**

- Selects `post_save` and the correct sender/instance.
- Uses `created` to distinguish creation from subsequent saves.
- Enforces one profile per user and avoids duplicate creation.
- Explains handler registration through app initialization.
- Gives a meaningful decoupling-versus-visibility tradeoff.

## Q12. Schema-change debugging scenario — 5 marks

**Expected answer:** Reproduce the failing query and confirm both environments use the intended code revision, settings, and database connection. Inspect migration files and `showmigrations`, compare applied history with the schema, and review the pending operations before applying the correct migrations. Do not assume a successful local migration changed the other database. Do not delete shared history or fake migrations merely to silence an error. For an existing populated table, use a meaningful default if suitable, or add a temporary nullable field, backfill valid values, verify completion, and then make it required. Consider application writes during that transition; do not discard existing rows to satisfy a new constraint.

**Evaluation criteria — 1 mark each:**

- Checks code/settings/database differences before making changes.
- Inspects migration files and application status.
- Compares schema/history and applies the appropriate reviewed fix.
- Offers a valid default or staged nullable/backfill/required approach.
- Preserves existing data and verifies the change before relying on it.

## Q13. Middleware scenario — 5 marks

**Expected answer:** Middleware wraps request processing. With entries A, B, C, request handling proceeds A → B → C; responses return C → B → A for layers entered. A callable receives `get_response`, measures elapsed time around calling it, and returns the response. Register its dotted path in `MIDDLEWARE`. It may return early for unauthorized private requests. For Django session authentication, put session middleware before authentication middleware and the custom check after authentication middleware. Restrict only the intended area, exempt public/signup/authentication-entry URLs, and avoid redirecting a public authentication page back to itself. A JWT-protected API needs its configured JWT authentication layer; do not assume ordinary authentication middleware validates bearer tokens. Cross-cutting middleware checks do not replace per-object authorization.

**Evaluation criteria — 1 mark each:**

- Explains middleware placement and request/response order.
- Describes the `get_response` wrapper and duration measurement.
- Registers it and respects authentication dependencies.
- Implements a private-area authentication check with public exclusions.
- Explains early responses and prevents redirect loops.

## Q14. Signup and JWT scenario — 5 marks

**Expected answer:** Route the signup request to a view, bind/validate the input, reject invalid or duplicate email, and create the user using a password-hashing API such as `create_user()` or `set_password()` followed by save. Apply password validation explicitly where the selected creation flow does not do so. Never store or return the raw password. The default Django `User.email` is not unique, and the default model also requires a username: explain a deliberate username strategy when using it. A duplicate check alone can race; a dependable unique-email design needs a matching database constraint, for example through a suitable custom user model planned at project setup. Recognizing and explaining this mismatch in the training requirement is stronger than claiming the default model enforces uniqueness.

After successful creation and the applicable eligibility checks, Simple JWT can issue a refresh token with `RefreshToken.for_user(user)` and derive an access token. `for_user()` does not check active status itself. Access tokens authenticate protected requests and are normally short-lived; refresh tokens obtain replacement access tokens. A later API request typically sends `Authorization: Bearer <access_token>` to an endpoint configured with JWT authentication and permissions. Verification checks the signature, expiry, expected token type, and applicable user state; decoding unverified claims is insufficient. JWTs are signed, not inherently encrypted, so omit secrets from their claims.

**Evaluation criteria — 1 mark each:**

- Describes signup routing/input validation and useful invalid-input handling.
- Uses secure password creation and appropriate password validation.
- Recognizes the default-user email/username limitations and a sound uniqueness design.
- Explains post-signup issuance and access-versus-refresh purpose.
- Explains verification and permission checks on the later protected request.

Reviewer note: package installation details are not a separate mark. If discussed, the distribution is `djangorestframework-simplejwt`, imported as `rest_framework_simplejwt`; its standard integration uses Django REST Framework. Do not require a broader DRF syllabus.

## Q15. Protected profile scenario — 5 marks

**Expected answer:** For a current-user profile, resolve the identity from the authenticated request, not a caller-controlled ID. A session-authenticated Django view can use `login_required` and `request.user`, rendering only the required public-to-that-user fields in the template context. A JWT-authenticated endpoint must first run its configured JWT verifier and permission checks, then use the verified request identity. Merely hiding or disabling the ID input is not authorization. A regular unauthenticated HTML request should redirect to the configured authentication entry page; an API may instead return the appropriate authentication error. An issued token does not automatically create a Django session, attach itself to later requests, or get validated by ordinary `AuthenticationMiddleware`. Explain a coherent request transport/authentication flow and keep user data and password hashes out of unrelated responses.

**Evaluation criteria — 1 mark each:**

- Identifies the caller-controlled ID as the source of unauthorized disclosure.
- Derives the current user's data from a verified identity and enforces access server-side.
- Passes only intended fields to a template without exposing credentials.
- Handles an unauthenticated HTML request appropriately.
- Distinguishes JWT issuance/transport/verification from ordinary Django session authentication.

## Scorecard and interpretation

| Question | Score | Evidence / gaps |
|---|---:|---|
| Q1 | /5 | |
| Q2 | /5 | |
| Q3 | /5 | |
| Q4 | /5 | |
| Q5 | /5 | |
| Q6 | /5 | |
| Q7 | /5 | |
| Q8 | /5 | |
| Q9 | /5 | |
| Q10 | /5 | |
| Q11 | /5 | |
| Q12 | /5 | |
| Q13 | /5 | |
| Q14 | /5 | |
| Q15 | /5 | |
| **Total** | **/75** | |

Suggested interpretation: 60–75 indicates strong understanding of the reviewed material; 45–59 indicates workable understanding with targeted gaps; 30–44 indicates a need for guided practice; below 30 indicates a need to revisit foundations. These are suggested meeting criteria, not certification standards. Since preparation is intentional, credit clear reasoning and application rather than recitation alone.

Record serious misconceptions explicitly, especially plaintext password storage, trusting a submitted identity, or destructive migration advice. The total should not conceal a specific gap that needs correction before independent work. This meeting measures explanations and the requested code sketches; it does not establish competence in a complete production implementation.

**Strengths:** __________

**Priority learning gaps, with question IDs:** __________

**Agreed next learning task:** __________

## Technical references for the reviewer

- [Project setup](https://docs.djangoproject.com/en/5.2/intro/tutorial01/), [model fields](https://docs.djangoproject.com/en/5.2/ref/models/fields/), [migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/), and [queries](https://docs.djangoproject.com/en/5.2/topics/db/queries/) support Q1–Q4, Q8, and Q12.
- [Forms](https://docs.djangoproject.com/en/5.2/topics/forms/), [ModelForms](https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/), [static files](https://docs.djangoproject.com/en/5.2/howto/static-files/), and [file uploads](https://docs.djangoproject.com/en/5.2/topics/http/file-uploads/) support Q5–Q6.
- [Class-based views](https://docs.djangoproject.com/en/5.2/topics/class-based-views/intro/), [URL dispatcher](https://docs.djangoproject.com/en/5.2/topics/http/urls/), [admin](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/), and [admin actions](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/actions/) support Q7 and Q9.
- [Model inheritance](https://docs.djangoproject.com/en/5.2/topics/db/models/#model-inheritance), [signals](https://docs.djangoproject.com/en/5.2/topics/signals/), and [middleware](https://docs.djangoproject.com/en/5.2/topics/http/middleware/) support Q10–Q13.
- [Customizing authentication](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/), [using authentication](https://docs.djangoproject.com/en/5.2/topics/auth/default/), [Simple JWT integration](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/getting_started.html), and [manual token creation](https://django-rest-framework-simplejwt.readthedocs.io/en/stable/creating_tokens_manually.html) support Q14–Q15.
