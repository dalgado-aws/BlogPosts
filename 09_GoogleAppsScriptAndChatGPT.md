## ChatGPT Assisted Programming with Google Apps Script

### Why Google Scripts to Experiment with ChatGPT?

#### Any sprawling API is made accessible 

I have been using ChatGPT to generate shell/bash scripts snippets for a while now. 
And I find Bash/Shell programming to be ideally suited for automation with ChatGPT. 

It helps me get control over the vastness of bash/shell scripting.
Unlike Java or C, shell/bash is not a compact language.
It consists of a vast array utilities that can be creatively knitted together with pipes, loops, and other esoteric constructs.
Each utility is further gifted with a multitude of options. 

Other than the most frequently used commands and options, it is not always easy to remember the various commands and their abilities.

ChatGPT adept at remembering the arcane options for every command and then choosing just the right one for the task at hand.

```However,  it is not always feasible to develop a bash/shell application that can be easily developed and tested online.```

#### Easiness to get a non-trivial app up and running without any locally setup 

Unlike bash/shell scripting, the whole Google Apps Script ecosystem lives online.

[Google Apps Script API]( https://developers.google.com/apps-script) humongous public api that I always 
wanted to dabble in.  Previously, I had built a Gmail addon that currently sits in my inside my gmail.

As I built the addon as a side-project and learnt that it takes more than the estimated time to learn the intricacies of a vast 
api. StackOverflow definitely helps with quick-fixes but it will not expose the varied features and best practises of an API.

The time-investment required to master an API can be a barrier to getting started on side-projects.  

### An Online App for Personal Email Hygeine

Every few weeks I use [MailStrom](https://mailstrom.co/) to groom my gmail inbox. 
I try to keep my inbox clean, neat, and organized. 

Without grooming, important emails can get lost in the forest of newsletters, discount-sale offers, 
emails about online purchases (amazon, etc.) and social media alerts. 

We can use Google Apps Script to build a poor man's MailStrom. 

The Google Apps Script Web App will show us an aggregated view of a gmail inbox. Later on we can add features to the app
that allows us to setup rules to automatically delete some emails.

At first, we can build a simple screen tht shows us an aggregated view of the gmail inbox that looks like below.
We will see how a few prompts to ChatGPT can get our App up and running in no time.

| sender's email             | count of emails sent | click on link to view all these emails   |
|----------------------------|----------------------|------------------------------------------|
| john@gmail.com             | 26 emails from john  | link to all John's email                 |
| notifications@facebook.com | 15 emails from john  | link to all facebook notification emails |
| orders@amazon.com          | 7 emails from john   | link to all amazon orders email          |
| shipping@books.com         | 3 emails from john   | link to all books.com email              |


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
    
![](google_apps_script/new_web_app_deployment_1.jpg)

    - Click on gear box next to "Select type", and choose "Web App". Then Click on "Deploy"

![](google_apps_script/new_web_app_deployment_2.jpg)

    - Copy the URL

![](google_apps_script/new_web_app_deployment_3.jpg)

    - Open the URL in a browser

![](google_apps_script/open_app_on_browser.jpg)

### Adding Meat using ChatGPT

Now that we have a basic Web Application running, it is time to summon ChatGPT to 
conjure up the code to add functionality to the app.

Jump to https://chat.openai.com/ and login into the app using a Google account. 

Copy-paste the following request at the ChatGPT prompt as seen in the image below. 

```commandline
Create a google apps script function that counts the emails sent be each sender
in the last 3 months. Sort the list in descending order
```
![](google_apps_script/chatgpt_first_prompt.jpg)

ChatGPT has created the function that will generate the data we want.
Now we want to render the results of the function as HTML.

Since ChatGPT is a conversational chatbot, we can add to our initial request.
At the ChatGPT prompt, enter the following:

```commandline
Create a function that uses a HTML template to display the list
```

![](google_apps_script/chatgpt_second_prompt.jpg)

And just like that, ChatGPT will create a Google Apps script template to render the array from
the previous function. Every call to ChatGPT will generate a different solution. The code
generated for me is available  [here]()

It is amazing how ChatGPT got the context for our request. 
It "figured out" that we want a template that will work with Google Apps Script.
It also generated code to render the template using data generated by our function.

![](google_apps_script/chatgpt_second_prompt_b.jpg)

ChatGPT has created the meat of the function but we need to fit it in our framework.
We need some understanding of the working of a webapp to glue the whole thing together.

We will have to copy the javascript code to code.js
We also need to create a new file to contain the template 

It is important to note that every invocation of ChatGPT could render a completely
different code/response.

#### Deploy again 
Now we have to deploy the application again. The additional code we added uses objects like
`GMailApp` that need more access control. 
This time around we will have to go through more Authorization Screens since we are 
accessing the email information. Like before, once the deployment is done, we will get a URL
to access the app.

### Open the Deployment URL in the Browser
![](google_apps_script/open_new_app_on_browser.jpg)

We were able to build an app in a few minutes. Google Apps Script is a vast API that presents
enormous opportunities for Automation. As a first step, we could modify the template to
include links to open all the emails from a sender. A typical link would look like this:

https://mail.google.com/mail/u/0/#search/from%3AKAYAK+%3Cservice%40email.kayak.com%3E

#### Vast Possibilities to Explore

ChatGPT and other bots like it are enhancing the productivity of programmers. The time-costs to get started with 
an interesting side-project is vastly reduced.  

Now you can get started on the C# application for Windows that you were always postponing or the python big data applicaition


