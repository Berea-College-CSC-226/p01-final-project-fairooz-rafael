# CSC226 Final Project

**Author(s)**: Fairooz, Rafael

️**Google Doc Link**: https://docs.google.com/document/d/1TBcWua-ldKdQVddmQOZm22J62i7bgtcS_1MXITquLJs/edit?usp=sharing

---

## Milestone 1: Setup, Planning, Design

️**Title**: `Super system for inventory - Amigazon`

**Purpose**: `Help a company keep track of their products and implement an effective expenses sheet`

**Source Assignment(s)**: `Used inspiration from homework 7 and 9, for reading data from a file and using upc in real life application`

️**CRC Card(s)**:
  

️**Products class**:

 ![product class CRC.png](image/product%20class%20CRC.png "clase inventario")

️**upc class**:

![UPC class CRC.png](image/UPC%20class%20CRC.png "UPC")

️**inventory class**:

![inventory class CRC.png](image/inventory%20class%20CRC.png "xyz")


**Branches**: This project will **require** effective use of git. 

Each partner should create a branch at the beginning of the project, and stay on this branch (or branches of their 
branch) as they work. When you need to bring each others branches together, do so by merging each other's branches 
into your own, following the process we've discussed in previous assignments, then re-branching out from the merged code.  

```
    Branch 1 starting name: rafael
    Branch 2 starting name: fairooz_newApproach
```

### References 

```
    UPC barcodes Homework 9 - we reused the logic behind the upc code making it adaptable
    It's in your genes Homework 8 (didn't use code, just logic)
    Oh the places that you will go Homework 7 - used to read text files and load data from a text file
    Tkinter library - used to build our graphic interface
    Listbox, and Scrollbar documentation - used on widgets for the interface
    ChatGPT - used in debugging and merging of versions of code
```

---

## Milestone 2: Code Setup and Issue Queue

Most importantly, keep your issue queue up to date, and focus on your code. 🙃

Reflect on what you’ve done so far. How’s it going? Are you feeling behind/ahead? What are you worried about? 
What has surprised you so far? Describe your general feelings. Be honest with yourself; this section is for you, not me.

```
   We created all the class we needed till now as for the program except GUI part. The program should function to read 
   product data and show summary to both customer and company and it should work for purchase and update. Additionally,
   we worked on GUI for customer interface where they can see the inventory list and add to cart or purchase products.
   
   I think we're in track, not behind not ahead. I think the way functionality works suprised us the most. Due to hw11, 
   when we broke down our program into subtask we figured it out how we could work with a few classes than we thought initially.
   
   We're excited to complete our program and see how it comes out. Maybe works with more advancement in future if it 
   goes according to our preference
```

---

## Milestone 3: Virtual Check-In

Indicate what percentage of the project you have left to complete and how confident you feel. 

️**Completion Percentage**: `75%`

️**Confidence**: Describe how confident you feel about completing this project, and why. Then, describe some 
  strategies you can employ to increase the likelihood that you'll be successful in completing this project 
  before the deadline.

```
   We are pretty confident that we'll be able to complete it on time. At this point, we've all the class and methods working, we only need refinement and testing; also some improvement for GUI.
   To make it successful we will be creating issues as our checklist and even create the extra ideas as optional, if we have time, we will complete those after our main completion. 
```

---

## Milestone 4: Final Code, Presentation, Demo

### User Instructions

In a paragraph, explain how to use your program. Assume the user is starting just after they hit the "Run" button 
in PyCharm. 

After running the program in PyCharm, a window will open saying it's a Company inventory App with option of user type: Customer or Company.
Then in the next slide,
if you select "Customer" : You can see a list of products, add products to your cart, check your cart, change quantities, and make a purchase.
if you select "Company" : Log in with username "admin" and password "1234" to see the company dashboard. You can view the inventory, check total earnings, and see a pie chart of expenses & revenue. Also, you can create new products that will be updated in both interfaces.
And you can use the buttons on each screen to move between pages.

### Errors and Constraints

Every program has bugs or features that had to be scrapped for time. These bugs should be tracked in the issue queue. 
You should already have a few items in here from the prior weeks. Create a new issue for any undocumented errors and 
deficiencies that remain in your code. Bugs found that aren't acknowledged in the queue will be penalized.

### Reflection
Each partner should write three to four well-written paragraphs address the following (at a minimum):

- Why did you select the project that you did?
- How closely did your final project reflect your initial design?
- What did you learn from this process?
- What was the hardest part of the final project?
- What would you do differently next time, knowing what you know now?
- How well did you work with your partner? What made it go well? What made it challenging?

```
    Partner 1: I would say I had fun in all the duration of this project. A day before the presentation we met with Fairooz to make the final refinements on it, and we saw that the project indeed came alive with the exception of a more practical and appealing design. The initial idea we had was just selling objects and along the way we thought of more features like login or adding new products to an inventory. 
I’d say our main idea and guide stayed the same, however when we worked deeper on the project and started using multiple classes at the same time, we changed the design and functionality from our initial expectations, which turned out well because the project works.
Some of the challenges were merging without a doubt, because we first divided functionality thinking that the “upc” class had a lot of relevance until we saw that we were using it on a wrong way. So from there, we had different codes and those differences continued to grow in the coming weeks, the last week being the most difficult to debug and merge in terms of functionality. For the ending, Fairooz and me divided the graphical interface from the functioning of the classes, and bringing those together without affecting the others was a difficult process. Plus, as I’ve also mentioned on my evaluation, I didn’t really catch up much with Graphic interface, so it made it harder. 
At the end, with this experience I would definitely change our planning and the way we communicate about functionality of a program. Neither of us did much documentation in the first weeks and that also took a bit of time to understand. So, for a future project I’d work harder on the initial planning and foundation, and besides that I’d try to be more prepared and aligned with the code that we require to execute our ideas.
Finally, working with Fairooz was a good experience. We were very understandable and flexible when needed, also she took on a lot of the debugging and merging; we also met multiple times and that facilitated understanding each other, to the point where we did driver navigator work too. The only challenges I experienced were meeting deadlines and that the first weeks she was not really updating and merging her branches properly. 
```

```
    Partner 2: We selected this project to test ourselves in an area we hadn’t seen in class. Our initial design looks very similar to the final result, but we changed from the logic of how getting there a lot. For example, we thought of the classes and then changed their form.
For our final project, we selected this one because I feel it is something useful and also interesting to learn. At first I think it will be simple, like only showing products and letting people buy. But when we start working more, I see that it can be more than that. The final project is close to our first design, but also different in good ways.
I learned many things, especially how classes connect and how reading files and GUI work together. 
The hardest part was understanding Rafael’s pace, because he was planning ahead too much and that confused me sometimes. Also, at some point I didn’t understood what was different from our codes. We worked separately for long time, so when we tried to combine everything, many errors appeared. In the last week we had many issues with merging.
If I could do it again, I would plan more from the start and write more notes, so both of us stay on the same track. Also, time planning would be important.
Working with my partner was good. Rafael is experienced coder and helped me a lot to understand how he thought of the problems to solve. I like how we distributed the work. The challenge was merging and keeping our work updated, but overall, we communicated well and solved most of the problems.

```

---