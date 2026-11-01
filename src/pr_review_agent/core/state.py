pr = {
    "number": 247,
    "comments": [],
    "status": "PENDING",
}


def reset_pr():
    pr["comments"].clear()
    pr["status"] = "PENDING"