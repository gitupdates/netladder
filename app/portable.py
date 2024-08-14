import flask
import requests
from flask import request

app = flask.Flask(__name__)
googlebot_headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
}
html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>13ft Ladder</title>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet" async>
    <style>
        body {
            font-family: 'Open Sans', sans-serif;
            background-color: #FFF;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 90vh;
            transition: background-color 0.3s, color 0.3s;
        }

        h1 {
            font-size: 1.5rem;
            margin-bottom: 20px;
            text-align: center;
            color: #333;
        }

        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
        }

        input[type=text] {
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            width: 100%;
            font-size: 1rem;
            box-sizing: border-box;
        }

        input[type="submit"] {
            padding: 10px;
            background-color: #6a0dad;
            color: #fff;
            border: none;
            border-radius: 5px;
            width: 100%;
            text-transform: uppercase;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        input[type="submit"]:hover {
            background-color: #4e0875;
        }

        /* Toggle switch styles */
        .dark-mode-toggle {
            position: absolute;
            top: 10px;
            right: 10px;
        }

        .dark-mode-toggle input {
            display: none;
        }

        .dark-mode-toggle label {
            cursor: pointer;
            text-indent: -9999px;
            width: 52px;
            height: 27px;
            background: grey;
            display: block;
            border-radius: 100px;
            position: relative;
        }

        .dark-mode-toggle label:after {
            content: '';
            position: absolute;
            top: 2px;
            left: 2px;
            width: 23px;
            height: 23px;
            background: #fff;
            border-radius: 90px;
            transition: 0.3s;
        }

        .dark-mode-toggle input:checked+label {
            background: #6a0dad;
        }

        .dark-mode-toggle input:checked+label:after {
            left: calc(100% - 2px);
            transform: translateX(-100%);
        }

        /* Responsive adjustments */
        @media only screen and (max-width: 600px) {
            form {
                padding: 10px;
            }

            h1 {
                font-size: 1.2rem;
            }
        }

        /* Dark mode styles */
        body.dark-mode {
            background-color: #333;
            color: #FFF;
        }

        body.dark-mode h1 {
            color: #FFF;
        }

        body.dark-mode input[type=text] {
            background-color: #555;
            border: 1px solid #777;
            color: #FFF;
        }

        body.dark-mode input[type="submit"] {
            background-color: #9b30ff;
        }

        body.dark-mode input[type="submit"]:hover {
            background-color: #7a1bb5;
        }
    </style>
</head>

<body>
    <div class="dark-mode-toggle">
        <input type="checkbox" id="dark-mode-toggle">
        <label for="dark-mode-toggle" title="Toggle Dark Mode"></label>
    </div>
    <form action="/article" method="post">
        <h1>Enter Website Link</h1>
        <label for="link">Link of the website you want to remove paywall for:</label>
        <input type="text" id="link" name="link" required>
        <input type="submit" value="Submit">
    </form>

    <script>
        const toggleSwitch = document.getElementById('dark-mode-toggle');
        const currentTheme = localStorage.getItem('theme') || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");

        if (currentTheme === "dark") {
            document.body.classList.add("dark-mode");
            toggleSwitch.checked = true;
        }

        toggleSwitch.addEventListener('change', function () {
            if (this.checked) {
                document.body.classList.add("dark-mode");
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.remove("dark-mode");
                localStorage.setItem('theme', 'light');
            }
        });
    </script>
</body>

</html>
"""


def bypass_paywall(url):
    """
    Bypass paywall for a given url
    """
    response = requests.get(url, headers=googlebot_headers)
    response.encoding = response.apparent_encoding
    return response.text


@app.route("/")
def main_page():
    return html


@app.route("/article", methods=["POST"])
def show_article():
    link = flask.request.form["link"]
    try:
        return bypass_paywall(link)
    except requests.exceptions.RequestException as e:
        return str(e), 400
    except e:
        raise e


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET"])
def get_article(path):
    full_url = request.url
    parts = full_url.split("/", 4)
    if len(parts) >= 5:
        actual_url = "https://" + parts[4].lstrip("/")
        try:
            return bypass_paywall(actual_url)
        except requests.exceptions.RequestException as e:
            return str(e), 400
        except e:
            raise e
    else:
        return "Invalid URL", 400


app.run(host="0.0.0.0", port=5000, debug=False)
