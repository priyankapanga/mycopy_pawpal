# PawPal+ Project Reflection

## 1. System Design

The streamlit app should be able to allow the user to at least add their activity, pet, and see their schedule for the day.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Answer:
My intitial design was:
Classes:
Owner: Attributes are name, preferences. A function can be checkavailability() that can be caused while scheduling. Another attribute is their schedule.
Pet: Attributes are pet name, age
Activity: Attributes are the name of the specific activity, as well as the time it needs.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes it changed quite a lot! Once I started considering how information actually moves between one component to the other (from the user to the pet to the task to the schedule), I realised schedule has to manage everything. Also, I had only used duration before but I realised some tasks have fixed timings and some dont, like a bath or a specific appointment time, and the app should try to accomodate both. I added many methods and attributes similar to this like sorting, filtering,and marking as complete. Now, there's a clearer flow between each.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The constraints considered by the scheduler is specific start time(if provided), duration(to avoid conflicts if we know starting time), and priority. I decided priority mattered the most, and those with a specific appointment time.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The program detects conflicts but doesn't block them. I think this is alright because the owner can choose what to do next. Also, conflict checks only happen when a task has a start and fixed duration. This is okay for now because the ones without can technically be scheduled any time within the day/week or time depending on the task's description chosen.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used it(Copilot) to check if my design was a good starting point, but I felt like it got too complicated, so I started working on the logic, then came back to fix the design. I also used Claude Code to help write pytests. The most helpful questions were- what logic doesn't make sense? What blindspots does this logic have.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One time, I asked for help in making sure that tasks were arranged by priority. I almost accepted the solution, but I saw that it doing it separately for each pet, meaning that even when only sorting by priority, it will put a lower priority of pet A over a high priority of pet B. So, I took some time to point where it could do and carefuly read. Another time was when I wanted to add a new feature, sorting by duration. It suggested a fix that added that button, but when I read the suggestion, it was going to also remove the starting time attribute. So I made sure that I was careful with it.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested if all my features like sorting, filtering worked. I checked if my scheduler was comparing tasks across pets of the same user, not jsut within the same pet's schedule. This was important because the owner is still one person and has one schedule to work with. I also tested if the conflict detector was working so that copies weren't made, and if a new task was made if it was "daily" and marked as completed.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

4-4.5 stars
I would want to test the schedule prioritization more, and think about what it will pick between two competing tasks: depending on which priority, time, duration.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  I really liked that we started with design and ended up with UI. I think I liked seeing the working table and being able to mark tasks as completed.
  **b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  I would want to make the scheduler "smarter" to schedule tasks before, after, or in between tasks dynamically.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  One important thing I learned is that I don't have to "perfect" my system design right at the beginning, but can make careful and organised changes to it. I also learned that to make better system designs, we have to think about the way information flows from one to the other. And if we have an app or something a user interacts with, we can map out everything they do and make sure it leads to an action in the logic in our system design!

This was a really nice project that I learned a lot from. Thank you!!
