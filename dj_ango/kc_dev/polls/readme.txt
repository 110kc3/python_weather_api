Question “index” page – displays the latest few questions.
Question “detail” page – displays a question text, with no results but with a form to vote.
Question “results” page – displays results for a particular question.
Vote action – handles voting for a particular choice in a particular question.
In Django, web pages and other content are delivered by views. Each view is represented by a Python function (or method, in the case of class-based views). Django will choose a view by examining the URL that’s requested (to be precise, the part of the URL after the domain name).

Now in your time on the web you may have come across such beauties as ME2/Sites/di