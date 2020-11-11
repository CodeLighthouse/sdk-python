---
tags: [python, sdk]
---

# CodeLighthouse's Python SDK

Welcome to CodeLighthouse's official documentation for our Python SDK! If you're looking for guidance on how to install, configure, and/or integrate our SDK into your code, you're in the right place! 

## Installing the SDK
The CodeLighthouse SDK is published on [PyPi](https://pypi.org/project/CodeLighthouse/), the Python package index. 

### Installing with Pip
Installing the SDK with pip couldn't be easier! 
Simply run:

```bash
pip install codelighthouse
```

If you're using pip for dependency management, once you install CodeLighthouse, you can easily add it to your list of dependencies:
```bash
pip freeze > requirements.txt
```

## Configuring the SDK
Once you have installed the SDK, you need to import and configure it. Configuring the SDK requires signing up an account at [codelighthouse.io](https://codelighthouse.io). Using CodeLighthouse for a small or personal project? No worries, we offer a [free tier](https://codelighthouse.io/#pricing) subscription!

### SDK Configuration Options
The CodeLighthouse SDK has several configuration options that provide for current functionality and future extensibility. 
<!-- title: SDK Configuration Options -->
| Option                  | Value                                          | Required? |
|-------------------------|------------------------------------------------|-----------|
|`organization_name`      |The name of your organization when you signed up| yes       |
|`x_api_key`              |Your organization's API Key                     | yes       |
|`resource_name`          | The name of the resource you are embedding the SDK into| no|
|`resource_group`         |The group of resources that the resource you are embedding the SDK into belongs to| no |
|`github_repo`            | The github repository for this project to add issues to|no|

#### Mandatory Options
These options are required for your SDK to successfully authenticate to our server and to function properly.
* `organization_name`  - The name of your organization. After you sign up, this can be found in your [CodeLighthouse Admin Dashboard](https://codelighthouse.io/admin) on the [organization](https://codelighthouse.io/admin/organization) page. We recommend copying and pasting this value into the SDK to prevent typos.
* `x_api_key` - Your API key, registered when you sign up for your account. After you sign up, this can be found in your [CodeLighthouse Admin Dashboard](https://codelighthouse.io/admin) on the [organization](https://codelighthouse.io/admin/organization) page. We recommend copying and pasting this value into the SDK to prevent typos.

#### Optional Options
The following options are used for organizing your resources and their errors. The specified values for each will be included in your error notifications. When a function in a resource encounters an error, the code owner will be notified of the resource group, resource name, environment, and function name where the error ocurred. We anticipate being able to filter errors and visualizations on the basis of these options in the near future.

* `resource_name` - The name of the resource that your code belongs to. This is used for tracking errors when you are using CodeLighthouse in multiple different projects or resources. This value is included in the error notifications you receive so that you know where the error ocurred. We also anticipate allowing you to filter your error feed by resource name, as well as offering error analytics and visualizations on a per-resource basis in the near future. 
* `resource group` - the name of the group or resources that this resource belongs to. Similar to `resource_name`, this is used for tracking errorss, and is included in the error notifications you receive. We expect to be able to allow you to filter and visualize errors on a per-`resource_group` basis as well. 

The following options allow you to configure other information about the resource that you are embedding the SDK in.
* `github_repo` - This value allows you to specify the name of the GitHub repository that this code belongs to. When new types of errors occur, the SDK will automatically create issues in your repository. For this to work, you must configure your organization's GitHub integration in your CodeLighthouse Administrator Dashboard's [organization](https://codelighthouse.io/admin/organization) page. 

### Configuration Example
```python
# IMPORT CODELIGHTHOUSE
from codelighthouse.CodeLighthouse import CodeLighthouse
import os

# INSTANTIATE THE ERROR CATCHER
lighthouse = CodeLighthouse(
    organization_name="CodeLighthouse, LLC",
    x_api_key="your API Key",
    resource_group="serverless-applications",
    resource_name="notifications-app",
    github_repo="notifications_app"
)
```

## Using the SDK
Once you have configured the SDK, it's super easy to use! Simply use the CodeLighthouse `error_catcher` decorator above functions that you want to get notifications for uncaught errors in. 

### Using the Error Catcher Decorator
Each decorator only applies to the one function defined directly below it. In the decorator, specify the email address of the user in your organization who should receive the notification. 

```python
@lighthouse.error_catcher(email="example@codelighthouse.io")
def some_function():
  do_some_thing()
  print("Did something!")
```

### Adding Additional Users
You can invite additional users to your organization in your admin panel on the [user management page](https://codelighthouse.io/admin/users). Note that each payment plan only comes with a fixed number of users, and that adding additional users past that number will cost more. Please refer to our [pricing guide](https://codelighthouse.io/#pricing) for more information.

## A Complete Example
CodeLighthouse's SDK is built with pure python and will work with any native python framework. The example below uses flask to illustrate a common application of our SDK. 

```python
# IMPORTS
import os
from flask import Flask
from codelighthouse.CodeLighthouse import CodeLighthouse
import os

# CONFIGURE THE SDK
lighthouse = CodeLighthouse(
    organization_name="CodeLighthouse, LLC",
    x_api_key=os.environ.get("CODELIGHTHOUSE_API_KEY"),
    resource_group="serverless-applications",
    resource_name="notifications-app",
    github_repo="notifications_app"
)

# CREATE YOUR APP
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# ADD THE CODELIGHTHOUSE error_catcher DECORATOR TO FUNCTIONS
@lighthouse.error_catcher(email='user1@codelighthouse.io')
@app.route('/')
def say_hello():
    return "Hello, World! Real-time error notifications brought to you by CodeLighthouse"

@lighthouse.error_catcher(email='user2@codelighthouse.io')
@app.route('/<name>')
def hello_name(name):
    return f'Hello, {name}! '

app.run()
```
