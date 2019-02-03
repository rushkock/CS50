# Ruchella Kock
# 12460796
# Implements a stock trading website
# My personal touch is to allow users to change their passwords and Require users' passwords to have some number of letters, numbers, and/or symbols


import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup, usd

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        new_password = request.form.get("confirmation")
        # ensure that all fiels were filled in correctly
        if not username:
            return apology("Fill in all fields")

        if check_password(password, new_password):
            # encrypt the users' password
            hash = generate_password_hash(password)

            # add user to the database
            result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username, hash=hash)
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

            # check if the username already existed
            if not result:
                return apology("Username already in use")

            # log the user in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")
        else:
            return apology("One or more fields filled in incorrectly")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    id = session["user_id"]
    # select the portfolio of the user if the sum(shares) <= 0 don't select it
    shares = db.execute(
        "SELECT SUM(shares), stock, price, SUM(value) FROM portfolio WHERE id = :id GROUP BY stock HAVING SUM(shares) > 0 ", id=id)
    total_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=id)
    return render_template("index.html", shares=shares, cash=total_cash[0]["cash"])


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        looked_up = lookup(symbol)
        # check if user filled in a symbol
        if not symbol:
            return apology("Fill in all fields")
        # check if symbol exists
        elif looked_up == None:
            return apology("Your stock symbol doesn't exist")
        return render_template("quoted.html", name=looked_up["name"], symbol=looked_up["symbol"], price=looked_up["price"])
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure all fields were submitted and that the shares are digits
        if not symbol or not shares:
            return apology("Please fill in all fields")
        elif not shares.isdigit():
            return apology("Please fill in a numerical value")

        # look the symbol up and check if the symbol exists
        looked_up = lookup(symbol)
        if looked_up == None:
            return apology("Stock doesn't exist")
        id = session["user_id"]
        price = looked_up["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=id)
        total_cost = int(shares) * looked_up["price"]

        # check if user has enough money, if they do buy the stock
        if int(cash[0]["cash"]) > int(total_cost):
            db.execute("INSERT INTO portfolio (id, stock, shares, price, value, date)"
                       "VALUES (:id, :symbol, :shares, :price, :value, CURRENT_TIMESTAMP)",
                       id=id, symbol=symbol.upper(), shares=shares, price=price, value=price * int(shares))
            db.execute("UPDATE users SET cash = cash - :total_cost WHERE id = :id", id=id, total_cost=total_cost)
        else:
            return apology("Not enough funds")

        # Redirect user to home page
        flash("Bought!")
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol or not shares:
            return apology("Fill in all fields")
        if not shares.isdigit():
            return apology("Please fill in a numerical value")

        id = session["user_id"]
        looked_up = lookup(symbol)
        price = looked_up["price"]
        # check if the user has enough shares
        check_shares = db.execute("SELECT SUM(shares), stock FROM portfolio WHERE id = :id GROUP BY stock", id=id)
        for share in range(len(check_shares)):
            if check_shares[share]["stock"] == symbol:
                if int(check_shares[share]["SUM(shares)"]) < int(shares):
                    return apology("Not enough shares")
        # sell the share by updating the cash and inserting the field in portfolio with (- number of shares)
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=id)
        total_profit = int(shares) * looked_up["price"]
        db.execute("INSERT INTO portfolio (id, stock, shares, price, value, date)"
                   "VALUES (:id, :symbol, :shares, :price, :value, CURRENT_TIMESTAMP)",
                   id=id, symbol=symbol.upper(), shares=0 - int(shares), price=price, value=price * -int(shares))
        db.execute("UPDATE users SET cash = cash + :total_profit WHERE id = :id", id=id, total_profit=total_profit)
        flash("Sold!")
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        id = session["user_id"]
        stocks = db.execute("SELECT stock, SUM(shares) FROM portfolio WHERE id = :id GROUP BY stock HAVING SUM(shares) > 0", id=id)
        return render_template("sell.html", stocks=stocks)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id = session["user_id"]
    history = db.execute("SELECT * FROM portfolio WHERE id = :id", id=id)
    return render_template("history.html", history=history)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        old_password = request.form.get("old_password")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check if password is correct
        rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        if not check_password_hash(rows[0]["hash"], old_password):
            return apology("Password incorrect")
        # check if the new password is properly implemented
        if check_password(password, confirmation):
            # encrypt the users' password
            hash = generate_password_hash(password)

            # update hash
            db.execute("UPDATE users SET hash = :hash", hash=hash)
            flash("Password changed!")
            # Redirect user to home page
            return redirect("/")
        else:
            return apology("One or more fields filled in incorrectly")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        id = session["user_id"]
        username = db.execute("SELECT username FROM users WHERE id = :id", id=id)
        username = username[0]["username"]
        total_cash = db.execute("SELECT cash FROM users WHERE id = :id", id=id)
        cash = total_cash[0]["cash"]
        return render_template("account.html", username=username, cash=cash)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


def check_password(password, new_password):
    """Make sure password is correctly chosen"""

    # ensure that all fiels were filled in correctly
    if password != new_password:
        return False

    # check if password has number, length and symbols
    number = len(re.findall(r"[0-9]", password))
    capital = len(re.findall(r"[A-Z]", password))
    lower = len(re.findall(r"[a-z]", password))
    return len(password) > 5 and number > 0 and capital > 0 and lower > 0



# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
