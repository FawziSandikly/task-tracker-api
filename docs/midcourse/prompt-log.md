Prompt Log 
 

Project 
Task Tracker REST API 
 
This document records the prompts used during the development of the mid-course features and explains how AI assisted throughout the implementation. 
 
--- 
 

Feature: Due Dates 
 

Prompt 1 
 

Goal 
Add due dates to tasks. 
 

Prompt 
Design a FastAPI implementation that adds an optional §§BLOCK*0§§ field to a Task Tracker API built with SQLModel. Include validation and explain how overdue tasks should be determined. 
 

Outcome 
The response explained how to: 

Add a §§BLOCK*1§§ field to the SQLModel model. 
Update request and response schemas. 
Store due dates in SQLite. 
Compare the due date with the current date to determine whether a task is overdue. 
 
The generated code was reviewed and adapted before being integrated. 
 
--- 
 

Prompt 2 
 

Goal 
Validate due dates. 
 

Prompt 
How can I validate that a due date is in ISO 8601 format and reject invalid values in a FastAPI application using Pydantic? 
 

Outcome 
The response demonstrated how FastAPI automatically validates date fields using Pydantic and returns HTTP 422 for invalid input. The validation strategy was incorporated into the API. 
 
--- 
 

Prompt 3 
 

Goal 
Return overdue information. 
 

Prompt 
Show how to include an is_overdue property in FastAPI responses without storing it in the database. The value should be calculated dynamically from the task's due date. 
 

Outcome 
The response suggested computing the property at runtime instead of storing redundant data. This approach simplified the database model while providing useful information to API clients. 
 
--- 
 

Feature: Tags 
 

Prompt 4 
 

Goal 
Store multiple tags for each task. 
 

Prompt 
Show how to add tags to a Task Tracker API so each task can store multiple tags and return them in API responses. 
 

Outcome 
The response explained how to: 

Store multiple tags. 
Update request and response models. 
Return tags in API responses. 
Support updating tags. 
 
The generated solution required minor modifications before integration. 
 
--- 
 

Prompt 5 
 

Goal 
Validate tags. 
 

Prompt 
How can I validate task tags in FastAPI so duplicate tags are removed, whitespace is trimmed, and empty tags are rejected? 
 

Outcome 
The response demonstrated several validation techniques using Pydantic validators. The implementation was adapted to keep tag data clean and consistent. 
 
--- 
 

Prompt 6 
 

Goal 
Filter tasks by tag. 
 

Prompt 
Design a FastAPI endpoint that returns all tasks containing a specified tag. Include an example implementation using SQLModel. 
 

Outcome 
The response described different filtering approaches and example query logic. The ideas were adapted to match the project's existing API structure. 
 
--- 
 

Testing 
 

Prompt 7 
 

Goal 
Improve automated testing. 
 

Prompt 
Write pytest tests for a FastAPI Task Tracker API including CRUD operations, due dates, tags, and invalid input handling. 
 

Outcome 
The response generated example unit tests that were modified to match the project structure before being committed. 
 
--- 
 

Debugging 
 

Prompt 8 
 

Goal 
Debug API validation. 
 

Prompt 
Why does my FastAPI endpoint return HTTP 422 instead of HTTP 200 when updating a task? 
 

Outcome 
The explanation helped identify validation issues, incorrect request bodies, and schema mismatches, improving endpoint reliability. 
 
--- 
 

Documentation 
 

Prompt 9 
 

Goal 
Improve project documentation. 
 

Prompt 
Generate documentation explaining the new features, API endpoints, and testing strategy. 
 

Outcome 
The generated documentation was used as a starting point for updating the README and project reports. 
 
--- 
 

Weak Prompt → Strong Prompt Example 
 

Weak Prompt 
Add tags. 
 

Why it was weak 
The prompt did not specify the framework, data model, storage method, or expected API behavior. This resulted in a generic response that required significant modification. 
 

Strong Prompt 
Show how to implement multiple tags for each task in a FastAPI Task Tracker API using SQLModel. Include changes to the database model, request and response schemas, CRUD operations, validation, and example JSON requests and responses. 
 

Improvement 
Providing project-specific details produced a much more complete and relevant solution that required only minor adjustments before integration. 
 
--- 
 

Reflection on AI Usage 
 
AI significantly reduced development time by explaining concepts, generating implementation examples, suggesting validation strategies, producing test cases, and helping debug issues. Rather than copying generated code directly, every response was reviewed, tested, and adapted to fit the project's architecture and coding standards. 
 
The most effective prompts were those that clearly specified the framework (FastAPI), ORM (SQLModel), desired feature, validation requirements, and expected API behavior. More detailed prompts consistently produced more accurate and useful responses
