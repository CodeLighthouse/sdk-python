---
tags: [python, sdk]
---

# CodeLighthouse's Python SDK

Welcome to CodeLighthouse's official documentation for our Python SDK! If you're looking for guidance on how to 
install, configure, and/or integrate our SDK into your code, you're in the right place! 

## Installing the SDK
The CodeLighthouse SDK is published on [PyPi](https://pypi.org/project/CodeLighthouse/), the Python package index. 

### Installing with Pip
Installing the SDK with pip couldn't be easier! 
Simply run:

```bash
pip install codelighthouse
```

If you're using pip for dependency management, once you install CodeLighthouse, you can easily add it to your list of 
dependencies:
```bash
pip freeze > requirements.txt
```

## Configuring the SDK
Once you have installed the SDK, you need to import and configure it. Configuring the SDK requires signing up an 
account at [codelighthouse.io](https://codelighthouse.io). Using CodeLighthouse for a small or personal project? No 
worries, we offer a [free tier](https://codelighthouse.io/#pricing) subscription!

### SDK Configuration Options
The CodeLighthouse SDK has several configuration options that provide for current functionality and future 
extensibility. 
<!-- title: SDK Configuration Options -->
| Option                  | Value                                          | Required? |
|-------------------------|------------------------------------------------|-----------|
|`organization_name`      |The name of your organization when you signed up| yes       |
|`x_api_key`              |Your organization's API Key                     | yes       |
|`default_email`          |The default email for notifications to be sent to | yes     |
|`send_uncaught_exceptions` | A boolean value.  Tells the application whether or not to send uncaught exceptions to CodeLighthouse.  Default of `True` | no |
|`resource_name`          |The name of the resource you are embedding the SDK into| no|
|`resource_group`         |The group of resources that the resource you are embedding the SDK into belongs to| no |

#### Required Parameters
These options are required for your SDK to successfully authenticate to our server and to function properly.
* `organization_name`  - The name of your organization. After you sign up, this can be found in your 
[CodeLighthouse Admin Dashboard](https://codelighthouse.io/admin) on the 
[organization](https://codelighthouse.io/admin/organization) page. We recommend copying and pasting this value into the 
SDK to prevent typos.
* `x_api_key` - Your API key, registered when you sign up for your account. After you sign up, this can be found in 
your [CodeLighthouse Admin Dashboard](https://codelighthouse.io/admin) on the 
[organization](https://codelighthouse.io/admin/organization) page. We recommend copying and pasting this value into the 
SDK to prevent typos.

#### Optional Parameters
The following options are used for organizing your resources and their errors. The specified values for each will be 
included in your error notifications. When a function in a resource encounters an error, the code owner will be 
notified of the resource group, resource name, environment, and function name where the error ocurred. We anticipate 
being able to filter errors and visualizations on the basis of these options in the near future.

* `resource_name` - The name of the resource that your code belongs to. This is used for tracking errors when you are 
using CodeLighthouse in multiple different projects or resources. This value is included in the error notifications you 
receive so that you know where the error ocurred. We also anticipate allowing you to filter your error feed by resource 
name, as well as offering error analytics and visualizations on a per-resource basis in the near future. 
* `resource group` - the name of the group or resources that this resource belongs to. Similar to `resource_name`, this 
is used for tracking errorss, and is included in the error notifications you receive. We expect to be able to allow you 
to filter and visualize errors on a per-`resource_group` basis as well. 

### Configuration Example
```python
# IMPORT CODELIGHTHOUSE
from codelighthouse import CodeLighthouse
import os

# INSTANTIATE THE ERROR CATCHER
lighthouse = CodeLighthouse(
    organization_name="CodeLighthouse, LLC",
    x_api_key="your API Key",
    default_email="hello@codelighthouse.io",
    resource_group="serverless-applications",
    resource_name="notifications-app"
)
```

## Using the SDK
Once you have configured the SDK, it's super easy to use! Simply use the CodeLighthouse `error_catcher` decorator above 
functions that you want to get notifications for uncaught errors in. 

### Using the Error Catcher Decorator
Each decorator only applies to the one function defined directly below it. In the decorator, specify the email address 
of the user in your organization who should receive the notification. 

```python
@lighthouse.error_catcher(email="alice@codelighthouse.io")
def some_function():
  do_some_thing()
  print("Did something!")
```

<!-- theme: warning -->
### Decorators and Web Frameworks

Note that the CodeLighthouse decorator must be inside of decorators used for web framework routing (Flask, Pyramid). 
Alternatively, using `app.add_url_rule()` instead of the `@app.route()` decorator will work for Flask apps and 
blueprints.

### Sending Errors Manually

Throughout your application, you probably already have some code that is handling errors as they come in.  If you want 
CodeLighthouse to know about those, you can pass them by calling `lighthouse.error(exception)` and passing it the 
exception and optionally an email for a user in your organization as well.  This allows CodeLighthouse to continue to 
help your developers understand their code even if it isn't a mission critical situation.

```python
def some_function():
    try:
        call_a_broken_function()
    except NameError as e:
        lighthouse.error(e, email="bob@codelighthouse.io")
```

### Adding Additional Users
You can invite additional users to your organization in your admin panel on the 
[user management page](https://codelighthouse.io/admin/users). Note that each payment plan only comes with a fixed 
number of users, and that adding additional users past that number will cost more. Please refer to our 
[pricing guide](https://codelighthouse.io/#pricing) for more information.

## A Complete Example
CodeLighthouse's SDK is built with pure python and will work with any native python framework. The example below uses 
flask to illustrate a common application of our SDK. 

```python
# IMPORTS
from flask import Flask
from codelighthouse import CodeLighthouse
import os

# CONFIGURE THE SDK
lighthouse = CodeLighthouse(
    organization_name="CodeLighthouse, LLC",
    x_api_key=os.environ.get("CODELIGHTHOUSE_API_KEY"),
    resource_group="serverless-applications",
    resource_name="notifications-app"
)

# CREATE YOUR APP
app = Flask(__name__)

# ADD THE CODELIGHTHOUSE error_catcher DECORATOR TO FUNCTIONS
@app.route('/')
@lighthouse.error_catcher(email='alice@codelighthouse.io')
def say_hello():
    return "Hello, World! Real-time error notifications brought to you by CodeLighthouse"


@app.route('/<name>')
@lighthouse.error_catcher(email='bob@codelighthouse.io')
def hello_name(name):
    try:
        return f'Hello, {name}! '
    except NameError as e:
        lighthouse.error(e, email="alice@codelighthouse.io")
        return "This error was handled by CodeLighthouse"

app.run()
```
