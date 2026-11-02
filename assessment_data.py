"""
assessment_data.py - Career Profiles, Benchmarks, Diagnostic Quizzes & Verified Resources
Curated for SkillPath AI to provide deterministic, transparent, and accurate guidance.
"""

CAREER_PATHS = {
    "Full-Stack Developer": {
        "description": "Builds end-to-end web applications including responsive frontends, scalable server APIs, and databases.",
        "benchmark_skills": [
            {"skill": "HTML & CSS", "target": 85, "priority": "High", "why": "Essential for semantic web structure, accessible layouts, and modern responsive UI."},
            {"skill": "JavaScript Core", "target": 90, "priority": "High", "why": "The programming language of the modern web, powering client interactivity and server runtimes."},
            {"skill": "Frontend Frameworks (React/Vue)", "target": 75, "priority": "Medium", "why": "Industry standard for building maintainable, component-driven single-page applications."},
            {"skill": "Backend APIs & Node.js/Python", "target": 80, "priority": "High", "why": "Powers business logic, authentication, and secure client-server communication."},
            {"skill": "Relational Databases & SQL", "target": 80, "priority": "High", "why": "Critical for persistent data storage, schema design, and querying structured records."},
            {"skill": "Git & Collaboration", "target": 75, "priority": "Medium", "why": "Foundational for source control, team collaboration, and CI/CD pipelines."},
            {"skill": "Deployment & Web Security", "target": 65, "priority": "Low", "why": "Ensures your applications run securely in production with HTTPS, CORS, and hosting."}
        ],
        "quiz": [
            {
                "id": "fs_1",
                "category": "HTML & CSS",
                "question": "Which HTML5 semantic element is best suited for independent, self-contained content like a blog post or news story?",
                "options": ["<section>", "<div>", "<article>", "<aside>"],
                "correct_index": 2,
                "explanation": "<article> represents an independent, self-contained piece of content that could theoretically be syndicated on its own. <section> is for thematic grouping."
            },
            {
                "id": "fs_2",
                "category": "JavaScript Core",
                "question": "What will `console.log(typeof null)` and `console.log(typeof undefined)` output in JavaScript?",
                "options": [
                    "'null' and 'undefined'",
                    "'object' and 'undefined'",
                    "'undefined' and 'object'",
                    "'object' and 'null'"
                ],
                "correct_index": 1,
                "explanation": "In JavaScript, `typeof null` returns 'object' due to a historical legacy bug in JS engine implementation, while `typeof undefined` returns 'undefined'."
            },
            {
                "id": "fs_3",
                "category": "JavaScript Core",
                "question": "What is the primary difference between `==` (loose equality) and `===` (strict equality) in JavaScript?",
                "options": [
                    "`==` compares memory references while `===` compares values",
                    "`===` performs type coercion before comparing values",
                    "`==` performs type coercion while `===` checks both value and type without coercion",
                    "`===` only works for objects and arrays"
                ],
                "correct_index": 2,
                "explanation": "Strict equality `===` does not convert types; if operands have different types, it immediately returns false. Loose equality `==` coerces types first."
            },
            {
                "id": "fs_4",
                "category": "Backend APIs & Node.js/Python",
                "question": "In RESTful API design, which HTTP method should be used to partially update an existing resource?",
                "options": ["POST", "PUT", "PATCH", "UPDATE"],
                "correct_index": 2,
                "explanation": "PATCH is used for partial modifications of a resource. PUT typically replaces the entire resource, and POST creates a new subordinate resource."
            },
            {
                "id": "fs_5",
                "category": "Relational Databases & SQL",
                "question": "Which SQL clause is used to filter aggregated grouped records (e.g., after using `GROUP BY`)?",
                "options": ["WHERE", "HAVING", "LIMIT", "FILTER"],
                "correct_index": 1,
                "explanation": "WHERE filters rows before aggregation occurs, while HAVING filters grouped results after aggregation."
            },
            {
                "id": "fs_6",
                "category": "Git & Collaboration",
                "question": "What does `git merge` do compared to `git rebase`?",
                "options": [
                    "Merge creates a join commit preserving branch history; rebase replays commits on top of another base creating a linear history",
                    "Merge deletes the branch while rebase preserves it",
                    "Merge only works locally while rebase works with remotes",
                    "There is no difference in git history"
                ],
                "correct_index": 0,
                "explanation": "git merge preserves true chronological history with a 3-way merge commit; git rebase moves the entire feature branch to begin on the tip of the target branch."
            }
        ],
        "stages": [
            {
                "order": 1,
                "title": "Modern Frontend Fundamentals & Semantic UI",
                "description": "Master semantic HTML5, modern CSS flexbox/grid layouts, responsive media queries, and accessibility best practices.",
                "duration_hours": 30,
                "topics": ["Semantic HTML5", "CSS Flexbox & CSS Grid", "Responsive Design & Mobile-First", "Web Accessibility (WCAG)", "CSS Variables & Modern Reset"],
                "resources": [
                    {"title": "MDN Web Docs - HTML Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML"},
                    {"title": "MDN Web Docs - CSS Layout (Flexbox & Grid)", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout"},
                    {"title": "FreeCodeCamp - Responsive Web Design", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/"}
                ],
                "mini_project": {
                    "title": "Developer Portfolio & Responsive Product Showcase",
                    "problem": "Create a fully responsive, accessible personal portfolio page showcasing bio, skills, and interactive project cards.",
                    "skills": "HTML5, CSS Flexbox/Grid, Mobile-First Design, Accessibility",
                    "difficulty": "Beginner",
                    "requirements": ["Semantic HTML structure", "Responsive CSS without frameworks", "Clean contact form with input validation", "Lighthouse score > 90"],
                    "stretch_goals": ["Dark mode toggle with CSS custom properties", "Subtle micro-animations for cards"],
                    "completion_criteria": "Works seamlessly across mobile (375px), tablet (768px), and desktop (1280px)."
                }
            },
            {
                "order": 2,
                "title": "Core JavaScript & DOM Manipulation",
                "description": "Deep dive into vanilla JavaScript: ES6+ syntax, asynchronous programming (Promises, async/await), DOM events, and fetch API.",
                "duration_hours": 45,
                "topics": ["ES6+ Syntax (Arrow functions, Destructuring, Spread)", "Asynchronous JS, Promises & Async/Await", "DOM Traversal & Event Delegation", "Fetch API & Error Handling", "Local Storage & State Management"],
                "resources": [
                    {"title": "JavaScript.info - The Modern JavaScript Tutorial", "url": "https://javascript.info/"},
                    {"title": "MDN Web Docs - JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"},
                    {"title": "FreeCodeCamp - JavaScript Algorithms and Data Structures", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/"}
                ],
                "mini_project": {
                    "title": "Dynamic Task Kanban Board with Local Storage",
                    "problem": "Build an interactive task organizer where users can create, edit, filter, reorder, and persist tasks across page reloads.",
                    "skills": "Vanilla JS, DOM Events, LocalStorage, Array Methods",
                    "difficulty": "Beginner-Intermediate",
                    "requirements": ["Add, edit, delete tasks", "Column state (To-Do, In Progress, Done)", "Persist data in localStorage", "Filter by search text"],
                    "stretch_goals": ["Drag and drop using HTML Drag & Drop API", "Task priority tags and due dates"],
                    "completion_criteria": "Zero external libraries, no page reload when updating tasks."
                }
            },
            {
                "order": 3,
                "title": "Backend Engineering, REST APIs & Databases",
                "description": "Construct robust RESTful web services using Python/Flask or Node/Express with SQLite/PostgreSQL database persistence.",
                "duration_hours": 50,
                "topics": ["HTTP Methods & Status Codes", "RESTful Architecture & Routing", "Relational Database Design & SQL", "CRUD Operations with ORM/SQL", "Input Validation & Password Hashing"],
                "resources": [
                    {"title": "Flask Official Documentation", "url": "https://flask.palletsprojects.com/"},
                    {"title": "MDN Web Docs - Express/Node Web Development", "url": "https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs"},
                    {"title": "PostgreSQL Tutorial - SQL Fundamentals", "url": "https://www.postgresqltutorial.com/"}
                ],
                "mini_project": {
                    "title": "Secure Student Note-Taking & Bookmark API",
                    "problem": "Design and build a REST API allowing users to authenticate, manage categorized notes, and query notes with tags.",
                    "skills": "Python/Flask or Node, SQLite, REST design, Auth, Postman",
                    "difficulty": "Intermediate",
                    "requirements": ["Endpoints for CRUD operations on notes", "SQL database with foreign keys", "Parameterized queries preventing SQL injection", "Proper HTTP status codes (200, 201, 400, 404, 500)"],
                    "stretch_goals": ["Token-based authentication (JWT or Sessions)", "Search and pagination query parameters"],
                    "completion_criteria": "Fully documented API with verified JSON responses and error handling."
                }
            },
            {
                "order": 4,
                "title": "Full-Stack Integration, Auth & Deployment",
                "description": "Connect frontend client with backend service, implement authentication, security headers, and deploy to cloud platforms.",
                "duration_hours": 45,
                "topics": ["CORS & API Integration", "Session / JWT Authentication Flow", "Environment Variables & Secret Management", "Git Workflow & CI/CD", "Production Deployment (Render / Vercel / Railway)"],
                "resources": [
                    {"title": "OWASP Top 10 Web Application Security Risks", "url": "https://owasp.org/www-project-top-ten/"},
                    {"title": "GitHub Docs - Git Workflow and Pull Requests", "url": "https://docs.github.com/en/get-started/using-git"},
                    {"title": "Render / Vercel Web Deployment Guide", "url": "https://render.com/docs"}
                ],
                "mini_project": {
                    "title": "Full-Stack Collaborative Issue Tracker",
                    "problem": "Build an end-to-end issue tracker where teams can report bugs, assign members, update statuses, and view analytics.",
                    "skills": "Frontend-Backend Integration, Database Relations, Auth, Cloud Deployment",
                    "difficulty": "Intermediate-Advanced",
                    "requirements": ["User authentication and role isolation", "Dashboard showing ticket stats", "Responsive UI communicating with backend via Fetch/Async", "Live deployed URL with Git repo"],
                    "stretch_goals": ["Email notifications or export to CSV", "Activity audit log for ticket changes"],
                    "completion_criteria": "Working live app with public Git repository and comprehensive README."
                }
            }
        ]
    },
    "Python Developer": {
        "description": "Focuses on Python fundamentals, object-oriented design, algorithmic thinking, scripting, automation, and backend web frameworks.",
        "benchmark_skills": [
            {"skill": "Python Syntax & Data Structures", "target": 90, "priority": "High", "why": "Core foundations: lists, dictionaries, sets, tuples, list comprehensions, and generators."},
            {"skill": "Object-Oriented Programming (OOP)", "target": 85, "priority": "High", "why": "Essential for building clean, maintainable, modular software using classes and inheritance."},
            {"skill": "File Handling & Error Management", "target": 80, "priority": "High", "why": "Enables robust data processing and gracefully handling exceptions and edge cases."},
            {"skill": "Web Frameworks (Flask/FastAPI)", "target": 75, "priority": "Medium", "why": "Powers web APIs and microservices for production use."},
            {"skill": "Database Integration (SQLAlchemy/SQLite)", "target": 75, "priority": "Medium", "why": "Connects Python apps to databases for persistent data storage."},
            {"skill": "Unit Testing & Debugging", "target": 70, "priority": "Medium", "why": "Writing pytest and unittest suites ensures code correctness and stability."}
        ],
        "quiz": [
            {
                "id": "py_1",
                "category": "Python Syntax & Data Structures",
                "question": "What is the time complexity of looking up a key in a standard Python dictionary on average?",
                "options": ["O(n)", "O(1)", "O(log n)", "O(n^2)"],
                "correct_index": 1,
                "explanation": "Python dictionaries are implemented using hash tables, giving average-case key lookup, insertion, and deletion O(1) time complexity."
            },
            {
                "id": "py_2",
                "category": "Python Syntax & Data Structures",
                "question": "What is the key difference between a Python list and a tuple?",
                "options": [
                    "Lists are immutable; tuples are mutable",
                    "Lists are mutable; tuples are immutable",
                    "Lists can only store numbers; tuples can store any data type",
                    "Tuples cannot be iterated over"
                ],
                "correct_index": 1,
                "explanation": "Lists can be modified after creation (mutable), while tuples cannot be changed once defined (immutable), making tuples hashable and memory-efficient."
            },
            {
                "id": "py_3",
                "category": "Object-Oriented Programming (OOP)",
                "question": "In Python, which dunder (double-underscore) method is the constructor called when a new instance is created?",
                "options": ["__new__", "__init__", "__construct__", "__start__"],
                "correct_index": 1,
                "explanation": "`__init__` is the initializer method called to initialize instance attributes after object creation."
            },
            {
                "id": "py_4",
                "category": "File Handling & Error Management",
                "question": "Why is using `with open('file.txt', 'r') as f:` preferred over `f = open('file.txt', 'r')`?",
                "options": [
                    "It runs faster in Python",
                    "It automatically closes the file even if an exception occurs inside the block",
                    "It encrypts the file during reading",
                    "It converts text into JSON automatically"
                ],
                "correct_index": 1,
                "explanation": "The `with` statement utilizes Python's context manager protocol (`__enter__` and `__exit__`), guaranteeing that system resources/file descriptors are released safely."
            },
            {
                "id": "py_5",
                "category": "Unit Testing & Debugging",
                "question": "In pytest, what is the default naming convention for test functions so they are automatically discovered?",
                "options": ["Functions ending with _test", "Functions starting with test_", "Any function decorated with @test", "Functions starting with check_"],
                "correct_index": 1,
                "explanation": "pytest automatically discovers test functions that start with `test_` within files named `test_*.py` or `*_test.py`."
            }
        ],
        "stages": [
            {
                "order": 1,
                "title": "Python Core & Algorithmic Problem Solving",
                "description": "Master data types, memory model, loops, functions, comprehensions, and basic algorithmic complexity.",
                "duration_hours": 35,
                "topics": ["Variables, Types & Memory", "Control Flow & Functions", "Collections (Lists, Dicts, Sets, Tuples)", "Comprehensions & Generators", "Time & Space Complexity Basics"],
                "resources": [
                    {"title": "Official Python 3 Tutorial", "url": "https://docs.python.org/3/tutorial/"},
                    {"title": "Automate the Boring Stuff with Python", "url": "https://automatetheboringstuff.com/"},
                    {"title": "CS50's Introduction to Programming with Python", "url": "https://cs50.harvard.edu/python/"}
                ],
                "mini_project": {
                    "title": "Automated Personal Finance & Expense Tracker CLI",
                    "problem": "Create a command-line tool that parses CSV bank statements, categorizes spending, and generates statistical summaries.",
                    "skills": "Python Core, CSV parsing, Dictionaries, Functional abstractions",
                    "difficulty": "Beginner",
                    "requirements": ["Read and validate CSV inputs", "Categorize expenses by keywords", "Generate monthly summary reports", "Handle malformed lines gracefully"],
                    "stretch_goals": ["Export summary to JSON and formatted text tables", "Add budget threshold alerts"],
                    "completion_criteria": "Runs cleanly from terminal with argument parsing."
                }
            },
            {
                "order": 2,
                "title": "Object-Oriented Design & Clean Architecture",
                "description": "Build scalable code using OOP principles: encapsulation, inheritance, polymorphism, custom exceptions, and magic methods.",
                "duration_hours": 40,
                "topics": ["Classes & Objects", "Inheritance & Composition", "Dunder Methods & Operator Overloading", "Custom Exceptions & Robust Error Handling", "Type Hinting & Dataclasses"],
                "resources": [
                    {"title": "Real Python - Object-Oriented Programming in Python", "url": "https://realpython.com/python3-object-oriented-programming/"},
                    {"title": "Refactoring.Guru - Design Patterns in Python", "url": "https://refactoring.guru/design-patterns/python"}
                ],
                "mini_project": {
                    "title": "Library & Inventory Management Engine",
                    "problem": "Build an object-oriented inventory system simulating item borrowing, member tracking, overdue fines, and transaction logging.",
                    "skills": "OOP, Dataclasses, Custom Exceptions, File Persistence",
                    "difficulty": "Intermediate",
                    "requirements": ["Clean class hierarchy (Book, Member, Transaction)", "Encapsulated business rules", "Unit tests for overdue calculation", "Data persistence to JSON/SQLite"],
                    "stretch_goals": ["Add observer pattern for inventory alerts", "Type hints across all modules"],
                    "completion_criteria": "Well-tested domain model with > 80% test coverage."
                }
            },
            {
                "order": 3,
                "title": "Python Web Services & SQLite Database",
                "description": "Develop production-ready RESTful web APIs using Flask or FastAPI with SQLite relational persistence.",
                "duration_hours": 45,
                "topics": ["Flask/FastAPI Request-Response Cycle", "RESTful API Endpoints", "SQLite Integration & Parameterized SQL", "Authentication & Security", "Unit Testing with Pytest"],
                "resources": [
                    {"title": "Flask Mega-Tutorial by Miguel Grinberg", "url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world"},
                    {"title": "FastAPI Official Documentation", "url": "https://fastapi.tiangolo.com/"},
                    {"title": "Pytest Official Documentation", "url": "https://docs.pytest.org/"}
                ],
                "mini_project": {
                    "title": "Job Application Tracker REST API with Pytest Suite",
                    "problem": "Build an API for students to track internship applications, interview rounds, reminders, and company feedback.",
                    "skills": "Flask/FastAPI, SQLite, Pytest, HTTP Status Codes",
                    "difficulty": "Intermediate",
                    "requirements": ["REST CRUD endpoints", "SQL queries with foreign key constraints", "Pytest suite testing edge cases", "Clear API documentation"],
                    "stretch_goals": ["Export applications to Excel/CSV", "Docker containerization"],
                    "completion_criteria": "All pytest cases pass cleanly."
                }
            }
        ]
    },
    "Data Analyst": {
        "description": "Transforms raw business and scientific data into actionable insights using SQL, Python (Pandas/NumPy), and interactive visualizations.",
        "benchmark_skills": [
            {"skill": "SQL & Relational Querying", "target": 90, "priority": "High", "why": "The industry standard tool for extracting, aggregating, and joining data from corporate warehouses."},
            {"skill": "Python for Data Analysis (Pandas, NumPy)", "target": 85, "priority": "High", "why": "Core toolkit for data cleaning, transformation, reshaping, and numerical computations."},
            {"skill": "Data Visualization (Matplotlib, Seaborn)", "target": 80, "priority": "Medium", "why": "Communicating patterns, distributions, and trends visually to non-technical stakeholders."},
            {"skill": "Exploratory Data Analysis (EDA) & Statistics", "target": 80, "priority": "High", "why": "Understanding descriptive statistics, distributions, hypothesis testing, and anomaly detection."},
            {"skill": "Business Intelligence Tools (Power BI / Tableau)", "target": 70, "priority": "Medium", "why": "Designing interactive executive dashboards and KPI monitoring reports."}
        ],
        "quiz": [
            {
                "id": "da_1",
                "category": "SQL & Relational Querying",
                "question": "Which SQL join returns all rows from the left table, and the matched rows from the right table (with NULLs for non-matches)?",
                "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN"],
                "correct_index": 1,
                "explanation": "A LEFT JOIN preserves every row from the left table regardless of whether there is a matching row in the right table."
            },
            {
                "id": "da_2",
                "category": "Python for Data Analysis (Pandas, NumPy)",
                "question": "In Pandas, which method is most commonly used to inspect the count of non-null values and data types of each column in a DataFrame?",
                "options": ["df.describe()", "df.info()", "df.head()", "df.dtypes()"],
                "correct_index": 1,
                "explanation": "`df.info()` prints a concise summary including column names, non-null counts, and data types."
            },
            {
                "id": "da_3",
                "category": "Exploratory Data Analysis (EDA) & Statistics",
                "question": "Which measure of central tendency is least sensitive to extreme outliers in a skewed dataset?",
                "options": ["Mean", "Median", "Standard Deviation", "Variance"],
                "correct_index": 1,
                "explanation": "The median represents the 50th percentile (middle value) and is robust against extreme outlier values."
            },
            {
                "id": "da_4",
                "category": "Data Visualization (Matplotlib, Seaborn)",
                "question": "Which visualization type is best suited to show the distribution and five-number summary (quartiles) of a continuous variable?",
                "options": ["Pie Chart", "Box Plot (Box-and-Whisker)", "Line Chart", "Stacked Bar Chart"],
                "correct_index": 1,
                "explanation": "A box plot displays the minimum, first quartile, median, third quartile, and maximum, along with potential outliers."
            }
        ],
        "stages": [
            {
                "order": 1,
                "title": "Advanced SQL & Database Analytics",
                "description": "Master complex queries, aggregations, multi-table joins, subqueries, and window functions on real datasets.",
                "duration_hours": 30,
                "topics": ["Joins (Inner, Left, Self, Full)", "Aggregate Functions & Group By", "Window Functions (ROW_NUMBER, RANK, LAG/LEAD)", "Subqueries & Common Table Expressions (CTEs)", "Data Cleansing in SQL"],
                "resources": [
                    {"title": "Mode Analytics SQL Tutorial for Data Analysis", "url": "https://mode.com/sql-tutorial/"},
                    {"title": "SQLZoo Interactive SQL Practice", "url": "https://sqlzoo.net/"}
                ],
                "mini_project": {
                    "title": "E-Commerce Customer Retention & Sales SQL Analysis",
                    "problem": "Write SQL queries on an online store dataset to calculate customer lifetime value, monthly cohort retention, and churn.",
                    "skills": "SQL Joins, CTEs, Window Functions, Aggregations",
                    "difficulty": "Beginner-Intermediate",
                    "requirements": ["Calculate repeat purchase rate", "Identify top 10% spending customers", "Monthly revenue growth percentage using LAG", "Clean queries with comments"],
                    "stretch_goals": ["Build views for KPI metrics", "Automate query report execution"],
                    "completion_criteria": "Accurate SQL scripts with documented business insights."
                }
            },
            {
                "order": 2,
                "title": "Python Data Wrangling with Pandas & NumPy",
                "description": "Learn to load, inspect, clean, reshape, merge, and transform messy real-world datasets using Pandas and NumPy.",
                "duration_hours": 40,
                "topics": ["Pandas DataFrames & Series", "Handling Missing Data & Outliers", "Data Transformation & String Operations", "Grouping, Pivoting & Merging", "Datetime Manipulation"],
                "resources": [
                    {"title": "Pandas Official 10 Minutes Guide", "url": "https://pandas.pydata.org/docs/user_guide/10min.html"},
                    {"title": "Kaggle Python & Pandas Micro-Courses", "url": "https://www.kaggle.com/learn"}
                ],
                "mini_project": {
                    "title": "Real-World Job Postings & Salary Data Cleaning Pipeline",
                    "problem": "Clean and preprocess a scraped dataset of tech job postings with inconsistent salary strings, missing tags, and duplicates.",
                    "skills": "Pandas, Regular Expressions, Data Imputation, Type Casting",
                    "difficulty": "Intermediate",
                    "requirements": ["Extract standardized min/max salary numbers", "Handle missing values with justification", "Deduplicate listings", "Export clean dataset for visualization"],
                    "stretch_goals": ["Create reusable data cleaning functions", "Validate schema with assertions"],
                    "completion_criteria": "Reproducible Jupyter notebook or Python pipeline script."
                }
            },
            {
                "order": 3,
                "title": "Exploratory Data Analysis & Visual Storytelling",
                "description": "Uncover hidden patterns, correlations, and business stories using Matplotlib, Seaborn, and statistical tests.",
                "duration_hours": 35,
                "topics": ["Descriptive Statistics & Correlation", "Distribution & Categorical Plots", "Heatmaps & Pairplots", "Storytelling with Data Principles", "Executive Summary Presentation"],
                "resources": [
                    {"title": "Seaborn Official Tutorial", "url": "https://seaborn.pydata.org/tutorial.html"},
                    {"title": "Storytelling with Data by Cole Nussbaumer Knaflic (Summary & Guide)", "url": "https://www.storytellingwithdata.com/"}
                ],
                "mini_project": {
                    "title": "Comprehensive Student Academic Performance EDA Report",
                    "problem": "Conduct a thorough exploratory data analysis on student learning factors, identifying key drivers of test success.",
                    "skills": "Seaborn, Matplotlib, Statistical Correlation, Markdown Report",
                    "difficulty": "Intermediate",
                    "requirements": ["Univariate and bivariate analysis", "Correlation matrix heatmap", "At least 5 business/actionable recommendations", "Clear narrative takeaways"],
                    "stretch_goals": ["Interactive Plotly charts", "Executive 1-page PDF summary"],
                    "completion_criteria": "Polished analysis report with visual figures."
                }
            }
        ]
    },
    "AI/ML Engineer": {
        "description": "Designs and deploys machine learning models, neural networks, and generative AI systems using modern math, Python, Scikit-Learn, and PyTorch.",
        "benchmark_skills": [
            {"skill": "Mathematics for ML (Linear Algebra, Calculus, Probability)", "target": 80, "priority": "High", "why": "Core theory behind gradient descent, cost functions, matrix transformations, and Bayes rule."},
            {"skill": "Classical Machine Learning (Scikit-Learn)", "target": 85, "priority": "High", "why": "Supervised & unsupervised algorithms: regression, classification, clustering, evaluation metrics."},
            {"skill": "Deep Learning & PyTorch/TensorFlow", "target": 80, "priority": "High", "why": "Building neural architectures, CNNs, Transformers, and training with GPUs."},
            {"skill": "Feature Engineering & Data Preprocessing", "target": 85, "priority": "High", "why": "Scaling, encoding, feature selection, and preventing data leakage."},
            {"skill": "MLOps & Model Deployment (FastAPI, ONNX, Hugging Face)", "target": 70, "priority": "Medium", "why": "Serving models as low-latency microservices with API endpoints and monitoring."}
        ],
        "quiz": [
            {
                "id": "ml_1",
                "category": "Classical Machine Learning (Scikit-Learn)",
                "question": "What is the primary indicator of overfitting in a machine learning model?",
                "options": [
                    "High training loss and high validation loss",
                    "Very low training loss but significantly higher validation loss",
                    "Equal training and validation loss",
                    "Low accuracy on training data and high accuracy on validation data"
                ],
                "correct_index": 1,
                "explanation": "Overfitting happens when a model learns noise and specific details of the training set, performing exceptionally well on train data but failing to generalize to unseen validation data."
            },
            {
                "id": "ml_2",
                "category": "Classical Machine Learning (Scikit-Learn)",
                "question": "For an imbalanced classification problem (e.g., fraud detection with 99% legitimate transactions), why is raw Accuracy misleading?",
                "options": [
                    "Accuracy cannot be calculated with decimals",
                    "A naive model that always predicts 'not fraud' achieves 99% accuracy while detecting zero frauds",
                    "Accuracy requires balanced features rather than balanced classes",
                    "Accuracy only works for regression models"
                ],
                "correct_index": 1,
                "explanation": "In severe class imbalance, high accuracy can be achieved simply by always guessing the majority class, masking complete failure to detect the positive class. Precision, Recall, and F1-score are needed."
            },
            {
                "id": "ml_3",
                "category": "Feature Engineering & Data Preprocessing",
                "question": "Why must feature scaling (like StandardScaler) be fit ONLY on the training set and not on the whole dataset?",
                "options": [
                    "To save memory",
                    "To prevent data leakage from the test set into the training process",
                    "Because test data cannot be scaled",
                    "StandardScaler only accepts 100 rows"
                ],
                "correct_index": 1,
                "explanation": "Fitting scalers on test data introduces data leakage, giving the model prior knowledge of the test set's mean and variance that it wouldn't have in production."
            },
            {
                "id": "ml_4",
                "category": "Deep Learning & PyTorch/TensorFlow",
                "question": "What purpose does an activation function (like ReLU or GELU) serve in a neural network layer?",
                "options": [
                    "It converts numbers to integers",
                    "It introduces non-linearity, enabling the network to learn complex non-linear patterns",
                    "It stops backpropagation",
                    "It normalizes weights to 1"
                ],
                "correct_index": 1,
                "explanation": "Without non-linear activation functions, stacked neural network layers collapse mathematically into a single linear transformation, regardless of network depth."
            }
        ],
        "stages": [
            {
                "order": 1,
                "title": "Mathematics & Core Machine Learning Foundations",
                "description": "Understand gradient descent, loss functions, linear/logistic regression, decision trees, and validation metrics.",
                "duration_hours": 40,
                "topics": ["Linear Algebra & Matrix Ops", "Calculus & Gradient Descent", "Supervised Learning (Regression & Trees)", "Validation Strategies (K-Fold Cross-Validation)", "Evaluation Metrics (ROC-AUC, F1, RMSE)"],
                "resources": [
                    {"title": "3Blue1Brown - Essence of Linear Algebra", "url": "https://www.3blue1brown.com/topics/linear-algebra"},
                    {"title": "Scikit-Learn Official User Guide", "url": "https://scikit-learn.org/stable/user_guide.html"},
                    {"title": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"}
                ],
                "mini_project": {
                    "title": "Student Churn & Exam Score Prediction Engine",
                    "problem": "Build and evaluate competing machine learning models to predict student completion rates with complete cross-validation.",
                    "skills": "Scikit-Learn, Feature Pipeline, Metrics, Hyperparameter Tuning",
                    "difficulty": "Intermediate",
                    "requirements": ["Data preprocessing pipeline without leakage", "Compare at least 3 models (Ridge, Random Forest, Gradient Boosting)", "Hyperparameter search with GridSearchCV", "Confusion matrix & feature importance plot"],
                    "stretch_goals": ["Model explainability using SHAP values", "Save model artifact using Joblib"],
                    "completion_criteria": "Structured Jupyter notebook with rigorous validation."
                }
            },
            {
                "order": 2,
                "title": "Deep Learning & Modern Neural Architectures",
                "description": "Build, train, and fine-tune neural networks using PyTorch, exploring CNNs, embeddings, and Transformer concepts.",
                "duration_hours": 50,
                "topics": ["Tensors & PyTorch Autograd", "Multi-Layer Perceptrons (MLP)", "Convolutional Neural Networks (CNNs)", "Transfer Learning & Fine-Tuning", "Transformer Self-Attention Mechanics"],
                "resources": [
                    {"title": "PyTorch Official Tutorials & 60-Minute Blitz", "url": "https://pytorch.org/tutorials/"},
                    {"title": "DeepLearning.AI - Neural Networks and Deep Learning", "url": "https://www.deeplearning.ai/"},
                    {"title": "Hugging Face NLP Course", "url": "https://huggingface.co/learn/nlp-course"}
                ],
                "mini_project": {
                    "title": "Domain-Specific Text Classifier & Sentiment API",
                    "problem": "Fine-tune a pretrained transformer model (DistilBERT) to classify student feedback comments into actionable categories.",
                    "skills": "PyTorch, Hugging Face Transformers, Tokenization, Fine-Tuning",
                    "difficulty": "Advanced",
                    "requirements": ["Dataset tokenization and DataLoader pipeline", "Fine-tuning loop with validation loss tracking", "Evaluation on held-out test split", "Inference function returning predictions and confidence"],
                    "stretch_goals": ["Export to ONNX for fast CPU inference", "Wrap in lightweight FastAPI endpoint"],
                    "completion_criteria": "Working inference script on custom input sentences."
                }
            }
        ]
    },
    "Java Developer": {
        "description": "Specializes in enterprise software development, robust object-oriented architecture, Spring Boot microservices, and high-throughput systems.",
        "benchmark_skills": [
            {"skill": "Core Java (OOP, Collections, Streams, Concurrency)", "target": 90, "priority": "High", "why": "Foundational JVM knowledge: generics, memory management, multi-threading, and lambda expressions."},
            {"skill": "Spring Boot & RESTful Services", "target": 85, "priority": "High", "why": "The premier Java framework for creating standalone, production-grade microservices."},
            {"skill": "JPA / Hibernate & SQL", "target": 80, "priority": "High", "why": "Industry standard Object-Relational Mapping (ORM) for enterprise database persistence."},
            {"skill": "Build Tools & Testing (Maven/Gradle, JUnit, Mockito)", "target": 75, "priority": "Medium", "why": "Automates builds, dependency management, and robust unit/integration testing."},
            {"skill": "Software Design Patterns & Clean Code", "target": 75, "priority": "Medium", "why": "Applying SOLID principles, Factory, Repository, and Singleton patterns."}
        ],
        "quiz": [
            {
                "id": "java_1",
                "category": "Core Java (OOP, Collections, Streams, Concurrency)",
                "question": "What is the difference between `ArrayList` and `LinkedList` in Java when accessing an element by index?",
                "options": [
                    "ArrayList is O(1) random access; LinkedList is O(n) sequential traversal",
                    "ArrayList is O(n); LinkedList is O(1)",
                    "Both provide O(1) access",
                    "LinkedList does not support indexing"
                ],
                "correct_index": 0,
                "explanation": "ArrayList is backed by a contiguous array allowing instant O(1) indexed lookup. LinkedList must traverse node pointers sequentially (O(n))."
            },
            {
                "id": "java_2",
                "category": "Core Java (OOP, Collections, Streams, Concurrency)",
                "question": "In Java memory management, where are object instances stored, and where are local primitive variables kept?",
                "options": [
                    "Objects are on the Stack; primitives are on the Heap",
                    "Objects are on the Heap; local primitives are on the Stack",
                    "Both are stored exclusively in the Metaspace",
                    "Both are stored on the Stack"
                ],
                "correct_index": 1,
                "explanation": "In Java, dynamically allocated objects reside on the Heap (managed by Garbage Collection), while method call frames and local primitives are allocated on the thread's Stack."
            },
            {
                "id": "java_3",
                "category": "Spring Boot & RESTful Services",
                "question": "Which Spring Boot annotation marks a class as a REST controller where methods return JSON responses automatically?",
                "options": ["@Controller", "@RestController", "@Service", "@Component"],
                "correct_index": 1,
                "explanation": "`@RestController` is a convenience annotation that combines `@Controller` and `@ResponseBody`, eliminating the need to annotate every handling method with `@ResponseBody`."
            },
            {
                "id": "java_4",
                "category": "JPA / Hibernate & SQL",
                "question": "In Spring Data JPA, what interface can you extend to get standard CRUD methods without writing custom implementation code?",
                "options": ["JpaRepository", "SqlManager", "DataConnector", "DatabaseService"],
                "correct_index": 0,
                "explanation": "Extending `JpaRepository<Entity, ID>` provides built-in methods like `save()`, `findById()`, `findAll()`, and `deleteById()` automatically."
            }
        ],
        "stages": [
            {
                "order": 1,
                "title": "Core Java Mastery & Collections Framework",
                "description": "Deep dive into JVM internals, Object-Oriented principles, Collections framework, Generics, and modern Stream API.",
                "duration_hours": 40,
                "topics": ["Java JVM Architecture (Heap, Stack, GC)", "OOP & SOLID Principles in Java", "Collections Framework (List, Set, Map)", "Java Streams & Lambdas", "Exception Hierarchy & Multi-threading Basics"],
                "resources": [
                    {"title": "Oracle Official Java Documentation & Tutorials", "url": "https://docs.oracle.com/javase/tutorial/"},
                    {"title": "Baeldung - Java Collections Guide", "url": "https://www.baeldung.com/category/java/java-collections"}
                ],
                "mini_project": {
                    "title": "Multi-Threaded Banking & Transaction Simulation",
                    "problem": "Create a thread-safe banking system that handles concurrent account transfers, deposits, and statement audits without race conditions.",
                    "skills": "Java Concurrency, Synchronization, Streams, Unit Testing",
                    "difficulty": "Intermediate",
                    "requirements": ["Thread-safe account transfers using locks or synchronized blocks", "Audit log generation using Streams", "Custom exceptions (InsufficientFundsException)", "JUnit tests for race condition checks"],
                    "stretch_goals": ["Thread pool execution using ExecutorService", "Deadlock prevention algorithm"],
                    "completion_criteria": "Zero concurrency errors under stress test with 50 threads."
                }
            },
            {
                "order": 2,
                "title": "Enterprise Microservices with Spring Boot & JPA",
                "description": "Build enterprise-grade RESTful APIs using Spring Boot, Spring Data JPA, Hibernate, and embedded databases.",
                "duration_hours": 45,
                "topics": ["Spring Boot Dependency Injection & IoC", "Spring MVC & REST Endpoints", "Spring Data JPA & Entity Relationships", "DTO Pattern & ModelMapper", "JUnit 5 & Mockito Unit Testing"],
                "resources": [
                    {"title": "Spring Boot Official Reference Documentation", "url": "https://docs.spring.io/spring-boot/docs/current/reference/html/"},
                    {"title": "Baeldung - REST with Spring Tutorial", "url": "https://www.baeldung.com/rest-with-spring-series"}
                ],
                "mini_project": {
                    "title": "Enterprise Course Registration & Enrollment Service",
                    "problem": "Design a complete Spring Boot REST microservice for managing students, courses, prerequisites, and grade reports.",
                    "skills": "Spring Boot, JPA, SQLite/H2, DTOs, Mockito",
                    "difficulty": "Intermediate-Advanced",
                    "requirements": ["Entity relationships (@OneToMany, @ManyToMany)", "Pagination and sorting on course listings", "Validation annotations (@NotNull, @Size, @Email)", "Mockito unit tests for service layer"],
                    "stretch_goals": ["Swagger/OpenAPI documentation", "Spring Security basic auth"],
                    "completion_criteria": "Clean Spring Boot application with passing JUnit test suite."
                }
            }
        ]
    },
    "Backend Developer": {
        "description": "Engineers scalable server systems, high-performance database architectures, secure authentication, caching, and distributed systems.",
        "benchmark_skills": [
            {"skill": "API Design & Protocols (REST, GraphQL, gRPC)", "target": 90, "priority": "High", "why": "Creating clean, versioned, consistent interfaces for client consumers."},
            {"skill": "Relational & NoSQL Databases", "target": 85, "priority": "High", "why": "Schema normalization, indexing, query optimization, and transactions."},
            {"skill": "Authentication & Authorization (JWT, OAuth2, RBAC)", "target": 85, "priority": "High", "why": "Securing data, sessions, password hashing (bcrypt/argon2), and role-based permissions."},
            {"skill": "Caching & Performance (Redis, CDN)", "target": 75, "priority": "Medium", "why": "Reducing database bottlenecks and latency through efficient caching strategies."},
            {"skill": "System Design & Scalability Basics", "target": 75, "priority": "Medium", "why": "Load balancing, horizontal scaling, database replication, and message queues."}
        ],
        "quiz": [
            {
                "id": "be_1",
                "category": "Relational & NoSQL Databases",
                "question": "In relational databases, what does the 'I' in ACID transaction properties stand for?",
                "options": ["Integrity", "Isolation", "Indexing", "Idempotency"],
                "correct_index": 1,
                "explanation": "ACID stands for Atomicity, Consistency, Isolation, and Durability. Isolation ensures that concurrent execution of transactions leaves the database in the same state as if executed sequentially."
            },
            {
                "id": "be_2",
                "category": "Authentication & Authorization (JWT, OAuth2, RBAC)",
                "question": "Why should passwords NEVER be stored using simple MD5 or SHA-256 hashes?",
                "options": [
                    "Because MD5 and SHA-256 are too slow",
                    "Because they are fast unsalted hashes vulnerable to rainbow table lookups and brute-force GPU cracking; slow adaptive algorithms like bcrypt or argon2 must be used",
                    "Because hashes can be converted back to plaintext with a single mathematical equation",
                    "Because databases cannot store hex strings"
                ],
                "correct_index": 1,
                "explanation": "General-purpose hash algorithms (MD5, SHA-256) are designed for speed and data integrity, making them susceptible to billions of guesses per second on modern hardware. Passwords require key-stretching algorithms with work factors (e.g., bcrypt, argon2id)."
            },
            {
                "id": "be_3",
                "category": "Caching & Performance (Redis, CDN)",
                "question": "What is the 'Cache-Aside' (Lazy Loading) pattern?",
                "options": [
                    "The database writes data directly to the cache periodically",
                    "The application checks the cache first; on a cache miss, it reads from the database, writes the result to cache, and returns it",
                    "The application only reads from cache and never queries the database",
                    "Cache entries are never invalidated"
                ],
                "correct_index": 1,
                "explanation": "In Cache-Aside, the application first requests data from the cache. If missing (cache miss), it queries the database, stores the data in the cache for next time, and returns the response."
            },
            {
                "id": "be_4",
                "category": "API Design & Protocols (REST, GraphQL, gRPC)",
                "question": "What does it mean for an HTTP method to be 'Idempotent'?",
                "options": [
                    "It executes in under 100 milliseconds",
                    "Making multiple identical requests has the same outcome on server state as making a single request",
                    "It requires user authentication",
                    "It cannot return an error"
                ],
                "correct_index": 1,
                "explanation": "Idempotence means multiple identical requests have the exact same effect on server state as a single request. GET, PUT, and DELETE are idempotent; POST is typically not."
            }
        ],
        "stages": [
            {
                "order": 1,
                "title": "Advanced Database Architecture & Query Optimization",
                "description": "Master relational schema design, indexing strategies (B-Tree), transactions, and query execution plans.",
                "duration_hours": 35,
                "topics": ["Database Normalization (1NF, 2NF, 3NF)", "Indexes & B-Tree Execution Plans", "ACID Transactions & Lock Levels", "Connection Pooling & Migrations", "SQL Query Optimization"],
                "resources": [
                    {"title": "Use The Index, Luke! - Guide to Database Performance", "url": "https://use-the-index-luke.com/"},
                    {"title": "PostgreSQL Official Documentation", "url": "https://www.postgresql.org/docs/"}
                ],
                "mini_project": {
                    "title": "High-Throughput Analytics & Ledger Schema with Explain Plans",
                    "problem": "Design a relational schema for a financial ledger handling high write volume, analyzing query execution plans with EXPLAIN ANALYZE.",
                    "skills": "Database Indexing, Transactions, Query Optimization, Foreign Keys",
                    "difficulty": "Intermediate",
                    "requirements": ["Normalized schema with composite indexes", "Simulate 50,000 ledger rows", "Measure execution time before and after indexing", "Atomic multi-account transfer transaction"],
                    "stretch_goals": ["Implement optimistic locking with version column", "Soft delete pattern"],
                    "completion_criteria": "Demonstrated 10x query speedup with indexes documented."
                }
            },
            {
                "order": 2,
                "title": "Production API Architecture, Caching & Auth",
                "description": "Build high-reliability APIs featuring JWT authentication, role-based access control, Redis caching, and rate limiting.",
                "duration_hours": 45,
                "topics": ["REST Best Practices & Versioning", "JWT vs Server-Side Sessions", "Role-Based Access Control (RBAC)", "In-Memory Caching Strategies", "API Rate Limiting & Input Validation"],
                "resources": [
                    {"title": "RESTful API Design Best Practices", "url": "https://restfulapi.net/"},
                    {"title": "OWASP API Security Top 10", "url": "https://owasp.org/www-project-api-security/"}
                ],
                "mini_project": {
                    "title": "Secure Multi-Tenant SaaS Backend with Rate Limiting",
                    "problem": "Create a robust backend service supporting multiple organizations, user roles (Admin, Member, Viewer), and token bucket rate limiting.",
                    "skills": "Authentication, RBAC, Caching/Rate Limiting, REST API",
                    "difficulty": "Advanced",
                    "requirements": ["Password hashing with bcrypt/argon2", "Role middleware checking permissions per route", "Rate limiter returning 429 Too Many Requests", "Comprehensive test suite for auth edge cases"],
                    "stretch_goals": ["Refresh token rotation flow", "Docker-compose setup"],
                    "completion_criteria": "All endpoints secured and tested against unauthorized access."
                }
            }
        ]
    }
}

ALL_SKILLS_LIST = [
    "HTML & CSS", "JavaScript Core", "Frontend Frameworks (React/Vue)", "Backend APIs & Node.js/Python",
    "Relational Databases & SQL", "Git & Collaboration", "Deployment & Web Security",
    "Python Syntax & Data Structures", "Object-Oriented Programming (OOP)", "File Handling & Error Management",
    "Web Frameworks (Flask/FastAPI)", "Database Integration (SQLAlchemy/SQLite)", "Unit Testing & Debugging",
    "SQL & Relational Querying", "Python for Data Analysis (Pandas, NumPy)", "Data Visualization (Matplotlib, Seaborn)",
    "Exploratory Data Analysis (EDA) & Statistics", "Business Intelligence Tools (Power BI / Tableau)",
    "Mathematics for ML (Linear Algebra, Calculus, Probability)", "Classical Machine Learning (Scikit-Learn)",
    "Deep Learning & PyTorch/TensorFlow", "Feature Engineering & Data Preprocessing", "MLOps & Model Deployment",
    "Core Java (OOP, Collections, Streams, Concurrency)", "Spring Boot & RESTful Services", "JPA / Hibernate & SQL",
    "Build Tools & Testing (Maven/Gradle, JUnit, Mockito)", "Software Design Patterns & Clean Code",
    "API Design & Protocols (REST, GraphQL, gRPC)", "Authentication & Authorization (JWT, OAuth2, RBAC)",
    "Caching & Performance (Redis, CDN)", "System Design & Scalability Basics"
]
