---
name: README and Workflow
overview: Create a comprehensive README that documents setup, architecture, user workflow, implemented functions, pending work, and known bugs based on current code state.
todos:
  - id: inventory-code-features
    content: Map implemented functions and features per app from views/models/urls
    status: pending
  - id: document-pending-items
    content: List unfinished placeholders and missing test coverage
    status: pending
  - id: document-known-bugs
    content: Record concrete code-level bugs/risks with actionable notes
    status: pending
  - id: write-readme
    content: Create/update README.md with setup workflow, app workflow, and status sections
    status: pending
  - id: final-sanity-pass
    content: Verify README clarity, consistency, and alignment with current code
    status: pending
isProject: false
---

# README Creation Plan

## Goal
Make a clear and easy `[README.md](README.md)` in simple English.

It will explain:
- what this project does,
- how to run it,
- how users move through the app (workflow),
- what is already working,
- what is not finished,
- what known bugs are there.

## Files I Will Use
I will read these files to write correct README content:
- App routes: `[soledrop/urls.py](soledrop/urls.py)`, `[accounts/urls.py](accounts/urls.py)`, `[products/urls.py](products/urls.py)`, `[cart/urls.py](cart/urls.py)`, `[orders/urls.py](orders/urls.py)`
- Main logic: `[accounts/views.py](accounts/views.py)`, `[products/views.py](products/views.py)`, `[cart/views.py](cart/views.py)`, `[orders/views.py](orders/views.py)`
- Data models: `[accounts/models.py](accounts/models.py)`, `[products/models.py](products/models.py)`, `[cart/models.py](cart/models.py)`, `[orders/models.py](orders/models.py)`
- Settings and packages: `[soledrop/settings.py](soledrop/settings.py)`, `[requirements.txt](requirements.txt)`

## README Sections
- **About Project**: short intro of SoleDrop.
- **Tech Used**: Django, SQLite, templates, static files, and libraries.
- **How To Run**:
  - create virtual environment,
  - install requirements,
  - run migrations,
  - create admin user,
  - start server.
- **Workflow**:
  - Home -> Shop -> Product Page -> Add to Cart -> Checkout -> Order Confirmation.
  - Also mention login, profile, and wishlist flow.
- **Implemented Functions**:
  - list working functions by app (`accounts`, `products`, `cart`, `orders`).
- **Left To Implement**:
  - list unfinished functions/pages and missing tests.
- **Known Bugs**:
  - list real issues found in code in simple words.
- **Next Steps**:
  - short action list to improve project.

## Diagram
Add one Mermaid workflow diagram in README for easy understanding.