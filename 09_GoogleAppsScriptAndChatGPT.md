## ChatGPT Assisted Programming with Google Apps Script

### Why Google Scripts to Experiment with ChatGPT?

ChatGPT can be used to improve programmer efficiency in almost any programming language. There are few reasons why I decided
to use ChatGPT with Google Apps Script:

#### Any sprawling API is made accessible 

I have been using ChatGPT to generate shell/bash scripts snippets for a while now. 
And I find Bash/Shell programming to be ideally suited for automation with ChatGPT. 

It helps me get control over the vastness of bash/shell scripting.
Unlike Java or C, shell/bash is not a compact language.
It consists of a vast array utilities that can be creatively knitted together with pipes, loops, and other esoteric constructs.
Each utility is further gifted with a multitude of options. 

In case of bash/shell scripting, it is not always easy to remember the various commands and their abilities.
Developers tend to "muscle-memorize" the most frequently used commands and options.

ChatGPT, however, is adept at remembering the arcane options for every command and then choosing just the right one for the task at hand.

 ```As much as I would have liked to build a shell/bash application with ChatGPT,  it is not always feasible to develop a bash/shell application that can be easily developed and tested online.```

#### Easiness to get a non-trivial app up and running without any local setup 

Like bash/shell, Google Apps Script has an expansive api that takes time and effort to master.
```Unlike bash/shell scripting however, the whole Google Apps Script ecosystem lives online.```

[Google Apps Script API]( https://developers.google.com/apps-script) is a humongous public api that I have used to many personal projects. 
I built a Gmail add-on that currently sits in my inside my gmail.

It usually takes more than the estimated time to learn the intricacies of a vast api. 
StackOverflow definitely helps with quick-fixes but does not expose the varied features and best practises of an API.

With ChatGTP at on our side, we can set sail to explore any API that intrigues us, even within the constraint of 
limited time investment that holds back our personal/side projects.

### An Online App for Personal Email Hygeine

Every few weeks I use [MailStrom](https://mailstrom.co/) to groom and prune my gmail inbox. 
I try to keep my inbox clean, neat, and organized. 

Without grooming, important emails can get lost in the forest of newsletters, discount-sale offers, 
emails about online purchases (amazon, etc.) and social media alerts. 

We can use Google Apps Script to build a poor man's MailStrom. 

Our Google Apps Script Web App will show us an aggregated view of a gmail inbox. Later on we can add features to the app
that allows us to set up rules to automatically delete some emails.

At first, we can build a simple screen tht shows us an aggregated view of the gmail inbox that looks like below.
We will see how a few prompts to ChatGPT can get our App up and running in no time.

| sender's email             | count of emails sent    | click on link to view all these emails   |
|----------------------------|-------------------------|------------------------------------------|
| john@gmail.com             | 26 emails from john     | link to all John's email                 |
| notifications@facebook.com | 15 emails from facebook | link to all facebook notification emails |
| orders@amazon.com          | 7 emails from amazon    | link to all amazon orders email          |
| shipping@books.com         | 3 emails from books.com | link to all books.com email              |


### Getting Started: The Scaffolding To Deploy A Simple Web App

It is very easy and convenient to get started with Google Apps Script. 
All you need is a google/gmail account. 

##### 1. Open [scripts.google.com](scripts.google.com) and click on + New Project

 The app will create a new project with the code.js file open for editing

#### 2. Delete all existing content in code.js and enter the following function

```javaScript
function doGet() {
  return HtmlService.createHtmlOutput("<b>hello</b>");
}
```
#### 3. Deploy the app
    - Click on "Deploy" -> "New Deployments"
    
![](https://github.com/dalgado-aws/BlogPosts/blob/master/google_apps_script/img/new_web_app_deployment_1.jpg)

    - Click on gear box next to "Select type", and choose "Web App". Then Click on "Deploy"

![](https://github.com/dalgado-aws/BlogPosts/blob/master/google_apps_script/img/new_web_app_deployment_2.jpg)

    - Copy the URL

![](https://github.com/dalgado-aws/BlogPosts/blob/master/google_apps_script/img/new_web_app_deployment_3.jpg)

    - Open the URL in a browser

![](https://github.com/dalgado-aws/BlogPosts/blob/master/google_apps_script/img/open_app_on_browser.jpg)

### Adding Functionality using ChatGPT

Now that we have a basic Web Application running, it is time to summon ChatGPT to 
conjure up the code to add functionality to the app.

Jump to https://chat.openai.com/ and login into the app using a Google account. 

Copy-paste the following request at the ChatGPT prompt as seen in the image below. 

```commandline
Create a google apps script function that counts the emails sent by each sender
in the last 3 months. Sort the list in descending order
```
![](https://github.com/dalgado-aws/BlogPosts/blob/master/google_apps_script/img/chatgpt_first_prompt.jpg)

ChatGPT has created the function that will generate the data we want.
Now we want to render the results of the function as HTML.

Since ChatGPT is a conversational chatbot, we can add to our initial request.
At the ChatGPT prompt, enter the following:

```commandline
Create a function that uses a HTML template to display the list
```

![](https://github.com/dalgado-aws/BlogPosts/blob/master/google_apps_script/img/chatgpt_second_prompt.jpg)

And just like that, ChatGPT will create a Google Apps script template to render the array from
the previous function. Every call to ChatGPT will generate a different solution. The code
generated for me is available  [here]()

It is amazing how ChatGPT got the context for our request. 
It "figured out" that we want a template that will work with Google Apps Script.
It also generated code to render the template using data generated by our function.

![](https://github.com/dalgado-aws/BlogPosts/blob/master/google_apps_script/img/chatgpt_second_prompt_b.jpg)

ChatGPT has created the meat of the function, but we need to fit it in our framework.
We need some understanding of the working of a webapp to glue the whole thing together.

We will have to copy the javascript code to code.js
We also need to create a new file to contain the template 

All the glue code and ChatGPT responses that I copy-pasted are available here: https://github.com/dalgado-aws/BlogPosts/tree/master/google_apps_script

```It is important to note that every invocation of ChatGPT could render a completely different code/response.```

#### Deploy again 
Now we have to deploy the application again. The additional code we added uses objects like
`GMailApp` that need more access control. 
This time around we will have to go through more Authorization Screens since we are 
accessing the email information. Like before, once the deployment is done, we will get a URL
to access the app.

### Open the Deployment URL in the Browser
![](https://github.com/dalgado-aws/BlogPosts/blob/master/google_apps_script/img/open_new_app_on_browser.jpg)

We were able to build an app in a few minutes. Google Apps Script is a vast API that presents
enormous opportunities for Automation. As a first step, we could modify the template to
include links to open all the emails from a sender. A typical link would look like this:

https://mail.google.com/mail/u/0/#search/from%3AKAYAK+%3Cservice%40email.kayak.com%3E

#### Vast Possibilities to Explore

ChatGPT and other bots like it are enhancing the programmer-productivity. The time-costs to get started with 
an interesting side-project is vastly reduced. 

Developers can use ChatGPT to increase their productivity manifold even for plain old Java programming. 
Security Sensitive organizations however restrict access to these new supertools. They will have to make adjustments
as the cost-benefits become apparent.

Now you can get started on the C# application for Windows that you were always postponing or the python big data applicaition


