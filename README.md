# Demoblaze Automation

Automated test cases for the **Demoblaze e-commerce website** using **Selenium WebDriver** and **pytest**.  
This project covers end-to-end functional testing, including login, signup, product selection, cart management, checkout, and logout functionalities.


## 🗂 Project Structure

Demoblaze_Automation/
│
├── tests/ # Test scripts
│ ├── test_add_to_cart.py
│ ├── test_checkout.py
│ ├── test_login.py
│ ├── test_logout.py
│ ├── test_remove_from_cart.py
│ └── test_signup.py
│
├── pages/ # Page Object Models (POM)
│ ├── home_page.py
│ ├── login_page.py
│ ├── cart_page.py
│ ├── checkout_page.py
│ └── signup_page.py
│
├── utils/ # Configuration and helper functions
│ ├── config.py # URL, credentials, etc.
│ └── helpers.py
│
├── docs/ # Documentation
│ ├── BugReport.docx
│ ├── TestPlan.docx
│ └── SampleTestCases.xlsx
│
├── requirements.txt # Python dependencies
└── README.md # Project overview




 Installation

1.Clone the repository:

```bash
git clone https://github.com/yourusername/Demoblaze_Automation.git

2. Navigate to the project directory:
cd Demoblaze_Automation

3.Install dependencies:
pip install -r requirements.txt
Note: Make sure you have Chrome installed and the correct ChromeDriver version compatible with your Chrome browser.


Running Tests

Run all tests:
pytest -v

Run a specific test:
pytest -v tests/test_login.py

Generate a test report (optional, if using pytest-html):
pytest --html=report.html


Test Coverage

The automation suite covers the following functionalities:

Login: Verify login with valid and invalid credentials

Signup: Create new users and validate duplicate users

Add to Cart: Select products and add to cart

Remove from Cart: Remove items from the cart

Checkout: Complete the purchase process

Logout: Verify the logout functionality

Navigation: Verify category page navigation (Phones, Laptops, Monitors)


Dependencies

All Python dependencies are listed in requirements.txt:

selenium

pytest

webdriver-manager

📄Documentation

The docs/ folder contains:

BugReport.docx: Bugs found during manual/automated testing

TestPlan.docx: Project test strategy and scope

SampleTestCases.xlsx: Sample test cases for reference

 Contributing

Contributions are welcome! Please follow standard Git workflow:

Fork the repository

Create a new branch: git checkout -b feature-name

Commit changes: git commit -m "Add feature"

Push to branch: git push origin feature-name

Open a Pull Request

License

This project is licensed under the MIT License.
