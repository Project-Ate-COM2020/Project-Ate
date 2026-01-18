**What I have done since Thursday - to prepare for Tuesday**
I have set up our system stack with the small change of MySQL -> SQLite in this github

I used vite for the react server, and included a few react dependecies (react-dom, react-router-dom, axios, tailwindcss) to make most of the full frontend framework

Django is it's own full framework, I have only installed the Django-rest-framework to make building it as an API much easier

I have not started any Django apps yet, so the directory is mostly empty, after the meeting I think it would be would be a good starting point for everyone to use django to start an app - we only need 5 tho

I have written a bunch of installation guides, copied project info into here and started an example directory layout for the backend, I think this will help everyone understand what exactly they need to code

The main thing to do is have another look over the project brief - I only looked once and it looks like quite a lot of the project focuses on things outside of coding, so starting that early as well I think will be a good idea
I think that's everything

Personal design decisions that need to be discussed and can be changed:

we decided on React-Django-MySQL in meeting 1 - I have changed MySQL to SQLite as it's built in, 
however for integration testing and to make sure everyone knows what test data could be, we could switch to the mySQL server option.

I have also implemented the React-Django setup as a fully fledged external webserver - internal API model, the alternative would be to use 
DjangoDB as the whole stack and get rid of React - this however I think would make it much harder to differentiate coding responsibilities
and it would be harder to keep track of work as well as meaning we lose all the benefit of functional JS and Tailwind CSS.

I also binned off the suggested group roles - I think it is crucial that we each have a very objective and defined coding task that is somewhat self
contained, that way we don't have to deal with mixups. This means I have made team and development roles - these are not finished and there are a few changes
I would make, can be done on tuesday. However the whole thing is entirely subjective and we can decide to do something else entirely, like the
suggested group roles on ele.

I used functional javascript rather than functional typescript for react - we could change this but I thought most people would probably be more 
comfortable with javascript despite the development benefits of static type checking.

I have already assumed the decomposed features which are pretty clearly defined in the project spec:
(I have assumed we will not work on profiles just yet as it's quite an involved feature that's not required for the prototype at all)
(We would have to obviously make one test authentication method for the live demo - but we can just give it access to the whole website to show how it works)

Prototype:
- Marketplace
- analytics
- Forecasting
- Gameification 

Client handover:
- Profile creation, logins, authentication

Of course these decompositions can also be changed - however I do not think this design choice is very subjective

