Objective 1: 

1. We need a way to add these categories in the database first.
For that, I have added a CategoryModel with Post as a foreign key.

2. CategoryModel objects will be created at the time of adding the post. We have created "add_category" function which passes the post object being added as an argument.

3. add-category function calls the API functions and creates a new CategoryModel object for each category tag received from the API function call.

4. Last step is to display this in the template.
We create a property in the post model to retrieve all the category tags stored in the CategoryModel for the given post.

5. Like retrieving likes and comments, we loop through the list of category tags in the feed template, printing each one next to the post.