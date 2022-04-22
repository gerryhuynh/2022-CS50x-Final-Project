_This was my final project for the 2022 CS50x course. This project is now archived._

---

# GL Blog

**TL;DR:** A full-stack blog site that uses many of the tools learned from CS50.

## Intention
I created a blog site that uses many of the tools learned from CS50. I didn't want to stray too far beyond CS50 because I wanted my final project to be a culmination of what I learned from the course and a test to show the results of what I learned. It's okay to expand a bit from the teachings, but I want the general idea and tools from CS50 to be at the core.

I considered a program with a command-line interface using mostly C or Python, but I wanted to involve as many CS50 tools as possible. Therefore, I went with a full-stack website, with a front-end, back-end, and database.

**Tools used:**
- Flask framework - Python and Jinja2
  - Message flashing
  - Regular expression (Regex)
  - Sessions
  - Password hashing
  - Back-end error checking/validation
- SQLite (database)
  - JOIN table
  - Indexes
- HTML/CSS/Javascript
  - Bootstrap (CSS)
  - Front-end error checking/validation

# Features

**The main features of this blog site are:**
- [Registration and Login system](#registration-and-login-system)
  - Register
  - Login
  - Change account settings
  - Delete account
- [Blog posts](#blog-posts)
  - Make posts
  - Display posts
  - View individual posts
- [Smooth experience](#smooth-experience)
  - Front-end error checking/validation (live where possible/safe)
  - Back-end error checking/validation
  - Responsive based on dimensions of display

## Registration and Login system
The user is able to register a new account and login.

### **Register**
Registration only asks for 3 fields: name, email, password. I decided that these were the fundamental pieces of information I would need from a user:
- **Name:** identify the user
- **Email:** a unique email for login
- **Password:** login

When the user is registering, there is live validation and back-end validation as a backup (e.g. Inspect Element or JavaScript disabled).

This is done with a combination of Bootstrap validation, JavaScript, Python (Flask).

**Email**

Front-end (Bootstrap + JavaScript)
- Live validation
- Checks for empty fields for required fields
- Checks for a relatively valid format with regular expression
- Changing colors for valid (green) or invalid (red)

Back-end (Python/Flask + SQLite)
- Checks for empty fields for required fields
- Checks for a relatively valid format with regular expression
- Checks if an account exists for the email entered by comparing with database
- Flashes a relevant message
- Redirects to login page if successful registration

**Password**

Similar to email, but also checks to see if the two password matches on both the front-end with JavaScript and back-end.

Password field also displays what the password requirements are and checks for this with a regular expression.

The password is hashed with Werkzeug (similar to CS50 2022 problem set 9) for security.

### **Login**

Login system similarly has front-end live and back-end checks.

Front-end checks for valid email format and an input for password. It does not check for password. I decided to do this to allow a (malicious) user to enter a wrong password.

Back-end checks database to see if the email and password inputted matches.

Relevant error messages are displayed.

Upon login, some of the user's information is stored in the session/cookies, but not the password. I decided that storing the password, even if hashed, is a security risk.

### **Change Account Settings**

I wanted to offer the user the ability to change their account settings. The ability to change your name/email/password is common and a functionality that is useful in case the user wants to change any of these 3 aspects. (e.g. change online name, different email, a stronger password, etc.)

Name is easy to change; it is just a form submission and an update to the database and session information.

Updating email and password requires the user to confirm their password which is checked with the database.

Updating password, similar to registration, required the user to confirm their new password in addition to entering a new password.

### **Delete Account**

I wanted to offer the user the ability to delete their account in case the user no longer wants to keep their account. This is also useful for me when testing, so I can create and delete multiple accounts on the website as well.

Features
- Confirm if the user wants to delete account
  - Used modal component from Bootstrap
- The delete page can only be accessed from the change account page
- User is required to confirm both their email and password (similar to login)

## **Blog posts**

**Make new post**

Features
- Only logged in users would be able to make a new post.
- New post button on the top right corner on the navbar for easy access
- Post includes a title, an optional TL;DR (summary) section, and the content
- Title is limited to 255 characters
  - Check is done on the front-end with HTML and back-end with Python and in the SQLite database.
  - There is also basic validation similar to register/login system with Bootstrap
- Redirected to index page to view posts as an indication that the post was made
- New lines in post content are stored as is

**Display posts**

Features
- Viewable by everyone, logged in or not
- When there are no posts, the user is encouraged to make a new post
- When not logged in, the user is encouraged to register/login to start posting
- Displays title, TL;DR if there is one, author name and date created
- Posts are spaced out with a minimum height and a horizontal bar
- Wordwrapping is implemented in case the title or TL;DR is very long
- Stretched link from Bootstrap along with hover color for the row division is used for easy access to post with indication
- Sorted by newest at the top and oldest at the bottom

**View individual posts**

Features
- Displays title, TL;DR if there is one, author name, date and content
- In the back-end, new line in post content are processed with ```<br />``` Markup so that they can be properly displayed on the actual webpage

## **Smooth experience**

**Front-end error checking/validation**

Features
- Live error checking/validation for form submissions with JavaScript where possible
  - But not for sensitive information such as login or password in general; mostly for empty fields and valid general input
- JavaScript stored in separate .js file for scaleability

**Back-end error checking/validation**

Features
- Error checks/validation for form submissions
- Checks with database for valid submission
- Message flashing for errors (or success)
- Going to a page/route that does not exist (i.e. error 404) leads back to the home page
- Trying to go to a post that does not exist leads back to the home page
- Login required pages (similar to problem set 9)

**Responsive based on dimensions of display**

Features
- Based on Bootstrap (CSS) grid system and breakpoints

## **Features that can be added in the future**
- Better design
- Display table/list of user's own posts
- Delete posts
  - Directly from post
  - From list of user's own posts
- Editing posts — only user that made the post can edit
- Create draft — ability to save and edit post again later without posting
- Preview post
- Link to similar post when trying to create a new post with similar title for existing post
- Display first few lines of post in index page if no summary available
- Comments
  - Make, edit, delete
  - Number of comments
- Display a certain number of posts on page only with pagination feature
  - Ability to change number of posts to display on page
- Search posts
- Sort posts in different ways
- Add tags to posts
  - Filter by tags
- Hide/archive posts
- Display views for user
- Option to upvote(/downvote) posts
- Text editing features — e.g. bold, links, etc.
- Add images to posts
- Deactivate account instead of delete account
- Admin access level
    - Moderate/delete other users’ accounts
    - Moderate/delete ANY posts (/comments)
- See age of account
- Change password can’t be most recent/previous password

# Conclusion

I learned a lot from CS50, and I'm glad that I was able to make a relatively smooth blog site for my final project. It was fascinating learning everything from the low level code to the high level code and learning to appreciate how everything made is one made with intent. I really learned this lesson for my website when I was adding features and making my blog site run as smooth as possible.

Thank you Professor David J. Malan, Brian Yu, Doug Lloyd, and the rest of the (current and previous) CS50 staff and guests for organizing this course.
