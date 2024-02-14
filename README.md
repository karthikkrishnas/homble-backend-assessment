# Homble Backend Assessment

This repository is for the assessment of the backend engineer position at Homble ([www.homble.in](https://www.homble.in)).

We are looking for devs to work on our API services that are built on Django (Python based web-framework) and Django REST Framework (DRF). We need devs to have a good knowledge of Django and know the basics of DRF (serializers, function based views, and authentication/ permissions).

Interested candidates are expected to fork this repo, build out the challenges listed below, and share their fork back with us. If you are familiar with Django and DRF, this entire assessment could take you about 2-4 hours depending on your current proficiency level.

## Background Information and Preparation

- Our backend is an API based on Django Rest Framework, so candidates are expected to be reasonably well versed with Python, Django, and DRF.
- Your code is expected to be run on Python 3.8 and Django 3.2. We understand that these are not the latest, but these are what we currently have in our production environment, so please code accordingly.
- This repo contains the source code, list of dependencies (requirements.txt), a small sqlite DB instance and a postman collection. We understand that including a DB instance in a repo is not a recommended practice but believe it works here to simply reduce and speed up the work that candidates are required to do.

**To begin working on this assessment:**

1. First fork this repo and make your fork private.
2. You can add the owner of this repo, `karthikkrishnas`, as a collaborator in your private fork. Do all of the work in your fork and push your commits to submit them for evaluation.
3. Set up your virtual environment based on Python 3.8 and activate it. Pip install the dependencies in requirements.txt, create your superuser account, and then run the Django dev server.
4. Go through the below overview section to get a general understanding of what the code base currently contains.
5. Log in to the Django Admin site using your superuser credentials and go through what's already there. Then open the included Postman collection in your Postman tool, go through and test out any available requests.

You are now ready to start coding, feel free to use any programming tools and aids you please. But do understand that you will later need to explain your work and make modifications on the fly during interactions with the Homble team.

This is the first time we are doing this assessment, your feedback is welcome at tech@homble.in. Please do reach out if you have any questions or difficulties.

Wish you all the best! 🙂

## Overview of the Repo

- The Django project folder is `mysite`, there are two apps: `products` and `categories`.
- DRF token authentication for the API views, and the usual password authentication for the Django Admin site.
- Products app has a model `Product`, and the categories app has a model `Category`. All models have migrations up to date.
- There is only one view (function based), in the Products app. 
- The default `db.sqlite3` instance is included and migrated up to date.
- A basic `postman_collection.json` is included and can be imported into your Postman tool.

## Our Expectations and Coding Style Guidelines

- Show us you are knowledgeable, organized, detail oriented and thorough.
- We have tried to write out our challenges clearly and in detail, at least initially, so that you get our general approach. Please do read the requirements carefully to ensure you understand exactly what is asked before you jump into writing code.
- We are first looking for readability and elegance (even if you cannot fully do what is asked), then effectiveness of the code (doing what is asked), and finally optimization of number of DB queries, time and memory.
- Needless to say, name things appropriately.
- Your comments need not say what you are doing (since we can just read your code for that), but should instead say why you are doing what you are doing (since we absolutely cannot read your mind). 🙂
- Keep the coding style and practices as consistent as possible with the existing code as the example. Also please use the default formatting from Black Formatter.
- Please populate reasonably sensible and typo free data in the DB, not junk values.
- Please create small git commits, one for each assessment module, so that we can understand how your code evolved with the changing challenges. Please provide reasonable commit summaries and descriptions.
- Create migrations as you go along and migrate the included DB, so that you can just share it back with us in the repo. Also, update the Postman collection as you test out your new views, and then finally export it to update the repo’s json collection.
- Do code the challenges in the given order, and create a separate commit for each assessment module.
- We only want DRF function based views. No Django views or templates.

## Required Challenges

This section has 3 modules, so we need 3 commits.

### Extend the Product model and API:
- Extend the existing `products_list` view to accept a query parameter to show only refrigerated products or only non-refrigerated products. The existing functionality of showing all products should be the default if the query parameter is not provided or is empty.
- Add a field `edited_at` to automatically save the timestamp of the most recent object edit.
- Add a new charfield for ingredients with max 500 chars.
- Add the new fields as appropriate to the existing Admin interface and Product model serializer(s).
- Create the migration and migrate the DB.
- Update some reasonable data for the new fields via Django Admin.
- Create a new request, if required, in the Postman collection to test the view(s).

### Extend the Category model and API:
- Create a property `count_products` for model Category to count the number of products in each model. And show this in the Django CategoryAdmin interface in both the list page (`list view`) and in the change page form (`detail view`).
- Create a `CategorySerializer` (only reads, no writes required) in a new file `categories/serializers.py` that explicitly shows all the existing fields of the category, and has the following additional fields:
  - `count_products` - shows the property value
  - `products` - shows a list of all products, nested here using the existing `ProductListSerializer`
- Create a new view (only for admin/staff users) to show a list of all categories with all related products nested within. Use a rest_framework permission.
- Create a new request, if required, in the Postman collection to test the view(s).

### Add a new model Sku (short for store keeping unit):
- Create Sku to allow us to have different sizes for a Product, e.g., 200 gm vs 500 gm. Right now, let's use only grams to represent the different sizes. Also, the price field should effectively move from Product to Sku now. 
- Define the Sku model in the products app. Ensure at least the below fields, add any more you think are required. Also define its `__str__` representation to include the product name.
  - `id` - default pk
  - `product` - ForeignKey to Product model
  - `size` - PositiveSmallIntegerField
  - `price`
- For a given product, the `size` field has to be unique. Implement it.
- Create an Admin interface for the same to show all fields and properties. Use autocomplete for the product field. Also, add Sku as an inline in ProductAdmin.
- Create the migration and migrate the DB
- Add some reasonable new Sku objects (1-3 for each product) in the DB via Django Admin.

## Bar Raiser Challenges

This section has 3 modules, so we need 3 commits. Will you raise the bar?

### Extend the price functionality, plus management command:
- Now you can drop the `price` field from the Product table. And simultaneously, we also need more granularity in price fields in the SKU table.
- We need the following in Sku:
  - `price` field name to change to `selling_price`
  - new field `platform_commission` - PositiveSmallIntegerField
  - new field `cost_price` - PositiveSmallIntegerField
- Override the model save method to always set `selling_price` = `cost_price` + `platform_commission` while saving.
- Update Admin interfaces, serializers, and other code as you see fit.
- If there were a lot of existing Sku records when we added these new price fields, we would need to automatically update the price fields, and not do it individually via Django Admin. Do this with a management command using Django’s `BaseCommand` (and not `migrations.RunPython`). Assume that our DevOps setup ensures that this management command is automatically run immediately after the `migrate` command (but you can run it manually in your dev env).
- In the command, use a queryset update to make the `platform_commission` to 25% of `selling_price` and the `cost_price` to the difference of the two.
- Now migrate the DB and run the management command in your dev.

### Extend the Sku model and API, plus permissions:
- We want to be able to have Sku in terms of gm, kg, mL, L, and pc (piece). Add a field `measurement_unit` with choices defined via a list of ordered pairs.
- Next, add a validator to the Sku `size` field to ensure that it has a maximum value of 999.
- Add a field called `status` using `IntegerChoices`, but display only understandable text in the API (and not the integer value). Let's have choices as below: 
  - Pending for approval (default)
  - Approved
  - Discontinued
- Create a new view (admin/staff only) to create an Sku, status should always go to default for a new Sku, even if something else is provided.
- Create a new view to display all details of a single product, also nesting all of its approved Skus within. 
- While displaying the Skus above, we also need a field called `markup_percentage` which is calculated as `platform_commission` divided by the `cost_price`.
- Create a user group “Supervisors” via Django Admin. Provide Sku edit permission to Supervisors.
- Create a new view for only admins with Sku edit perm to be able to edit an Sku status.
- Update all the Admin interfaces as you see fit. Create/update any other parts of the code as you see fit.
- Then migrate and finally test in Postman.

### Querysets

You can provide each requirement below in a simple separate convenience view that basically only does the queryset work. If you think there are multiple ways to do any of the below, it would be great to see all. We are not looking for any brute force solutions, how could we do each of the below with minimal DB queries and minimal python iteration?

- Print/output in any way you please: queryset containing all active categories including a count of its approved SKUs.
- Print/output in any way you please: queryset containing all Skus including its category.
