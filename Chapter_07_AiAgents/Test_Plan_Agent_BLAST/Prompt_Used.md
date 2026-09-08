### prompt to create a BLAST framework 

Use only the folder @file:chapter_07_AI_Agents 

Let's use the BLAST.md file, and let's go with protocol 0, which is the first step. Our main objective is to create a test plan creator from a Jira ID.

What we need to do is create the following files:

- task_plan findings.md
- progress.md
- LLM.md

In these files, you need to mention all the details:

- How your thinking is
- What you have thought about it
- How exactly we can create this project in this case

I want you to create these files and add the following:

- In findings.md, mention the findings that you have found and how we can fetch them from Jira, and include any curl or request that you will be using.
- In progress.md, add everything you are making every hour, every 30 minutes, or every 10 minutes: what was done, what the error was, what the results were, and everything.
- In task_plan, mention all the checklists and the goals that we have for it.
- In LLM.md, mention what you think about the schemas, rules, and architecture while creating this project.



----

### prompt to crete a UI to generate Test plan 

 So lets do phase one , phase 2 , phase 3 , phase 4 everything in one go. My North start or my objective is very clear and simple.
  You will create a very simple UI where in the UI, first UI will be where user will give you a prompt like fetch this jira and
  create a test plan. your task will be that  you need to fetch the Jira automatically and create a test plan for it automatically
  in this case. LLM connection that we will be using is GROQ mentioned in @.env inside the @Chapter_07_AiAgents , and you can uae a
  model OpenAI GPT-120 billian parameter for this . My objective is very simple . you also have to create a setting phase . In the
  setting you will allow user to add a setting of JIRA , which is JIRA API, email id and their token , as well as you will allow the
   test connections of JIRA  as well as GROQ also. They will also add a key of GROQ also side by side with it . Please make sure
  whatever the step that you are doing , you update all the files of finding progress and test plan also side by side , follow BLAST
   framework properly and complete the project and run the project locally now.