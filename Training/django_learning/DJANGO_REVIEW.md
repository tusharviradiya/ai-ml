# Django learning review: junior backend developer

**Purpose:** Assess understanding, debugging, and implementation after the six training topics. Completion marks in the screenshots indicate training progress, not demonstrated competence; this document is an assessment instrument, not a completed evaluation.

**Candidate:** __________ **Reviewer:** __________ **Date:** __________
**Python/Django versions used:** __________ **Database:** __________

## Coverage and assessment format

| Screenshot | Covered material | Review questions | Maximum |
|---|---|---|---:|
| [topic_1.png](topics_ss/topic_1.png), Day 15, tickets 1–2 | Project setup, structure, settings, URL configuration | Q1–Q2 | 8 |
| [topic_2.png](topics_ss/topic_2.png), Day 16, tickets 3–4 | Models, fields, database configuration, migrations, ORM | Q3–Q6 | 16 |
| [topic_3.png](topics_ss/topic_3.png), Day 17, tickets 5–6 | Requests, basic views/URLs, templates, dynamic content | Q7–Q9 | 12 |
| [topic_4.png](topics_ss/topic_4.png), Day 18, tickets 7–8 | Query parameters, class-based views, regex URLs, namespaces | Q10–Q12 | 12 |
| [topic_5.png](topics_ss/topic_5.png), Day 19, tickets 9–10 | Forms, submission, validation, behavior and appearance | Q13–Q17 | 20 |
| [topic_6.png](topics_ss/topic_6.png), Day 20, tickets 11–12 | Admin access, registration, customization, actions, filters | Q18–Q20 | 12 |
| Integrated practical | Apply the six topics together | P1 | 20 |
| **Total** | | | **100** |

Suggested format: two sessions, with 75–90 minutes for Q1–Q20 and 60–75 minutes for P1. Allow more time if the candidate must create the practical project from scratch. Read only the prompts and follow-ups to the candidate; keep the answer key private. Permit official documentation during the practical, and require the candidate to explain submitted code. Exact API spelling from memory matters less than correct reasoning.

Each oral question has four independent one-point criteria, including the follow-up. Award 0, 0.5, or 1 for each criterion: absent/incorrect, partly correct or reached after substantial hints, or correct with a clear explanation. Record hints. Do not deduct twice for the same omission within one question. Equivalent working approaches earn credit.

Difficulty progresses from foundation checks into moderate and hard application. Hard questions extend the covered material through edge cases; do not expect senior-level infrastructure knowledge. Authentication is supplied context for a few scenarios, not a separate authentication syllabus. DRF, Celery, deployment architecture, and advanced async internals are outside this review.

## Shared example

Use a task tracker throughout:

- A `Project` has a name and a unique slug.
- A `Task` belongs to a project and has a title, description, status (`todo`, `doing`, `done`), optional due date, and creation timestamp.
- Task titles need not be unique. Assume project deletion must be blocked while tasks reference it.
- Lists can be filtered by status and searched by title. Staff manage records through Django admin.
- Where a question uses an owner, assume authentication already exists and an owner relation is available.

The examples use Django 5.2 documentation as an explicit reference baseline, not an assumption about the training environment. Accept equivalent APIs supported by the candidate's declared version.

## 1. Project foundations — 8 points

### Q1. Create the project and explain its structure — Foundation, 4 points

**Prompt:** Starting in an empty working directory with Django installed in an active virtual environment, create project `config` and app `tasks`. Explain project versus app, and identify the purpose of the generated files. Where would database settings and the first route go?

**Expected answer:** Use `django-admin startproject config .` and `python manage.py startapp tasks`. A project assembles configuration and apps; an app groups related functionality. `manage.py` runs project commands; `settings.py` contains configuration; root `urls.py` starts routing; `wsgi.py`/`asgi.py` expose server entry points. Add the app config to `INSTALLED_APPS`. An app URLconf is usually created manually and included from the root URLconf. [Reference: project/app tutorial](https://docs.djangoproject.com/en/5.2/intro/tutorial01/).

**Follow-up:** Why might `makemigrations tasks` report that the app is not installed even though its directory exists?

**Expected follow-up:** Check the selected settings module and `INSTALLED_APPS`; a directory alone does not register an app.

**Score, 1 point each:** correct commands; project/app distinction; correct file responsibilities; registration/settings diagnosis.

### Q2. Trace a request and diagnose configuration — Moderate, 4 points

**Prompt:** Trace `GET /tasks/` from Django receiving the request to returning rendered HTML. The server starts, but the URL returns 404. What would you inspect first?

**Expected answer:** Middleware participates around request/response handling; URL resolution selects a view; the view uses models/services as needed, renders a template with context, and returns an HTTP response. Inspect the root URLconf, app `include()`, matching path, and trailing slash. Distinguish routing failure from a view deliberately raising 404.

**Follow-up:** The view runs, but raises `TemplateDoesNotExist`. Does changing `ALLOWED_HOSTS` fix it?

**Expected follow-up:** No. Inspect the requested template name, directory layout, template engine settings, and app registration. `ALLOWED_HOSTS` addresses host validation.

**Score, 1 point each:** coherent request trace; correct separation of responsibilities; systematic 404 checks; template/configuration distinction.

## 2. Models, databases, migrations, and ORM — 16 points

### Q3. Design the data model — Moderate, 4 points

**Prompt:** Sketch the two models. Explain your field types, relationship, deletion rule, defaults, and optional-field behavior.

**Expected answer:** Use a bounded `CharField` for name/title, unique `SlugField` for project slug, `TextField(blank=True)` for description, status choices with a sensible default, `DateField(null=True, blank=True)` for optional due date, and a creation timestamp. Use `ForeignKey(Project, on_delete=models.PROTECT, related_name="tasks")`. `blank` controls validation while `null` controls database NULL storage; optional strings usually use empty strings rather than NULL. [Reference: model fields](https://docs.djangoproject.com/en/5.2/ref/models/fields/).

**Follow-up:** Does `choices=` alone prevent every invalid status written directly to the database?

**Expected follow-up:** No. Choices support Django validation; a database check constraint is needed if all database writes must enforce the allowed set.

**Score, 1 point each:** appropriate field types/defaults; relationship and `PROTECT`; correct `blank`/`null`; validation versus database enforcement.

### Q4. Explain and debug migrations — Moderate, 4 points

**Prompt:** You add `due_date`, but the page reports “no such column.” Explain `makemigrations` versus `migrate`, then give a safe diagnosis sequence. Include database configuration.

**Expected answer:** Confirm the active settings and `DATABASES` connection, check the model and app registration, generate/review the migration, inspect `showmigrations`, and apply it to the intended database. `makemigrations` compares model state with migration history; it does not discover arbitrary live-schema changes. `migrate` applies migration operations. Commit migration files with model changes. [Reference: migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/).

**Follow-up:** It works locally. Is deleting committed migrations and regenerating them a safe default fix for a shared environment?

**Expected follow-up:** No. First inspect migration history, dependencies, and schema drift. Prefer an intentional forward migration; avoid destroying shared history or data.

**Score, 1 point each:** command distinction; connection/settings checks; history/apply workflow; safe shared-history reasoning.

### Q5. Change an existing table safely — Hard, 4 points

**Prompt:** A populated `Project` table needs a new required, globally unique slug. Why is giving every existing row the default `"project"` problematic? Propose a migration sequence.

**Expected answer:** A common default collides under uniqueness. Add an intermediate nullable field, populate distinct values using a data migration and historical models, resolve collisions, then enforce uniqueness and non-nullability. Account for slug length and existing data. Coordinate application writes during the transition so new NULLs or duplicates cannot invalidate the final step. [Reference: data migration guidance](https://docs.djangoproject.com/en/5.2/howto/writing-migrations/#migrations-that-add-unique-fields).

**Follow-up:** What would you verify before applying this to the shared database?

**Expected follow-up:** Rehearse against representative existing data; check generated operations, uniqueness/null counts, backup/recovery options, and write coordination. A rollback may not restore discarded data automatically.

**Score, 1 point each:** collision diagnosis; staged schema/data sequence; collision/concurrent-write handling; concrete verification/recovery plan.

### Q6. Query correctly and explain query cost — Hard, 4 points

**Prompt:** Write a query for unfinished tasks whose title contains a search term, newest first. Explain `filter()` versus `get()`. A list template also displays `task.project.name` for every row; why might that become slow?

**Expected answer:** For example, `Task.objects.exclude(status="done").filter(title__icontains=term).select_related("project").order_by("-created_at", "-pk")`. `filter()` returns a queryset; `get()` expects exactly one object and can raise `DoesNotExist` or `MultipleObjectsReturned`. Querysets are lazy. Per-row relationship access can cause N+1 queries; `select_related` suits this foreign key. [Reference: querying](https://docs.djangoproject.com/en/5.2/topics/db/queries/).

**Follow-up:** Would you use the same optimization to load each project's reverse `tasks` collection? How would you verify improvement?

**Expected follow-up:** Use `prefetch_related("tasks")` for the reverse collection; compare query counts on representative data, for example with `assertNumQueries` or a query inspection tool. [Reference: queryset relationship loading](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#prefetch-related).

**Score, 1 point each:** correct filtering/order; retrieval semantics/laziness; N+1 explanation and foreign-key fix; reverse relation and measurement.

## 3. Basic views, URLs, and templates — 12 points

### Q7. Build a detail view — Moderate, 4 points

**Prompt:** Sketch the route and function-based view for `/tasks/42/`, rendering `tasks/detail.html`. What should happen for an unknown task? Should reading this URL change its status?

**Expected answer:** Use `path("tasks/<int:pk>/", views.task_detail, name="task-detail")`; resolve with `get_object_or_404(Task, pk=pk)` and return `render(request, "tasks/detail.html", {"task": task})`. A missing object returns 404. GET should read data without intentionally changing application state. [References: view shortcuts](https://docs.djangoproject.com/en/5.2/topics/http/shortcuts/), [HTTP method guidance](https://docs.djangoproject.com/en/5.2/topics/security/#csrf-protection).

**Follow-up:** Does an integer path converter prove that a task exists?

**Expected follow-up:** No. It validates/converts the path segment; the view still needs object lookup.

**Score, 1 point each:** route/argument agreement; lookup and missing-object behavior; render/context response; GET semantics and converter limitation.

### Q8. Render useful, safe templates — Moderate, 4 points

**Prompt:** Describe a list template with a shared page layout, task links, dynamic titles, and a message when the list is empty. How should a user-entered title containing `<script>` be displayed?

**Expected answer:** Use template inheritance (`extends`/`block`), a context variable, `for`/`empty`, and named URL reversal for links. Keep data selection in Python. Django templates autoescape ordinary variable output in HTML; avoid marking untrusted content `safe`. [Reference: templates](https://docs.djangoproject.com/en/5.2/topics/templates/).

**Follow-up:** Why can the same text be unsafe if inserted into JavaScript even though the HTML page uses autoescaping?

**Expected follow-up:** Escaping is context dependent; use an appropriate structured mechanism such as `json_script` and parse the resulting data rather than interpolating raw text into executable JavaScript. [Reference: `json_script`](https://docs.djangoproject.com/en/5.2/ref/templates/builtins/#json-script).

**Score, 1 point each:** inheritance/context; loop/empty state and links; escaping/untrusted HTML; JavaScript-context reasoning.

### Q9. Debug rendering with evidence — Moderate, 4 points

**Prompt:** `/tasks/` responds with 200, but the list is blank despite database rows. Give an investigation sequence that distinguishes data, view, and template problems.

**Expected answer:** Verify the active database and expected rows, inspect filters and the view's context key, confirm the template actually loaded, then inspect its loop variable and inheritance blocks. Reproduce with one known matching task. A successful status code alone does not establish correct content.

**Follow-up:** What regression checks would distinguish “no matching tasks” from “we forgot the context variable”?

**Expected follow-up:** Check response context/content for a known matching record and separately check the intentional empty-state message for an empty queryset.

**Score, 1 point each:** database/filter isolation; context/template inspection; reproducible investigation; meaningful populated/empty checks.

## 4. Advanced views and URL patterns — 12 points

### Q10. Validate query parameters — Moderate, 4 points

**Prompt:** Implement the behavior of `/tasks/?status=todo&q=invoice&page=2`. Where do those values come from? Define behavior for an unknown status and a nonnumeric page. How does the route change?

**Expected answer:** Read `request.GET`; the path route remains unchanged. Validate status against allowed values, trim/limit search input as appropriate, apply ORM filters, and paginate with stable ordering. State a consistent policy: reject invalid filters with a useful error or normalize them deliberately. `Paginator.get_page()` can provide forgiving page handling. [References: request query data](https://docs.djangoproject.com/en/5.2/ref/request-response/#django.http.HttpRequest.GET), [pagination](https://docs.djangoproject.com/en/5.2/topics/pagination/).

**Follow-up:** Is `order_by(request.GET["sort"])` a good unrestricted sorting API?

**Expected follow-up:** Map public sort options to an allowlist of supported fields; unexpected fields can cause errors, expensive work, or expose unintended ordering behavior. Do not mislabel every such case as SQL injection.

**Score, 1 point each:** query/path distinction; validation policy; stable pagination; sorting allowlist and accurate reasoning.

### Q11. Explain class-based views through a change — Moderate–Hard, 4 points

**Prompt:** Convert the filtered task list to `ListView`. Explain `as_view()`, `get_queryset()`, and `get_context_data()`. When would a function-based view be clearer?

**Expected answer:** `as_view()` exposes a callable that instantiates the view and dispatches the request. Put request-dependent filtering in `get_queryset()`; add context via `get_context_data()` while preserving `super()`. Generic views reduce repeated list/detail behavior; a small custom workflow may be clearer as a function. [Reference: class-based view introduction](https://docs.djangoproject.com/en/5.2/topics/class-based-views/intro/).

**Follow-up:** Why is storing a request's selected status in a mutable class-level dictionary a bug?

**Expected follow-up:** That mutable object can be shared across requests. Keep request-specific values on the per-request instance or in local variables.

**Score, 1 point each:** callable/dispatch explanation; correct filtering hook; context inheritance and justified view choice; shared-state diagnosis.

### Q12. Resolve routing and reversal bugs — Hard, 4 points

**Prompt:** Two apps both name a URL `detail`. Show how the tasks app can use `app_name = "tasks"`, a named integer route, and `include()` so callers can reverse `tasks:detail`. When is `re_path()` useful?

**Expected answer:** In `tasks/urls.py`, define `app_name = "tasks"` and `path("<int:pk>/", views.task_detail, name="detail")`; include it at `path("tasks/", include("tasks.urls"))`. Reverse with `reverse("tasks:detail", kwargs={"pk": 42})` or the template URL tag. Prefer converters for common patterns; regex supports restrictions such as `r"^archive/(?P<year>[0-9]{4})/$"`. URL patterns are checked in order. [Reference: URL dispatcher](https://docs.djangoproject.com/en/5.2/topics/http/urls/).

**Follow-up:** Why might putting `<slug:slug>/` before `new/` break a create page? Is regex `year` automatically an integer?

**Expected follow-up:** The broad slug route matches `new` first; put the literal first or redesign. Regex captures are strings unless explicitly converted later.

**Score, 1 point each:** include/namespace setup; correct reversal; converter/regex use; ordering and capture-type reasoning.

## 5. Forms, validation, and submission — 20 points

### Q13. Choose a form and protect editable fields — Moderate, 4 points

**Prompt:** Choose `Form` or `ModelForm` for a contact message and for creating a task. Define which task fields the browser may submit. Why avoid `fields = "__all__"` here?

**Expected answer:** A plain `Form` suits input not directly tied to a model; `ModelForm` derives fields/validation and persistence helpers from a model. Explicitly allow title, description, status, due date, and project if appropriate. An owner must be assigned from trusted server context. An explicit allowlist prevents later model additions from silently becoming editable. [Reference: ModelForms and field selection](https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/#selecting-the-fields-to-use).

**Follow-up:** If a project dropdown must contain only the current user's projects, is filtering its visible HTML options sufficient?

**Expected follow-up:** No. Restrict the form field's server-side queryset so forged project IDs fail validation; retain appropriate authorization in the view.

**Score, 1 point each:** justified form choice; explicit fields; trusted assignment/allowlist reasoning; server-side relationship restriction.

### Q14. Implement the submission lifecycle — Moderate, 4 points

**Prompt:** Describe create-form behavior for GET, invalid POST, and valid POST. Explain why `TaskForm(request.POST or None)` can mis-handle an empty POST.

**Expected answer:** Branch on `request.method`. GET gets an unbound form; POST gets a bound form, calls `is_valid()`, persists only valid input, and redirects after success. Invalid POST renders the same bound form with errors. An empty POST is falsy; `or None` can turn it into an unbound form and suppress expected validation errors. [Reference: working with forms](https://docs.djangoproject.com/en/5.2/topics/forms/).

**Follow-up:** Does redirecting after success guarantee that a double-click or retried POST cannot create duplicates?

**Expected follow-up:** No. It reduces refresh resubmission; stronger duplicate protection needs an appropriate uniqueness rule or idempotency design when required.

**Score, 1 point each:** explicit method/binding; validation before persistence; bound errors/success redirect; empty-POST and duplicate distinction.

### Q15. Place validation at the right level — Hard, 4 points

**Prompt:** Reject whitespace-only titles and require a due date when status is `doing`. Where do you implement each rule? How do you surface errors without crashing on another invalid field?

**Expected answer:** Use field validation/`clean_title()` for the title, returning its cleaned value; use `clean()` and `super().clean()` for the cross-field rule. Read possibly missing cleaned values with `.get()`, then raise `ValidationError` or use `add_error()` for a targeted error. Preserve parent ModelForm validation behavior. [Reference: form validation](https://docs.djangoproject.com/en/5.2/ref/forms/validation/).

**Follow-up:** Can browser `required` attributes or a date widget enforce these rules for all callers?

**Expected follow-up:** No. Browser checks improve usability; direct HTTP requests bypass them. Enforce invariants server-side and, where applicable, at the database layer.

**Score, 1 point each:** single-field placement/return; cross-field cleaning; missing-value and error handling; server-side enforcement distinction.

### Q16. Review a broken form handler — Hard, 4 points

**Prompt:** Identify the failures and describe a corrected request flow:

```python
def create_task(request):
    if request.method == "GET":
        Task.objects.create(title=request.GET.get("title", ""))
    form = TaskForm(request.POST)
    if form.is_valid():
        form.save()
    return render(request, "tasks/form.html", {"form": TaskForm()})
```

**Expected answer:** GET mutates state and supplies no required project. The form is bound regardless of method, and the returned fresh form discards errors and entered values. Use an explicit GET/POST lifecycle, save only a valid POST, redirect on success, and render the bound invalid form. The POST template needs `{% csrf_token %}` with CSRF middleware enabled. [References: forms](https://docs.djangoproject.com/en/5.2/topics/forms/), [CSRF protection](https://docs.djangoproject.com/en/5.2/howto/csrf/).

**Follow-up:** Should a developer fix a 403 by adding `csrf_exempt`? Does a valid CSRF token prove permission to edit any task?

**Expected follow-up:** Diagnose missing token/cookie and origin configuration first. CSRF checks do not replace user/object authorization.

**Score, 1 point each:** GET/incomplete-create diagnosis; correct binding; errors/redirect repair; CSRF handling and authorization distinction.

### Q17. Customize and edit a form safely — Hard, 4 points

**Prompt:** Change title placeholder/CSS and due-date input appearance. Then explain how the same ModelForm updates an existing task rather than creating a new one. Assume only its owner may edit it.

**Expected answer:** Configure widgets/attributes while retaining labels and errors; presentation does not replace validation. Fetch the task through an owner-scoped queryset (or perform an equivalent permission check). Pass `instance=task` on both GET and POST, validate, save, and redirect. [References: ModelForm widgets](https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/#overriding-the-default-fields), [generic editing patterns](https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-editing/).

**Follow-up:** What happens if the POST form omits `instance`? How do you verify the fix?

**Expected follow-up:** It generally creates a new record on save. Verify that the existing row changes, the row count stays fixed, and an unauthorized user cannot modify it.

**Score, 1 point each:** appropriate widget customization; authorized retrieval; correct instance/update lifecycle; duplicate and access verification.

## 6. Django admin — 12 points

### Q18. Diagnose admin access and registration — Moderate, 4 points

**Prompt:** The admin page loads, but a newly created normal user cannot enter it. After access is fixed, `Task` is missing. What do you check?

**Expected answer:** Default admin access requires an active staff user; staff status alone does not grant all model permissions. Check model permissions, app installation, model registration in `admin.py`, admin URL inclusion, and migrations for required tables. A superuser is convenient for local setup, not the required role for every operator. [Reference: admin](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/).

**Follow-up:** Does registering a model make its admin screens available to anonymous users?

**Expected follow-up:** No. Registration exposes the model through admin's access/permission system.

**Score, 1 point each:** active/staff requirement; model permissions; registration/configuration diagnosis; anonymous/superuser distinction.

### Q19. Make the admin useful — Moderate, 4 points

**Prompt:** Design `TaskAdmin` so staff see title, project, status, and due date; search title/project name; filter by status; and see creation time without editing it. How would you offer a custom “overdue” filter?

**Expected answer:** Use `list_display`, `search_fields = ("title", "project__name")`, `list_filter = ("status",)`, and `readonly_fields = ("created_at",)`. Use `SimpleListFilter` with `lookups()` and `queryset()` for overdue/not-overdue choices; define overdue using a past due date and unfinished status. [Reference: ModelAdmin options and filters](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter).

**Follow-up:** Displaying project names causes extra queries. What can you configure, and are read-only fields a general API security mechanism?

**Expected follow-up:** Use `list_select_related = ("project",)` or customize the admin queryset. `readonly_fields` affects the admin form; other write paths need their own controls.

**Score, 1 point each:** display/search configuration; standard filter/read-only setup; custom-filter design; query cost and scope of read-only protection.

### Q20. Implement a custom action deliberately — Hard, 4 points

**Prompt:** Add “mark selected tasks done.” Describe the function signature, registration, permission, and feedback. Is `queryset.update(status="done")` always equivalent to saving each task?

**Expected answer:** An action receives `(modeladmin, request, queryset)`; register it in `actions`, use `@admin.action(description=..., permissions=["change"])`, and report the updated count with `message_user`. Bulk update is efficient for a simple transition, but bypasses model `save()` and save signals. If transitions require per-object logic, use the appropriate business operation and transaction/error strategy. [Reference: admin actions](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/actions/).

**Follow-up:** A model's `save()` override calls `full_clean()`. Does that validation run for `queryset.update()`? Does ordinary model `save()` automatically call `full_clean()`?

**Expected follow-up:** Neither. Bulk update bypasses the override; ordinary `save()` does not automatically run full model validation. [Reference: model instance validation](https://docs.djangoproject.com/en/5.2/ref/models/instances/#django.db.models.Model.full_clean).

**Score, 1 point each:** action interface/registration; permission/feedback; bulk-update tradeoff; accurate validation semantics.

## 7. P1: Integrated practical — Hard, 20 points

### Candidate brief

Build a small task tracker from the shared example in a local sandbox. The reviewer may provide a fresh project scaffold and dependencies. Include migrations and enough seed data to demonstrate filtering. Use Django's built-in templates/forms; visual polish is not scored.

1. Implement `Project` and `Task`, including the protected relationship, unique project slug, valid statuses, and optional due date. Generate/apply migrations.
2. Provide a named, namespaced task list and detail page. The list supports status filtering, title search, deterministic pagination, and an empty state. The detail page returns 404 for a missing task. Use a class-based view for the list; other views may use either style.
3. Create tasks through a ModelForm with explicit fields. Enforce nonblank titles and a due date for `doing` tasks. Show errors while retaining input. Use POST with CSRF protection and redirect on success.
4. Add an edit page that updates an existing task. Assume this exercise's regular pages are available to a trusted local reviewer; owner-based authorization is assessed verbally in Q17. Do not spend the exercise implementing login.
5. Register both models in admin. Configure task display, search, status filter, an overdue `SimpleListFilter`, and the selected-task completion action.
6. Demonstrate the acceptance checks below. Automated tests are welcome; documented, repeatable manual checks are acceptable within the time limit. Explain one failed check and your diagnosis if a failure occurs.

### Reviewer reference flow

Expected structure: models/migrations → app URLconf included by project → filtered/paginated list queryset → detail lookup → ModelForm cleaning → explicit GET/POST handling → bound-error render or successful save/redirect → customized admin. A valid create path saves one row; a valid edit changes that row. Data selection belongs in the view/queryset and validation belongs in the form/model as appropriate.

The following is a reference lifecycle, not a complete solution. It assumes `TaskForm`, models, namespaced routes, and templates have already been defined:

```python
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import TaskForm
from .models import Task


@require_http_methods(["GET", "POST"])
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return redirect("tasks:detail", pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/form.html", {"form": form})
```

For the owner-restricted variant in Q17, scope the object lookup to the current user's allowed tasks before binding the form. CSRF belongs in the POST template and middleware configuration.

### Acceptance checks and practical scoring

Award one point for each independently demonstrated check, up to four per row. Give half credit for a partially working implementation with a correct diagnosis. Do not award points for code the candidate cannot explain.

| Area | Four checks, one point each | Maximum |
|---|---|---:|
| Data and migrations | Correct field/status definitions; relationship blocks project deletion; migrations apply to a fresh local database; missing/duplicate project slug is rejected through the relevant validation/constraint path | 4 |
| URLs, views, templates | Namespaced list/detail links resolve and missing detail is 404; search/status behavior including invalid status is demonstrated; deterministic pagination handles an invalid page by the stated policy; dynamic list and empty state render correctly | 4 |
| Forms and updates | Invalid title and cross-field rule produce visible errors with retained input; valid POST creates one row and redirects; edit changes the same row without increasing count; GET performs no write and POST uses CSRF protection | 4 |
| Admin | Both models registered and useful display/search; status and overdue filters work; action changes only selected rows and reports count; a staff user without change permission cannot invoke the change action | 4 |
| Problem-solving evidence | Reproducible setup/check instructions; observes database/query behavior rather than guessing; isolates and explains a defect or deliberately introduced bug; explains one implementation tradeoff and a concrete next improvement | 4 |
| **Practical total** | | **20** |

For the CSRF check, use a browser or a test client configured with `enforce_csrf_checks=True`; the default Django test client bypasses CSRF checks. For the admin permission check, use a staff account with view permission but without change permission. For the migration check, use a disposable database, preserving any existing workspace data.

**Practical follow-ups:**

- **Scenario:** The same POST is submitted twice. **Expected:** Explain that redirecting does not guarantee deduplication; discuss a suitable idempotency/constraint strategy if duplicate prevention becomes a requirement.
- **Scenario:** The list has 100 rows and project names trigger roughly one query per row. **Expected:** Demonstrate relationship loading and compare query counts.
- **Scenario:** The completion action must now send notifications. **Expected:** Recognize that bulk update does not emit save signals; propose an explicit transition operation and discuss reliable notification handling at an appropriate level.

These follow-ups deepen the discussion; they add no points beyond the 100-point total.

## 8. Scorecard and decision guidance

| Area | Score | Evidence / hints / misconceptions |
|---|---:|---|
| Foundations, Q1–Q2 | /8 | |
| Data and ORM, Q3–Q6 | /16 | |
| Basic views/templates, Q7–Q9 | /12 | |
| Advanced views/routing, Q10–Q12 | /12 | |
| Forms, Q13–Q17 | /20 | |
| Admin, Q18–Q20 | /12 | |
| Practical, P1 | /20 | |
| **Total** | **/100** | |

| Total | Interpretation | Suggested next step |
|---|---|---|
| 85–100 | Strong junior understanding with demonstrated application | Assign a bounded feature with normal review; revisit any weak area |
| 70–84 | Meets the learning target with identifiable gaps | Assign small features with focused review and targeted exercises |
| 55–69 | Partial understanding; application still inconsistent | Pair on a feature, then reassess weak topics using a new scenario |
| Below 55 | Foundations need reinforcement | Repeat a guided build and require an independent explanation/demo |

Use the score as evidence alongside observed work. A “meets target” result requires at least 12/20 on P1 and at least half the points in both data/ORM and forms. Otherwise record “needs practical reinforcement,” even when the aggregate exceeds 70. These thresholds are proposed reviewer criteria, not an external certification standard.

Record unresolved risks specifically: writes on GET, bypassed server validation, discarded errors, unsafe shared-database migration advice, or missing authorization in an owner-restricted scenario. Explain the consequence, request a correction, and record whether the candidate can fix it; avoid turning a single initial mistake into an unexplained blanket failure.

**Reviewer conclusion:** __________

**Three strongest demonstrated skills:** __________

**Three gaps with supporting question/check IDs:** __________

**Next exercise and observable success criteria:** __________

**Reassessment date:** __________
