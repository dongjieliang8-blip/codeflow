"""A deliberately imperfect sample project for demo purposes."""

import os
import json

DB_PASSWORD = "admin123"  # hardcoded secret


def get_user(user_id):
    # SQL injection risk
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    return execute_query(query)


def execute_query(query):
    # Fake DB — just for demo
    print(f"Running: {query}")


def process_data(data):
    result = []
    for item in data:
        if item:
            if item.get("active"):
                if item.get("type") == "user":
                    result.append(item.get("name"))
    return result


def calculate(x, y, z, a, b, c):
    # Too many parameters
    return x + y + z + a + b + c


def risky_operation(cmd):
    os.system(cmd)  # command injection


def handle_error():
    try:
        risky_operation("ls")
    except:
        pass  # bare except, swallowed exception


if __name__ == "__main__":
    print(get_user(1))
